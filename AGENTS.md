# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a kitty terminal configuration that ports personal dwm window manager keybindings and workflows to kitty. This is not a general-purpose config - it replicates one specific user's dwm setup with their personal keybindings and tool preferences.

## Key Architecture Decisions

### Configuration Structure

- **kitty.conf**: Main configuration file with all keybindings, layouts, and integrations
- **current-theme.conf**: Active Gruvbox Material color scheme (included via `include` directive in main config)
- **oceanic-next.conf**: Legacy/base color scheme include kept for compatibility
- **Makefile**: Installation automation with dependency management
- **tab_bar.py**: Custom powerline tab renderer with the global quota tracker
- **scripts/quota-cache**: Credential-free cache bridge for OMP and Claude Code usage data

### DWM Philosophy Port

The configuration maps dwm concepts to kitty equivalents:
- dwm tags (1-9) → kitty tabs (1-9)
- dwm master/stack layout → kitty tall/stack layouts with 50/50 bias
- dwm window focus (j/k) → kitty window navigation
- dwm mfact adjustment (h/l) → kitty window resizing
- tab reordering → cmd+shift+left/right moves the active tab one slot (kitty wraps at edges)

### Tool Integration Patterns

#### New Tab Pattern (Context-Creating Actions)
Used for actions that create entirely new contexts (project, directory, remote host):
- Launch directly with `--type=tab`
- Run fzf selector in the new tab
- Auto-close tab if user cancels (Escape) via `&&` chain
- Stay in tab and execute action if selection made
- Examples: Project switcher (cmd+shift+p), directory jumper (cmd+shift+z), SSH launcher (cmd+shift+n)

#### Overlay Pattern (Context-Enhancing Actions)
Used for actions that work within/enhance the current context:
- Launch with `--type=overlay` to show over current window
- Use `--allow-remote-control` if need to send results back to parent window
- Overlay auto-closes after action completes
- Examples: Git TUI (cmd+shift+g), file finder (cmd+g), search scrollback (cmd+shift+h), command history (cmd+r)

#### Tool-Specific Details

**Project Management (Projectile-inspired)**
- Projects managed via explicit inventory: `~/.config/kitty/projects`
- All scripts written in Python for reliability (no PATH dependencies)
- Project switcher checks for existing tabs via `kitten @ ls` before creating new ones
- Tab titles set to project basename for easy identification
- Four management commands (all in scripts/ directory):
  - Switch: Focus existing or create new project tab (new tab pattern)
  - Add: Append current directory to inventory with deduplication (overlay pattern, defaults to Y)
  - Remove: Remove current directory or select from fzf list (overlay pattern, defaults to N)
  - Prune: Scan and remove non-existent directories (overlay pattern)
- Scripts use `wait_for_key()` helper (tty/termios) for "press any key to close" functionality
- Smart confirmations: safe operations default to Y, destructive to N

**SSH Integration**
- SSH launcher parses ~/.ssh/config to display host details (user, hostname, port)
- Custom Python wrapper scripts handle connection string parsing (user@host:port formats)
- Scripts in scripts/ directory: ssh-list (parse config), ssh-connect (launch kitten ssh)
- Error visibility via command display and disconnect messages
- Uses `wait_for_key()` helper for "press any key to close" on disconnect

**Directory Navigation**
- Directory jumper uses `exec zsh` to replace the selector process with a shell in the chosen directory
- Integrates with zoxide for MRU directory tracking

**OMP Integration**
- OMP is the default agentic shell for this configuration
- `cmd+shift+c` launches OMP in the current directory using kitty `--cwd=current`
- `cmd+shift+d` launches OMP in `~/Desktop` using kitty `--cwd=~/Desktop`
- Launchers use `zsh -ic "exec omp"` so kitty gets the user's interactive shell PATH without hard-coding a private OMP install path
- Do not add OMP CLI arguments to these keybindings unless explicitly requested; directory context should come from kitty `--cwd`

