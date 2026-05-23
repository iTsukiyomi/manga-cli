from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Input, Footer, ListItem, ListView
from textual.reactive import reactive
from textual.screen import Screen
from .ChapterScreen import ChapterScreen

class SearchScreen(App):
    """ a search screen """
    CSS = """
    Screen {
        background: $surface;
    }

    #search-input {
        dock: top;
        margin: 1 2;
    }

    #results-list {
        margin: 0 2;
        height: 1fr;
        border: round $primary;
    }

    #status-label {
        dock: bottom;
        height: 1;
        margin: 0 2;
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

    results : reactive[list[dict]] = reactive([])

    def __init__(self, initial_query: str = ""):
        super().__init__()
        self.initial_query = initial_query
        self._debounce_timer = None
        self._current_results = []

    def compose(self):
        yield Header(show_clock=False)
        yield Input(placeholder="Search for a manga...", id="search-input", value=self.initial_query)
        yield ListView(id="results-list")
        yield Label("Type to search • ↑↓ to navigate • Enter to select • Q to quit", id="status-label")
        yield Footer()
    
    def on_mount(self):
        self.query_one("#search-input", Input).focus()
        if self.initial_query:
            self._do_search(self.initial_query)

    def on_input_changed(self, event: Input.Changed):
        """ triggers everytime user types or delete in input widget """
        query = event.value.strip()

        if self._debounce_timer is not None:
            self._debounce_timer.stop()

        if query:
            self._debounce_timer = self.set_timer(0.35, lambda: self._do_search(query))
        else:
            self._clear_results()
    
    def _do_search(self, query: str):
        fake_results = [
            {"title": f"{query} — Volume 1", "status": "ongoing",   "chapters": 120},
            {"title": f"{query} — Special",  "status": "completed", "chapters": 45},
            {"title": f"{query} Adventures", "status": "ongoing",   "chapters": 78},
        ]
        self._update_result_list(fake_results)
    
    def _clear_results(self):
        self.query_one("#results-list", ListView).clear()

    def _update_result_list(self, results: list[dict]):
        self._current_results = results
        list_view = self.query_one("#results-list", ListView)
        list_view.clear()
        
        for manga in results:
            status_color = "green" if manga['status'] == "ongoing" else "blue"
            label_txt = (
                f"{manga['title']} "
                f"[{status_color}][{manga['status']}][/{status_color}]"
                f"{manga['chapters']} chapters"
            )
            list_view.append(ListItem(Label(label_txt)))

    def on_list_view_selected(self, event: ListView.Selected):
        """ triggers when user selects a list item"""
        index = event.list_view.index
        if index < len(self._current_results):
            manga = self._current_results[index]
        else:
            manga = {"title": "Unknown Manga", "status": "ongoing", "chapters": 0}

        self.app.push_screen(ChapterScreen(manga))