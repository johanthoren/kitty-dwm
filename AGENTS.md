# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a kitty terminal configuration that ports personal dwm window manager keybindings and workflows to kitty. This is not a general-purpose config - it replicates one specific user's dwm setup with their personal keybindings and tool preferences.

## Key Architecture Decisions

### Configuration Structure

- **kitty.conf**: Main configuration file with all keybindings, layouts, and integrations
- **oceanic-next.conf**: Color scheme (included via `include` directive in main config)
- **Makefile**: Installation automation with dependency management

### DWM Philosophy Port

The configuration maps dwm concepts to kitty equivalents:
- dwm tags (1-9) → kitty tabs (1-9)
- dwm master/stack layout → kitty tall/fat layouts with 55/45 bias
- dwm window focus (j/k) → kitty window navigation
- dwm mfact adjustment (h/l) → kitty window resizing

### Tool Integration Patterns

#### New Tab Pattern (Context-Creating Actions)
Used for actions that create entirely new contexts (project, directory, remote host):
- Launch directly with `--type=tab`
- Run fzf selector in the new tab
- Auto-close tab if user cancels (Escape) via `&&` chain
- Stay in tab and execute action if selection made
- Examples: Project switcher (cmd+shift+p), directory jumper (cmd+shift+z), SSH launcher (cmd+shift+s)

#### Overlay Pattern (Context-Enhancing Actions)
Used for actions that work within/enhance the current context:
- Launch with `--type=overlay` to show over current window
- Use `--allow-remote-control` if need to send results back to parent window
- Overlay auto-closes after action completes
- Examples: Git TUI (cmd+shift+g), file finder (cmd+p), search scrollback (cmd+shift+h), command history (cmd+r)

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

## Installation and Testing

```bash
# Install configuration and all dependencies
make install

# Test configuration changes
# Reload kitty with: cmd+shift+r (keybinding in config)
```

## Important Implementation Details

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
2. Test by reloading config (cmd+shift+r within kitty)
3. Update README.md keybinding tables if adding/changing shortcuts
4. Commit atomically - one logical change per commit

## Key Keybindings to Remember

Search functionality uses a three-tier approach:
- `cmd+f` - Find in files by content (ripgrep → nvim at line)
- `cmd+p` - Find files by name (fzf → nvim)
- `cmd+shift+h` - Find in scrollback (fzf → clipboard)

Font size:
- `cmd+plus` / `cmd+equal` - Increase (supports Swedish/US keyboards)
- `cmd+minus` - Decrease
- `cmd+0` - Reset

Fullscreen moved to `cmd+shift+f` to free up `cmd+f` for find

## Dependencies

All managed via Makefile, but critical ones:
- **fzf**: Core of all interactive launchers
- **ripgrep**: File content search backend
- **kitten @**: Remote control commands (ships with kitty)
- **zoxide**: Directory jumper backend
- **kitten ssh**: Built-in SSH client with automatic remote shell integration
- **lazygit**: Git TUI overlay
- Ensure that the README.md and CLAUDE.md are both up-to-date when changing the behavior of the configuration.
- Never include git-attribution or co-authored-by.