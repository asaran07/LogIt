import curses
from curses import COLOR_BLACK, COLOR_GREEN, COLOR_WHITE, panel


class Window:
    def __init__(self, theHeight, theWidth, start_y=0, start_x=0):
        self.height = theHeight
        self.width = theWidth
        self.y = start_y
        self.x = start_x
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        # self.panel = panel.new_panel(self.window)

    def add_title(self, start_y, start_x, string):
        curses.start_color()
        curses.init_pair(1, COLOR_GREEN, COLOR_BLACK)
        self.window.attron(curses.color_pair(1))
        self.window.addstr(start_y, start_x, string, curses.A_BOLD)
        self.window.attroff(curses.color_pair(1))
        self.refresh()

    def refresh(self):
        self.window.refresh()
        curses.doupdate()

    def show(self):
        # self.panel.show()
        panel.update_panels()
        curses.doupdate()

    def hide(self):
        # self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def add_text(self, position, string, attribute=None):
        """Add text to the window, according to a position number"""
        positions = {1: (4, 6), 2: (5, 8), 3: (35, 8), 4: (36, 8)}

        y, x = positions.get(
            position, (0, 0)
        )  # Default to (0, 0) if position is invalid
        if attribute:
            self.window.addstr(y, x, string, attribute)
        else:
            self.window.addstr(y, x, string)
        self.refresh()

    def center_window(self, stdscr):
        """Center window relative to the screen"""
        screen_height, screen_width = stdscr.getmaxyx()
        self.y = (screen_height // 2) - (self.height // 2)
        self.x = (screen_width // 2) - (self.width // 2)
        self.window.mvwin(self.y, self.x)
        self.refresh()

    def add_border(self):
        """Add a solid white border aroud the window"""
        curses.start_color()
        curses.init_pair(2, COLOR_WHITE, COLOR_BLACK)
        self.window.attron(curses.color_pair(2))
        self.window.box()
        self.window.attroff(curses.color_pair(2))
        self.refresh()

    def clear(self):
        self.window.clear()

    def emptyOut(self):
        """Clear the window and add default border"""
        self.clear()
        self.add_border()

    def getInput(self, max_characters) -> str:
        return self.window.getstr(max_characters).decode("utf-8")
