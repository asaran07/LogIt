import curses
from curses import COLOR_BLACK, COLOR_GREEN, COLOR_WHITE, panel
from typing import Optional


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

    def add_text(
        self,
        y: int,
        x: int,
        text: str,
        wrap: bool = False,
        align: str = "left",
        attribute: Optional[int] = None,
    ):
        """
        Add text to the window at the specified coordinates.

        :param y: Y-coordinate (row) to start the text
        :param x: X-coordinate (column) to start the text
        :param text: The text to display
        :param wrap: Whether to wrap the text if it exceeds the window width
        :param align: Text alignment ('left', 'center', or 'right')
        :param attribute: Curses attribute for the text (e.g., curses.A_BOLD)
        """
        max_width = self.width - x - 1  # Maximum width for text

        if wrap:
            words = text.split()
            lines = []
            current_line = []
            current_width = 0

            for word in words:
                if current_width + len(word) + 1 <= max_width:
                    current_line.append(word)
                    current_width += len(word) + 1
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = len(word)

            if current_line:
                lines.append(" ".join(current_line))
        else:
            lines = [text[:max_width]]

        for i, line in enumerate(lines):
            if align == "center":
                x_pos = x + (max_width - len(line)) // 2
            elif align == "right":
                x_pos = x + max_width - len(line)
            else:  # 'left' align
                x_pos = x

            if y + i < self.height:
                if attribute:
                    self.window.addstr(y + i, x_pos, line, attribute)
                else:
                    self.window.addstr(y + i, x_pos, line)

        self.refresh()

    def add_centered_text(self, y: int, text: str, attribute: Optional[int] = None):
        """
        Add centered text to the window at the specified y-coordinate.

        :param y: Y-coordinate of the start of the text
        :param text: The text to display
        :param attribute: Curses attribute for the text (e.g., curses.A_BOLD)
        """
        x = (self.width - len(text)) // 2
        self.add_text(y, x, text, align="center", attribute=attribute)

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

    def getInputWprompt(self, prompt_string: str, max_input_chars) -> str:
        self.add_text(4, 6, prompt_string)
        self.refresh()
        self.window.move(5, 6)  # Move cursor to input position
        return self.getInput(max_input_chars)

    def startColoring(self, color_pair):
        self.window.attron(curses.color_pair(color_pair))

    def stopColoring(self, color_pair):
        self.window.attroff(curses.color_pair(color_pair))
