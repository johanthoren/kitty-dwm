# DWM-like Kitty Configuration

A [kitty](https://sw.kovidgoyal.net/kitty/) terminal configuration that replicates my personal [dwm](https://dwm.suckless.org/) setup, porting over my keybindings and workflows to the terminal multiplexer.

## About

This configuration recreates my dwm window manager experience within kitty. The keybindings and behaviors are specific to my personal dwm configuration - if you use different dwm bindings, you'll want to adjust these accordingly.

Key aspects ported from my dwm setup:

- **Master/Stack layouts** - Tall layout with 55/45 split ratio
- **hjkl navigation** - Window focus and resizing
- **Tag-based tabs** - My 1-9 tag workflow mapped to kitty tabs
- **Keyboard-driven** - All operations via keybindings
- **Integrated tooling** - fzf-based launchers I've added for terminal workflows

## Features

- **DWM-style layouts**: Tall, fat, and stack layouts with master/stack ratio control
- **Custom tab bar**: Always-visible tab bar with date/time status display
- **Smart integrations**:
  - File finder with preview (fzf + bat + neovim)
  - Git TUI (lazygit)
  - Directory jumper (zoxide + fzf)
  - SSH manager (sshs)
  - Scrollback search (fzf)
  - Kitten hints for URL/path selection
- **Process protection**: Warns before closing tabs with running processes (SSH, builds, etc.)
- **Window state memory**: Remembers window size, position, and fullscreen state
- **Oceanic Next theme**: Clean, modern color scheme
- **Shell integration**: Cursor shape protection, process detection

## Installation

### Prerequisites

- macOS (Linux/BSD users: replace `cmd` with your mod key in config)
- [Homebrew](https://brew.sh)

### Quick Install

```bash
git clone https://github.com/johanthoren/kitty-dwm.git ~/.config/kitty-dwm
cd ~/.config/kitty-dwm
make install
```

This will:
1. Install kitty and all dependencies (fzf, bat, neovim, lazygit, zoxide, sshs)
2. Create symlinks to your `~/.config/kitty/` directory
3. Prompt before overwriting existing configs

**Important**: On macOS, grant kitty Full Disk Access in System Settings → Privacy & Security → Full Disk Access. This is required for integrations (file finder, scrollback search, etc.) to work properly.

### Manual Installation

```bash
# Install dependencies
brew install --cask kitty
brew install fzf bat neovim lazygit zoxide sshs

# Link configs
ln -s ~/.config/kitty-dwm/kitty.conf ~/.config/kitty/kitty.conf
ln -s ~/.config/kitty-dwm/oceanic-next.conf ~/.config/kitty/oceanic-next.conf
```

## Keybindings

### Window Management (DWM-inspired)

| Key | Action | DWM Equivalent |
|-----|--------|----------------|
| `cmd+j` | Focus next window | `Mod+j` (focusstack +1) |
| `cmd+k` | Focus previous window | `Mod+k` (focusstack -1) |
| `cmd+h` | Shrink master area | `Mod+h` (setmfact -0.05) |
| `cmd+l` | Expand master area | `Mod+l` (setmfact +0.05) |
| `cmd+space` | Move window to master | `Mod+Return` (zoom) |
| `cmd+return` | New window (inherit cwd) | `Mod+Shift+Return` (spawn) |
| `cmd+n` | New window (home dir) | - |
| `cmd+w` | Close window* | `Mod+Shift+c` (killclient) |
| `cmd+shift+f` | Toggle fullscreen | `Mod+f` (togglefullscr) |
| `cmd+shift+j` | Move window forward | - |
| `cmd+shift+k` | Move window backward | - |
| `cmd+e` | Equalize window sizes | - |

*Confirms before closing if processes are running

### Layouts

| Key | Action | DWM Equivalent |
|-----|--------|----------------|
| `cmd+shift+l` | Cycle layouts | `Mod+t/m/f` (setlayout) |

Available layouts: tall (master/stack), fat (stack/master), stack (fullscreen cycling)

### Tab Management (Tags)

| Key | Action | DWM Equivalent |
|-----|--------|----------------|
| `cmd+1` to `cmd+9` | Go to tab N | `Mod+[1-9]` (view tag) |
| `cmd+t` | New tab | - |
| `cmd+shift+w` | Close tab* | - |

*Confirms before closing if processes are running

### Integrated Tools

| Key | Action | Description |
|-----|--------|-------------|
| `cmd+f` | Find in files | ripgrep content search → opens in neovim at matching line |
| `cmd+p` | File finder | fzf file picker → opens in neovim |
| `cmd+u` | Open URL | Select URL from screen and open in browser |
| `cmd+shift+p` | Insert path | Select path from screen and insert at cursor |
| `cmd+shift+o` | Open path in nvim | Select path from screen and open in neovim |
| `cmd+shift+y` | Copy line | Select line from screen and copy to clipboard |
| `cmd+shift+g` | Git TUI | Launch lazygit in overlay |
| `cmd+shift+z` | Directory jumper | zoxide picker → new tab in directory |
| `cmd+shift+s` | SSH launcher | sshs picker → new tab with SSH session |
| `cmd+shift+h` | Search scrollback | fzf search → copy to clipboard |
| `cmd+shift+a` | Launch Claude Code | New window with Claude in current directory |

### Kitty Management

| Key | Action |
|-----|--------|
| `cmd+shift+r` | Reload config |
| `cmd+r` | Command history search |
| `cmd+b` | Toggle tab bar |
| `cmd+shift+x` | Show scrollback buffer |
| `cmd+shift+escape` | Kitty shell (debugging) |
| `cmd+c` | Copy to clipboard |
| `cmd+v` | Paste from clipboard |
| `cmd++` / `cmd+=` | Increase font size |
| `cmd+-` | Decrease font size |
| `cmd+0` | Reset font size |
| `page_up` / `page_down` | Scroll up/down one page |
| `home` / `end` | Scroll to top/bottom |
| `ctrl+u` / `ctrl+d` | Scroll up/down (vim-style) |
| `cmd+q` | Quit kitty |

## Dependencies

- **[kitty](https://sw.kovidgoyal.net/kitty/)** - Terminal emulator
- **[fzf](https://github.com/junegunn/fzf)** - Fuzzy finder
- **[bat](https://github.com/sharkdp/bat)** - File preview with syntax highlighting
- **[neovim](https://neovim.io/)** - Text editor
- **[lazygit](https://github.com/jesseduffield/lazygit)** - Git TUI
- **[zoxide](https://github.com/ajeetdsouza/zoxide)** - Smart directory jumper
- **[sshs](https://github.com/quantumsheep/sshs)** - SSH connection manager

## Configuration

The main configuration is in `kitty.conf`. Key sections:

- **Appearance**: Font (MesloLGS Nerd Font), borders, theme inclusion
- **Layouts**: DWM-style tall/fat/stack configurations
- **Keybindings**: All mappings using `cmd` as mod key (macOS)
- **FZF Integrations**: Tool launchers and pickers
- **Behavior**: Shell integration, remote control, confirmations

### Customization

Edit `kitty.conf` to customize:
- Change `cmd` to your preferred mod key
- Adjust layout bias (default 55% master)
- Modify color scheme (see `oceanic-next.conf`)
- Add/remove FZF integrations

## DWM Mapping Comparison

| DWM Concept | Kitty Equivalent | Implementation |
|-------------|------------------|----------------|
| Master/Stack | Tall/Fat layouts | `enabled_layouts tall:bias=55;...` |
| Tags (1-9) | Tabs (1-9) | `goto_tab N` |
| focusstack | Window focus | `next_window` / `previous_window` |
| setmfact | Resize master | `resize_window narrower/wider` |
| zoom | Move to master | `move_window_to_top` |
| killclient | Close window | `close_window_with_confirmation` |

## Tips

1. **Shell setup**: This configuration assumes zsh with [Powerlevel10k](https://github.com/romkatv/powerlevel10k) prompt. Some settings (like `ignore-shell` in close confirmations) are specifically to accommodate p10k's background processes.
2. **Shell integration**: Requires zsh/bash with kitty integration for process detection
3. **Remote processes**: Confirmation works for local processes (including SSH client), but not processes on remote hosts
4. **SSH sessions**: Use `cmd+shift+s` for managed sessions that auto-close on exit

## License

MIT License

## Credits

- Inspired by [dwm](https://dwm.suckless.org/) by suckless.org
- Built on [kitty](https://sw.kovidgoyal.net/kitty/) by Kovid Goyal
- Theme: [Oceanic Next](https://github.com/voronianski/oceanic-next-color-scheme)

Special thanks to Kovid Goyal for creating kitty - it's like you read my mind.
