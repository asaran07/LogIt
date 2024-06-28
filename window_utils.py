import curses
from curses import panel


class Window:
    def __init__(self, theHeight, theWidth, start_y, start_x, theTitle=""):
        self.height = theHeight
        self.width = theWidth
        self.y = start_y
        self.x = start_x
        self.title = theTitle
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.panel = panel.new_panel(
            self.window
        )  # TODO: Add feature for having multiple panels, maybe use a list.
        if self.title:
            self.window.addstr(2, 3, self.title, curses.A_BOLD)

    def refresh(self):
        self.window.refresh()

    def show(self):
        self.panel.show()
        panel.update_panels()
        curses.doupdate()

    def hide(self):
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def add_text(self, y: int, x: int, string, attribute=None):
        if attribute:
            self.window.addstr(y, x, string, attribute)
        else:
            self.window.addstr(y, x, string)
        self.refresh()

    def center_window(self, stdscr):
        screen_height, screen_width = stdscr.getmaxyx()
        self.y = (screen_height // 2) - (self.height // 2)
        self.x = (screen_width // 2) - (self.width // 2)
        self.refresh()

    def add_border(self, color_pair):
        self.window.attron(color_pair)
        self.window.box()
        self.window.attroff(color_pair)
