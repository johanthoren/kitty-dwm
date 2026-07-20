#!/usr/bin/env python3
"""Powerline tabs with subscription quota status on the right."""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from kitty.fast_data_types import Screen, add_timer, get_boss, wcswidth
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_tab_with_powerline,
)

CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "kitty-dwm"
COLLECTOR = Path.home() / ".config/kitty/scripts/quota-cache"
COLLECT_INTERVAL = 60
STALE_AFTER = 300
BAR_WIDTH = 10
COLORS = {
    "openai": 0x7DAEA3,
    "claude": 0xE78A4E,
    "grok": 0xD3869B,
    "healthy": 0xA9B665,
    "warning": 0xD8A657,
    "critical": 0xEA6962,
    "muted": 0x928374,
    "background": 0x282828,
    "foreground": 0xD4BE98,
    "track": 0x3C3836,
}

StatusSpan = tuple[str, int, int | None, bool]

_collector: subprocess.Popen[bytes] | None = None
_last_collect = 0.0
_tab_counts: dict[int, int] = {}


def load_cache(name: str) -> dict[str, Any]:
    try:
        with (CACHE_DIR / name).open() as source:
            return json.load(source)
    except (OSError, ValueError, TypeError):
        return {}


def reset_in(resets_at: float, now: float) -> str:
    seconds = max(0, int(resets_at - now))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes = seconds // 60
    if days:
        return f"{days}d" + (f"{hours}h" if hours else "")
    if hours:
        return f"{hours}h" + (f"{minutes}m" if minutes else "")
    return f"{minutes}m"


def quota_color(used: int) -> int:
    if used >= 90:
        return COLORS["critical"]
    if used >= 80:
        return COLORS["warning"]
    return COLORS["healthy"]


def usage_bar(used: int, timer: str) -> list[StatusSpan]:
    text = timer.center(BAR_WIDTH)
    filled = used * BAR_WIDTH // 100
    color = quota_color(used)
    spans: list[StatusSpan] = []
    if filled:
        spans.append((text[:filled], COLORS["background"], color, True))
    if filled < BAR_WIDTH:
        spans.append((text[filled:], COLORS["foreground"], COLORS["track"], True))
    return spans


def provider_spans(
    label: str,
    color: int,
    cache_name: str,
    expected_windows: tuple[tuple[str, str], ...],
    now: float,
    show_missing: bool = False,
    stale_after: float | None = None,
) -> list[StatusSpan]:
    cache = load_cache(cache_name)
    spans: list[StatusSpan] = [(f" ● {label} ", color, None, True)]
    found = False
    for key, window_label in expected_windows:
        window = cache.get(key)
        separator = "" if not found else " · "
        if not isinstance(window, dict):
            if show_missing:
                spans.append((f"{separator}{window_label} --", COLORS["muted"], None, False))
                found = True
            continue
        try:
            used = max(0, min(100, round(float(window["usedPercentage"]))))
            timer = reset_in(float(window["resetsAt"]), now)
        except (KeyError, TypeError, ValueError):
            continue
        spans.extend(
            (
                (f"{separator}{window_label} ", COLORS["muted"], None, False),
                *usage_bar(used, timer),
                (f" {used}%", quota_color(used), None, True),
            )
        )
        found = True
    if not found:
        spans.append(("--", COLORS["muted"], None, False))
    if cache and stale_after is not None and now - float(cache.get("updatedAt", 0)) > stale_after:
        spans.append((" !", COLORS["warning"], None, True))
    return spans


def status_spans(now: float | None = None) -> list[StatusSpan]:
    now = time.time() if now is None else now
    clock = time.strftime("%H:%M", time.localtime(now))
    openai = provider_spans(
        "OAI",
        COLORS["openai"],
        "openai-usage.json",
        (("fiveHour", "5h"), ("weekly", "wk")),
        now,
        stale_after=STALE_AFTER,
    )
    grok = provider_spans(
        "XAI",
        COLORS["grok"],
        "grok-usage.json",
        (("weekly", "wk"), ("monthly", "mo")),
        now,
        stale_after=STALE_AFTER,
    )
    claude = provider_spans(
        "CC",
        COLORS["claude"],
        "claude-usage.json",
        (("fiveHour", "5h"), ("weekly", "wk")),
        now,
        show_missing=True,
    )
    sep: StatusSpan = (" ", COLORS["muted"], None, False)
    return [
        *openai,
        sep,
        *grok,
        sep,
        *claude,
        ("   ", COLORS["warning"], None, False),
        (clock, COLORS["foreground"], None, True),
        (" ", COLORS["muted"], None, False),
    ]


def mark_tab_bars_dirty(timer_id: int | None = None) -> None:
    for tab_manager in get_boss().all_tab_managers:
        tab_manager.mark_tab_bar_dirty()


def collect_usage() -> None:
    global _collector, _last_collect
    now = time.monotonic()
    if _collector is not None and _collector.poll() is not None:
        _collector = None
    if _collector is None and now - _last_collect >= COLLECT_INTERVAL and COLLECTOR.is_file():
        _collector = subprocess.Popen(
            ["/bin/zsh", "-ic", 'exec "$1"', "quota-cache", str(COLLECTOR)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _last_collect = now


def refresh_usage(timer_id: int | None = None) -> None:
    collect_usage()
    mark_tab_bars_dirty()


def ensure_refresh_timer() -> None:
    boss = get_boss()
    attribute = "_kitty_dwm_quota_timer_started"
    if getattr(boss, attribute, False):
        return
    setattr(boss, attribute, True)
    add_timer(refresh_usage, 0, False)
    add_timer(refresh_usage, 1, True)


def draw_status(draw_data: DrawData, screen: Screen, spans: list[StatusSpan]) -> int:
    text = "".join(part for part, _, _, _ in spans)
    start = max(0, screen.columns - wcswidth(text))
    screen.cursor.x = start
    default_bg = as_rgb(int(draw_data.default_bg))
    for part, color, background, bold in spans:
        screen.cursor.fg = as_rgb(color)
        screen.cursor.bg = default_bg if background is None else as_rgb(background)
        screen.cursor.bold = bold
        screen.draw(part)
    screen.cursor.bg = default_bg
    screen.cursor.bold = False
    return start


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_tab_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    if extra_data.for_layout:
        if is_last:
            _tab_counts[draw_data.os_window_id] = index
        return draw_tab_with_powerline(
            draw_data, screen, tab, before, max_tab_length, index, is_last, extra_data
        )

    ensure_refresh_timer()
    collect_usage()
    spans = status_spans()
    status_start = screen.columns - wcswidth("".join(part for part, _, _, _ in spans))
    tab_count = _tab_counts.get(draw_data.os_window_id, index)
    tab_boundary = max(3, status_start * index // max(1, tab_count))
    available = max(3, tab_boundary - before)
    end = draw_tab_with_powerline(
        draw_data, screen, tab, before, min(max_tab_length, available), index, is_last, extra_data
    )
    if is_last:
        status_start = draw_status(draw_data, screen, spans)
        return min(end, status_start)
    return end
