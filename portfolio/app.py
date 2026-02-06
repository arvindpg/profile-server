"""Portfolio TUI Application."""

from textual.app import App

from screens.portfolio import PortfolioScreen


class PortfolioApp(App):
    """A TUI portfolio application served over SSH."""

    TITLE = "Arvind's Portfolio"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False  # Disable command palette for SSH

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("tab", "next_tab", "Next Tab"),
        ("shift+tab", "previous_tab", "Previous Tab"),
    ]

    def action_next_tab(self) -> None:
        """Switch to next tab."""
        try:
            from textual.widgets import TabbedContent
            tabs = self.query_one(TabbedContent)
            tabs.action_next_tab()
        except Exception:
            pass

    def action_previous_tab(self) -> None:
        """Switch to previous tab."""
        try:
            from textual.widgets import TabbedContent
            tabs = self.query_one(TabbedContent)
            tabs.action_previous_tab()
        except Exception:
            pass

    def on_mount(self) -> None:
        """Set up the app on mount."""
        self.push_screen(PortfolioScreen())


def main():
    """Run the app directly for testing."""
    app = PortfolioApp()
    app.run()


if __name__ == "__main__":
    main()
