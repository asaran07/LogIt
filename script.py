import curses

from window_utils import Window

# Constants for menu titles and messages
TITLE_WELCOME = "Welcome to LogIt"
TITLE_CREATE_LOG = "Create a log"
MSG_SELECT_ACTIVITY = "What activity to create a log for?"
MSG_SELECT_OPTIONS = "Please select from the following: "
CR_NEW_ACT = "Create New Activity"
ENTR_ACT_NAME = "Enter Activity Name: "
UTF8 = "utf-8"
MAX_CHARS = 30
NO_ACT_STARTED = "[No Activities Started]"
KEY_FOR_CONTINUE = "Press any key to continue..."
activities = []


def log_time_menu2(window: Window, stdscr):
    current_row = 0
    draw_title_menu(window, stdscr)

    def print_menu(stdscr, selected_row_idx):
        window.clear()
        if len(activities) == 0:
            window.add_text(2, NO_ACT_STARTED)
        else:
            for idx, activity in enumerate(activities):
                if idx == selected_row_idx:
                    window.window.attron(curses.color_pair(1))
                    window.window.addstr(idx + 6, 8, "> " + activity)
                    window.window.attroff(curses.color_pair(1))
                else:
                    window.window.addstr(idx + 6, 8, activity)
        draw_logit_menu(window, stdscr)
        window.add_text(3, "Create new activity (press 'n')")
        window.add_text(4, "Go to main menu (press 'x')")

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(activities):
            current_row += 1
        elif key == ord("\n") and current_row < len(activities):
            log_activity_menu(window, stdscr, activities[current_row])
        elif key == ord("n"):
            activity_creation_menu(window, stdscr)
            print_menu(stdscr, current_row)
        elif key == ord("x"):
            stdscr.clear()
            break

        print_menu(stdscr, current_row)


def enable_input():
    """Enable echo and show cursor."""
    curses.echo()
    curses.curs_set(1)


def disable_input():
    """Disable echo and hide cursor."""
    curses.curs_set(0)
    curses.noecho()


def activity_creation_menu(window: Window, stdscr):
    window.emptyOut()
    window.add_title(2, 4, CR_NEW_ACT)

    enable_input()

    # Prompt for activity name
    window.add_text(1, ENTR_ACT_NAME)
    window.refresh()
    window.window.move(5, 8)  # Move cursor to input position
    activity_name = window.getInput(MAX_CHARS)

    if activity_name:
        # Add activity to the list
        activities.append(activity_name)

        # Show confirmation
        window.emptyOut()
        window.add_title(2, 4, "Activity Created")
        window.add_text(1, f"'{activity_name}' has been added to your activities.")
        window.add_text(4, KEY_FOR_CONTINUE)
        window.refresh()

    disable_input()
    stdscr.getch()  # Wait for user input before returning


def log_activity_menu(window: Window, stdscr, activity):
    window.emptyOut()
    window.add_title(2, 4, f"Log data for {activity}")

    enable_input()

    # Prompt for duration
    window.add_text(1, "Duration (minutes): ")
    window.refresh()
    window.window.move(5, 8)
    duration = window.window.getstr(30).decode("utf-8")

    # Prompt for engagement
    window.add_text(2, "Engagement (0-5): ")
    window.refresh()
    window.window.move(6, 8)
    engagement = window.getInput(MAX_CHARS)

    # Log confirmation
    window.emptyOut()
    window.add_title(2, 4, "Activity logged")
    window.add_text(1, f"Activity: {activity}")
    window.add_text(2, f"Duration: {duration} minutes")
    window.window.addstr(6, 8, f"Engagement: {engagement}")
    window.add_text(4, "Press any key to continue...")
    window.refresh()

    disable_input()
    stdscr.getch()


def logs_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Logs Menu - Work in Progress")
    if len(activities) == 0:
        stdscr.addstr(1, 0, "No Activities Logged")
    else:
        for idx, activity in enumerate(activities):
            stdscr.addstr(
                idx + 1, 0, f"{activity}: {idx + 1} logs"
            )  # Placeholder summary
    stdscr.refresh()
    stdscr.getch()


def draw_menu(window: Window, stdscr, title, message):
    window.center_window(stdscr)
    window.add_title(2, 4, title)
    window.add_border()
    window.add_text(1, message)


def draw_title_menu(window, stdscr):
    draw_menu(window, stdscr, TITLE_WELCOME, MSG_SELECT_OPTIONS)


def draw_logit_menu(window, stdscr):
    draw_menu(window, stdscr, TITLE_CREATE_LOG, MSG_SELECT_ACTIVITY)


def run2(stdscr):
    title_window = Window(40, 120)
    draw_title_menu(title_window, stdscr)
    curses.curs_set(0)
    menu = ["Log Time", "View Logs"]
    current_row = 0

    def print_menu(selected_row_idx):
        title_window.clear()
        height, width = title_window.window.getmaxyx()
        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                title_window.window.attron(curses.color_pair(1))
                title_window.window.addstr(y, x, row)
                title_window.window.attroff(curses.color_pair(1))
            else:
                title_window.window.addstr(y, x, row)
        draw_title_menu(title_window, stdscr)
        title_window.refresh()

    print_menu(current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            if current_row == 0:
                log_time_menu2(title_window, stdscr)
            elif current_row == 1:
                logs_menu(stdscr)
        elif key == ord("q"):
            break

        print_menu(current_row)


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()
    run2(stdscr)


# Start application
curses.wrapper(main)
