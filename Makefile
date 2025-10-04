.PHONY: install deps

install: deps
	@echo "Installing Kitty configuration..."
	@if [ -L ~/.config/kitty ]; then \
		if [ "$$(readlink ~/.config/kitty)" = "$(PWD)" ]; then \
			echo "✓ ~/.config/kitty already linked to this directory"; \
		else \
			echo "✗ ERROR: ~/.config/kitty is a symlink to another location"; \
			echo "  Current target: $$(readlink ~/.config/kitty)"; \
			exit 1; \
		fi \
	elif [ -e ~/.config/kitty ]; then \
		read -p "~/.config/kitty already exists. Replace with symlink? (y/N) " answer; \
		if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
			rm -rf ~/.config/kitty; \
			ln -s $(PWD) ~/.config/kitty; \
			echo "✓ Linked ~/.config/kitty -> $(PWD)"; \
		else \
			echo "✗ Skipped installation"; \
			exit 1; \
		fi \
	else \
		ln -s $(PWD) ~/.config/kitty; \
		echo "✓ Linked ~/.config/kitty -> $(PWD)"; \
	fi
	@echo ""
	@echo "Installation complete! Reload kitty config with cmd+shift+r"

deps:
	@echo "Checking dependencies..."
	@command -v brew >/dev/null 2>&1 || { echo "✗ Homebrew not found. Install from https://brew.sh"; exit 1; }
	@echo "✓ Homebrew installed"
	@command -v kitty >/dev/null 2>&1 || { echo "Installing kitty..."; brew install --cask kitty; }
	@echo "✓ kitty installed"
	@command -v fzf >/dev/null 2>&1 || { echo "Installing fzf..."; brew install fzf; }
	@echo "✓ fzf installed"
	@command -v bat >/dev/null 2>&1 || { echo "Installing bat..."; brew install bat; }
	@echo "✓ bat installed"
	@command -v nvim >/dev/null 2>&1 || { echo "Installing neovim..."; brew install neovim; }
	@echo "✓ neovim installed"
	@command -v lazygit >/dev/null 2>&1 || { echo "Installing lazygit..."; brew install lazygit; }
	@echo "✓ lazygit installed"
	@command -v zoxide >/dev/null 2>&1 || { echo "Installing zoxide..."; brew install zoxide; }
	@echo "✓ zoxide installed"
	@command -v sshs >/dev/null 2>&1 || { echo "Installing sshs..."; brew install sshs; }
	@echo "✓ sshs installed"
	@echo ""
