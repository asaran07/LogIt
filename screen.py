import curses
from typing import Any, Tuple


class Screen:
    def __init__(self, stdscr: Any) -> None:
        self.stdscr = stdscr
        self._cursor_visible = True

    @property
    def cursor_visible(self) -> bool:
        return self._cursor_visible

    @cursor_visible.setter
    def cursor_visible(self, visible: bool) -> None:
        curses.curs_set(1 if visible else 0)
        self._cursor_visible = visible

    def refresh(self) -> None:
        self.stdscr.refresh()

    def clear(self) -> None:
        self.stdscr.clear()

    def get_input(self) -> str:
        return self.stdscr.getstr().decode("utf-8")

    def draw_border(self) -> None:
        self.stdscr.border()

    def add_str(self, y: int, x: int, string: str, attr: int = curses.A_NORMAL) -> None:
        try:
            self.stdscr.addstr(y, x, string, attr)
        except curses.error:
            # WARN: Need to handle potential curses errors, e.g., writing outside the window
            pass

    def get_screen_size(self) -> Tuple[int, int]:
        return self.stdscr.getmaxyx()
