import curses
from curses import A_BLINK, A_DIM, COLOR_BLACK, COLOR_GREEN, COLOR_WHITE, panel
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

    def startColoring(self, color_pair):
        self.window.attron(curses.color_pair(color_pair))

    def stopColoring(self, color_pair):
        self.window.attroff(curses.color_pair(color_pair))

    def draw_border(self):
        self.window.border()
        self.refresh()

    def getInputWithPrompt(
        self,
        title_string: str,
        prompt_string: str,
        max_input_chars: int,  # TODO: Add parameter for dynamic cancel message
    ) -> str:
        self.clear()
        self.draw_border()
        title_y, title_x = 2, 4
        prompt_y, prompt_x = 4, 6
        input_y, input_x = 5, 6
        instruction_y = self.height - 3

        self.add_title(title_y, title_x, title_string)
        self.add_text(prompt_y, prompt_x, prompt_string)
        self.add_text(
            instruction_y,
            6,
            "Press Enter to finish or Esc to cancel",
            attribute=curses.A_DIM,
        )

        input_str = ""
        while True:
            self.window.move(input_y, input_x)
            self.window.clrtoeol()  # Clear the input line
            self.window.addstr(input_y, input_x, input_str)
            self.draw_border()  # Redraw border to fix any cleared parts
            self.refresh()

            char = self.window.getch()

            if char == 27:  # Escape
                curses.curs_set(0)
                self.emptyOut()
                self.add_text(
                    2,
                    4,
                    "[i] log creation canceled",  # BUG: Static 'log' message for all scenarios
                    attribute=curses.A_BLINK | curses.A_BOLD | curses.A_ITALIC,
                )
                self.add_text(
                    instruction_y,
                    4,
                    "returning to main menu...",
                    attribute=curses.A_DIM,
                )
                self.refresh()
                curses.napms(400)
                return ""
            elif char == 10:  # Enter
                if input_str:
                    curses.curs_set(0)
                    self.add_text(
                        input_y,
                        input_x,
                        input_str,
                        attribute=curses.A_BOLD | curses.A_BLINK | curses.A_REVERSE,
                    )
                    self.refresh()
                    curses.napms(50)
                    self.add_text(
                        input_y,
                        input_x,
                        input_str,
                        attribute=curses.A_BOLD | curses.A_BLINK,
                    )
                    curses.napms(50)
                    curses.curs_set(1)
                    return input_str
            elif char == curses.KEY_BACKSPACE or char == 127:  # Backspace
                input_str = input_str[:-1]
            elif (
                len(input_str) < max_input_chars and 32 <= char <= 126
            ):  # Printable characters
                input_str += chr(char)  # TODO: Make the user input appear italic.
