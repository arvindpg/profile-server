"""Portfolio screen with tabbed content."""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, Static


CONTENT_DIR = Path(__file__).parent.parent / "content"

TABS = ["About", "Backend", "DevOps", "Frontend", "Security", "Others"]


class TabBar(Horizontal):
    """Simple tab bar using Static widgets."""

    DEFAULT_CSS = """
    TabBar {
        height: 3;
        width: 100%;
        background: $surface-darken-1;
        padding: 0 1;
    }

    TabBar .tab {
        padding: 1 2;
        margin-right: 1;
        background: $surface;
    }

    TabBar .tab.active {
        background: $primary;
        text-style: bold;
    }
    """

    def __init__(self, tabs: list[str], active: int = 0):
        super().__init__()
        self.tabs = tabs
        self.active = active

    def compose(self) -> ComposeResult:
        for i, tab in enumerate(self.tabs):
            classes = "tab active" if i == self.active else "tab"
            yield Static(f" {tab} ", classes=classes, id=f"tab-{i}")

    def set_active(self, index: int) -> None:
        """Set the active tab."""
        self.active = index
        for i, child in enumerate(self.query(".tab")):
            if i == index:
                child.add_class("active")
            else:
                child.remove_class("active")


class PortfolioScreen(Screen):
    """Main portfolio screen with tabs for different sections."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("left", "previous_tab", "Prev Tab"),
        ("right", "next_tab", "Next Tab"),
        ("tab", "next_tab", "Next Tab"),
    ]

    def __init__(self):
        super().__init__()
        self.current_tab = 0
        self.tab_names = ["about", "backend", "devops", "frontend", "security", "others"]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield TabBar(TABS, active=0)
        with VerticalScroll(id="content"):
            yield Markdown(self.load_content("about"), id="markdown-content")
        yield Footer()

    def load_content(self, name: str) -> str:
        """Load markdown content from file."""
        content_file = CONTENT_DIR / f"{name}.md"
        if content_file.exists():
            return content_file.read_text()
        return f"# {name.title()}\n\nContent coming soon..."

    def update_content(self) -> None:
        """Update the displayed content based on current tab."""
        tab_name = self.tab_names[self.current_tab]
        content = self.load_content(tab_name)
        markdown = self.query_one("#markdown-content", Markdown)
        markdown.update(content)

        # Update tab bar
        tab_bar = self.query_one(TabBar)
        tab_bar.set_active(self.current_tab)

    def action_previous_tab(self) -> None:
        """Switch to previous tab."""
        self.current_tab = (self.current_tab - 1) % len(self.tab_names)
        self.update_content()

    def action_next_tab(self) -> None:
        """Switch to next tab."""
        self.current_tab = (self.current_tab + 1) % len(self.tab_names)
        self.update_content()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