**Quota Status**
- `tab_bar.py` keeps the quota status at the right edge for every tab and repaints reset timers every 15 seconds
- OpenAI data comes from `omp usage --provider openai-codex --json`, launched through `zsh -ic` so the interactive PATH resolves OMP
- Claude data comes only from native Claude Code status line JSON piped to `scripts/quota-cache --claude`; initialize it by opening `/usage` and then closing the view
- Cache files contain percentages and reset timestamps only under `${XDG_CACHE_HOME:-$HOME/.cache}/kitty-dwm`
- Missing data renders as `--`; only auto-refreshed OpenAI data older than five minutes renders with `!`

## Installation and Testing

```bash
# Install configuration and all dependencies
make install

# Test configuration changes
# Reload kitty with: cmd+shift+; (semicolon key, Shift+, on Swedish layout)
```

## Important Implementation Details

### Appearance Details
- Active window borders use Gruvbox Material bright yellow (`#d8a657`) at `3pt` for readability
- Inactive window borders use muted Gruvbox gray (`#665c54`) to reduce visual noise

### Keybinding Conflicts
- Uses `cmd` as MODKEY for macOS (would be Super/Mod on Linux/BSD)
- ALL default kitty shortcuts are cleared via `clear_all_shortcuts yes`
- Font size uses both `cmd+plus` (Swedish keyboard) and `cmd+equal` (US keyboard)

### Shell Integration Requirements
- Assumes zsh with Powerlevel10k prompt
- `ignore-shell` flag in close confirmations specifically handles p10k background processes
- `shell_integration enabled no-cursor` enables process detection while preventing cursor shape changes

### Remote Control Architecture
- `allow_remote_control yes` required for tool integrations
- `kitten @` (not `kitty @`) is the correct command for remote control
- Overlay processes need `--allow-remote-control` to communicate with main kitty instance
- Use `--match state:overlay_parent` to target the window beneath an overlay

### Process Protection
- `close_window_with_confirmation ignore-shell` only confirms for actual processes (SSH, htop, etc.)
- Tab closing uses `close_tab` (not `close_tab_with_confirmation` - that action doesn't exist)
- `confirm_os_window_close 1` handles confirmation for tabs with multiple windows containing processes
- `ignore-shell` prevents false positives from Powerlevel10k background jobs
- Relies on shell integration to detect running processes

## Modification Workflow

When changing keybindings or integrations:

1. Edit `kitty.conf` directly - this is the single source of truth
2. Test by reloading config (cmd+shift+; or cmd+shift+, on Swedish layout, within kitty)
3. Update README.md keybinding tables if adding/changing shortcuts
4. Commit atomically - one logical change per commit

## Key Keybindings to Remember

Search functionality uses a three-tier approach:
- `cmd+f` - Find in files by content (ripgrep → nvim at line)
- `cmd+g` - Find files by name (fzf → nvim)
- `cmd+shift+h` - Find in scrollback (fzf → clipboard)

Font size:
- `cmd+plus` / `cmd+equal` - Increase (supports Swedish/US keyboards)
- `cmd+minus` - Decrease
- `cmd+0` - Reset

Fullscreen moved to `cmd+shift+f` to free up `cmd+f` for find

OMP:
- `cmd+shift+c` - Launch OMP in the current directory
- `cmd+shift+d` - Launch OMP in `~/Desktop`
- OMP launchers use `zsh -ic "exec omp"` so kitty gets the user's interactive shell PATH while passing no arguments to OMP; directory context is supplied by kitty `--cwd`
- `cmd+p` forwards `ctrl+p` to cycle OMP models

## Dependencies

Critical dependencies and integrations:
- **fzf**: Core of all interactive launchers
- **ripgrep**: File content search backend
- **kitten @**: Remote control commands (ships with kitty)
- **zoxide**: Directory jumper backend
- **kitten ssh**: Built-in SSH client with automatic remote shell integration
- **lazygit**: Git TUI overlay
- **OMP**: Default agentic shell launched by `cmd+shift+c` and `cmd+shift+d`
- Ensure that the README.md and CLAUDE.md are both up-to-date when changing the behavior of the configuration.
- Never include git-attribution or co-authored-by.
