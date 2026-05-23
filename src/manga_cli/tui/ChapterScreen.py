from textual.app import App
from textual.widgets import Label, Header, Input, Footer, ListItem, ListView
from textual.reactive import reactive
from textual.screen import Screen

    
class ChapterScreen(Screen):
    """ shows chapter list for selected manga """
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, manga: dict):
        super().__init__()
        self.manga = manga
        self.chapters : list[dict] = []

    def compose(self):
        yield Header(show_clock=False)
        title = self.manga.get("title", "unknown")
        status = self.manga.get("status", "unknown")
        yield Label(f"[bold]{title}[/bold]  [{status}]", id="manga-title")
        yield ListView(id="chapters-list")
        yield Label("Enter to read • Escape to go back • Q to quit", id="status-label")
        yield Footer()

    def on_mount(self):
        chapter_list = self.query_one("#chapters-list", ListView)
        for i in range(1, 11):
            chapter_list.append(ListItem(Label(f"Chapter {i} — Page 1-20")))
    
    def on_list_view_selected(self, event: ListView.Selected):
        index = event.list_view.index
        chp_num = index + 1
        self.notify(f"Opening chapter {chp_num} in reader...")