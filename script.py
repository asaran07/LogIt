import curses
from curses import (
    COLOR_BLACK,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_WHITE,
    COLOR_YELLOW,
    panel,
)

activities = []


def main_menu(stdscr):
    curses.curs_set(0)
    menu = ["Log Time", "View Logs"]
    current_row = 0

    def print_menu(stdscr, selected_row_idx):
        stdscr.clear()
        for idx, row in enumerate(menu):
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 1, 2, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 1, 2, row)
        stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            if current_row == 0:
                log_time_menu(stdscr)
            elif current_row == 1:
                logs_menu(stdscr)
        elif key == ord("q"):
            break

        print_menu(stdscr, current_row)


def log_time_menu(stdscr):
    current_row = 0

    def print_menu(stdscr, selected_row_idx):
        stdscr.clear()
        if len(activities) == 0:
            stdscr.addstr(0, 0, "No Activities Started")
        else:
            for idx, activity in enumerate(activities):
                if idx == selected_row_idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(idx, 0, activity)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(idx, 0, activity)
        stdscr.addstr(len(activities), 0, "Create new activity (press 'n')")
        stdscr.addstr(len(activities) + 1, 0, "Go to main menu (press 'x')")
        stdscr.refresh()

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(activities):
            current_row += 1
        elif key == ord("\n") and current_row < len(activities):
            log_activity_menu(stdscr, activities[current_row])
        elif key == ord("n"):
            activity_creation_menu(stdscr)
            print_menu(stdscr, current_row)
        elif key == ord("x"):
            break

        print_menu(stdscr, current_row)


def activity_creation_menu(stdscr):
    curses.curs_set(1)
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter Activity Name: ")
    activity_name = stdscr.getstr().decode("utf-8")
    stdscr.addstr(1, 0, "Select Activity Type: [digital, physical, meeting, misc] ")
    activity_type = stdscr.getstr().decode("utf-8")
    activities.append(activity_name)
    stdscr.addstr(3, 0, "Activity created")
    curses.curs_set(0)
    stdscr.refresh()
    curses.napms(1000)
    curses.noecho()


def log_activity_menu(stdscr, activity):
    curses.curs_set(1)
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, f"Log data for {activity}")
    stdscr.addstr(1, 0, "Duration (minutes): ")
    duration = stdscr.getstr().decode("utf-8")
    stdscr.addstr(2, 0, "Engagement (0-5): ")
    engagement = stdscr.getstr().decode("utf-8")
    stdscr.addstr(4, 0, "Activity logged")
    stdscr.refresh()
    curses.napms(1000)
    curses.noecho()


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


def run(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    win_height = 40
    win_width = 120

    curses.start_color()
    curses.init_pair(1, COLOR_WHITE, COLOR_BLACK)
    curses.init_pair(2, COLOR_GREEN, COLOR_BLACK)

    # Calculate top-left corner coordinates to center the window
    start_y = (screen_height // 2) - (win_height // 2)
    start_x = (screen_width // 2) - (win_width // 2)

    main_window = curses.newwin(win_height, win_width, start_y, start_x)
    main_window.attron(curses.color_pair(1))
    main_window.box()
    main_window.attroff(curses.color_pair(1))

    main_window.attron(curses.color_pair(2))
    main_window.addstr(2, 3, "Welcome to LogIt")
    main_window.attroff(curses.color_pair(2))

    main_panel = panel.new_panel(main_window)

    # Initially update the panel to show it
    panel.update_panels()
    curses.doupdate()

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break

        panel.update_panels()
        curses.doupdate()


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()
    run(stdscr)


# Start application
curses.wrapper(main)
