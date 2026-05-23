from .SearchScreen import SearchScreen


def run_tui(initial_query: str = ""):
    app = SearchScreen(initial_query=initial_query)
    app.run()