import curses
import os
import pickle
from typing import List

from activity import Activity
from log import Log
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
ACT_CREATED = "Activity Created"
ACT_ADDED = "' has been added to your activities."
LOG_DATA_FOR = "Log data for "
DURATION_PROMPT = "Duration (minutes): "
ENGAGEMENT_PROMPT = "Engagement (0-5): "
ACT_LOGGED = "Activity logged"
ACTIVITY_LABEL = "Activity: "
DURATION_LABEL = "Duration: "
DURATION_UNIT = " minutes"
ENGAGEMENT_LABEL = "Engagement: "


activities: List[Activity] = []
logs: List[Log] = []
SAVE_FILE = "data.pkl"


def save_data():
    with open(SAVE_FILE, "wb") as f:
        pickle.dump((activities, logs), f)


def load_data():
    global activities, logs
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            activities, logs = pickle.load(f)
    else:
        activities, logs = [], []


def log_time_menu(window: Window, stdscr):
    current_row = 0
    draw_title_menu(window, stdscr)

    def print_menu(stdscr, selected_row_idx):
        window.clear()
        if len(activities) == 0:
            window.add_text(5, 8, NO_ACT_STARTED)
        else:
            for idx, activity in enumerate(activities):
                if idx == selected_row_idx:
                    window.startColoring(1)
                    window.window.addstr(idx + 6, 8, "> " + activity.name)
                    window.stopColoring(1)
                else:
                    window.window.addstr(idx + 6, 8, activity.name)

        draw_logit_menu(window, stdscr)
        window.add_text(35, 8, "Create new activity (press 'n')")
        window.add_text(36, 8, "Go to main menu (press 'x')")

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
            break

        print_menu(stdscr, current_row)


def isEmptyString(string: str) -> bool:
    return string == ""


def create_log_menu(window: Window, stdscr):
    window.emptyOut()
    window.add_title(2, 4, "Create a New Log")
    enable_input()

    log_name = window.getInputWprompt("Create Log", "Enter Log Name: ", MAX_CHARS)
    if isEmptyString(log_name):
        return
    duration = window.getInputWprompt("Create Log", "Duration (minutes): ", MAX_CHARS)
    if isEmptyString(duration):
        return
    engagement = window.getInputWprompt("Create Log", "Engagement (0-5): ", MAX_CHARS)
    if isEmptyString(engagement):
        return

    window.emptyOut()
    window.add_title(2, 4, "Confirm Log Creation")
    window.add_text(4, 6, f"Name: {log_name}")
    window.add_text(5, 8, f"Duration: {duration} minutes")
    window.add_text(6, 8, f"Engagement: {engagement}")
    window.add_text(35, 8, "Create this log? (y/n)")
    disable_input()

    while True:
        key = stdscr.getch()
        if key in [ord("y"), ord("Y")]:
            new_log = Log(log_name, int(duration), int(engagement))
            logs.append(new_log)
            add_log_to_activity_menu(window, stdscr, new_log)
            break
        elif key in [ord("n"), ord("N")]:
            break


def add_log_to_activity_menu(window: Window, stdscr, log: Log):
    if not activities:
        window.emptyOut()
        window.add_text(4, 6, "No activities available. Log saved without association.")
        window.add_text(35, 8, "Press any key to continue...")
        stdscr.getch()
        return

    current_row = 0
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Add Log to Activity")
        window.add_text(
            4, 6, "Select an activity or press 'q' to keep log independent:"
        )
        for idx, activity in enumerate(activities):
            if idx == current_row:
                window.startColoring(1)
                window.add_text(idx + 5, 8, f"> {activity.name}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 5, 8, f"  {activity.name}")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(activities) - 1:
            current_row += 1
        elif key == ord("\n"):
            activities[current_row].add_log(log)
            window.emptyOut()
            window.add_text(4, 6, f"Log added to '{activities[current_row].name}'")
            window.add_text(35, 8, "Press any key to continue...")
            stdscr.getch()
            break
        elif key == ord("q"):
            break


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
    enable_input()

    activity_name = window.getInputWprompt(CR_NEW_ACT, ENTR_ACT_NAME, MAX_CHARS)

    if activity_name:
        # Add activity to the list
        activities.append(Activity(activity_name))

        # Show confirmation
        window.emptyOut()
        window.add_title(2, 4, ACT_CREATED)
        window.add_text(4, 6, f"'{activity_name}" + ACT_ADDED)
        window.add_text(36, 8, KEY_FOR_CONTINUE)

    disable_input()
    stdscr.getch()  # Wait for user input before returning


def log_activity_menu(window: Window, stdscr, activity: Activity):
    window.emptyOut()
    enable_input()

    duration = window.getInputWprompt(
        LOG_DATA_FOR + activity.__str__(), DURATION_PROMPT, MAX_CHARS
    )

    # Prompt for engagement, need to add function for window to do more than one prompt.
    window.add_text(5, 8, ENGAGEMENT_PROMPT)
    window.window.move(6, 8)
    engagement = window.getInput(MAX_CHARS)

    activity.add_log(duration)

    # Log confirmation
    window.emptyOut()
    window.add_title(2, 4, ACT_LOGGED)
    window.add_text(4, 6, f"{ACTIVITY_LABEL + activity.__str__()}")
    window.add_text(5, 8, f"{DURATION_LABEL + duration + DURATION_UNIT}")
    window.window.addstr(6, 8, f"{ENGAGEMENT_LABEL + engagement}")
    window.add_text(36, 8, KEY_FOR_CONTINUE)

    disable_input()
    stdscr.getch()


def logs_menu(window: Window, stdscr):
    window.emptyOut()
    window.add_title(2, 4, "Logs")

    if not logs:
        window.add_text(4, 6, "No Logs Created")
        window.add_text(
            window.height - 3, 6, "Press any key to continue...", attribute=curses.A_DIM
        )
        window.refresh()
        stdscr.getch()
        return

    # Calculate dimensions for split screen
    left_width = window.width // 2
    right_width = window.width - left_width - 1
    content_height = window.height - 6  # Accounting for title and instructions

    current_row = 0

    def draw_logs_list(selected_idx):
        for idx, log in enumerate(logs):
            if idx < content_height:
                if idx == selected_idx:
                    window.startColoring(1)
                    window.add_text(idx + 4, 3, f"> {log.name[:left_width-4]}")
                    window.stopColoring(1)
                else:
                    window.add_text(idx + 4, 3, f"  {log.name[:left_width-4]}")

    def draw_log_details(log):
        window.add_text(4, left_width + 2, f"Name: {log.name}", wrap=True)
        window.add_text(
            5,
            left_width + 2,
            f"Activity: {log.activity.name if log.activity else 'No Activity'}",
            wrap=True,
        )
        window.add_text(6, left_width + 2, f"Duration: {log.duration} minutes")
        window.add_text(7, left_width + 2, f"Engagement: {log.engagement}")
        # TODO: add or adjust details for logs

    # Draw vertical line to split the screen
    for y in range(4, window.height - 1):
        window.add_text(y, left_width, "│")

    window.add_text(
        window.height - 2,
        2,
        "↑↓: Navigate  Enter: Select  q: Quit",
        attribute=curses.A_DIM,
    )

    while True:
        window.clear()
        window.add_border()
        window.add_title(2, 4, "Logs")

        # Redraw the vertical line
        for y in range(4, window.height - 3):
            window.add_text(y, left_width, "│")

        draw_logs_list(current_row)
        draw_log_details(logs[current_row])

        window.add_text(
            window.height - 3,
            4,
            "↑↓: Navigate  Enter: Select  q: Quit",
            attribute=curses.A_DIM,
        )
        window.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < min(
            len(logs) - 1, content_height - 1
        ):
            current_row += 1
        elif key == ord("\n"):
            # TODO: add functionality for when logs are selected
            pass
        elif key == ord("q"):
            break

    window.clear()
    window.refresh()


def draw_menu(window: Window, stdscr, title, message):
    window.center_window(stdscr)
    window.add_title(2, 4, title)
    window.add_border()
    window.add_text(4, 6, message)


def draw_title_menu(window, stdscr):
    draw_menu(window, stdscr, TITLE_WELCOME, MSG_SELECT_OPTIONS)


def draw_logit_menu(window, stdscr):
    draw_menu(window, stdscr, TITLE_CREATE_LOG, MSG_SELECT_ACTIVITY)


def manage_activities_menu(window: Window, stdscr):
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Manage Activities")
        window.add_text(4, 6, "1. Create new activity")
        window.add_text(5, 6, "2. View/Edit activities")
        window.add_text(6, 6, "3. Delete activity")
        window.add_text(7, 6, "4. Back to main menu")

        key = stdscr.getch()
        if key == ord("1"):
            activity_creation_menu(window, stdscr)
        elif key == ord("2"):
            view_edit_activities_menu(window, stdscr)
        elif key == ord("3"):
            delete_activity_menu(window, stdscr)
        elif key == ord("4") or key == ord("q"):
            break


def delete_activity_menu(window: Window, stdscr):
    if not activities:
        window.emptyOut()
        window.add_text(4, 6, "No activities to delete.")
        window.add_text(35, 8, "Press any key to continue...")
        stdscr.getch()
        return

    current_row = 0
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Delete Activity")
        for idx, activity in enumerate(activities):
            if idx == current_row:
                window.startColoring(1)
                window.add_text(idx + 4, 6, f"> {activity.name}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 4, 6, f"  {activity.name}")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(activities) - 1:
            current_row += 1
        elif key == ord("\n"):
            window.emptyOut()
            window.add_title(2, 4, "Deleting activity")
            window.add_text(
                4,
                6,
                f"Are you sure you want to delete '{activities[current_row].name}'? (y/n)",
            )
            confirm = stdscr.getch()
            if confirm in [ord("y"), ord("Y")]:
                del activities[current_row]
                window.add_text(35, 8, "Activity deleted. Press any key to continue...")
                stdscr.getch()
                break
        elif key == ord("q"):
            break


def view_edit_activities_menu(window: Window, stdscr):
    # Need to add the view/edit functionality
    pass  # Placeholder for now


def main_menu(stdscr):
    title_window = Window(40, 120)
    draw_title_menu(title_window, stdscr)
    curses.curs_set(0)
    menu = ["Create Log", "View Logs", "Manage Activities", "Exit"]
    current_row = 0

    def print_menu(selected_row_idx, highlight=False):
        title_window.clear()
        height, width = title_window.window.getmaxyx()
        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                if highlight:
                    title_window.window.attron(curses.A_REVERSE)
                title_window.startColoring(1)
                title_window.window.addstr(y, x, row)
                if highlight:
                    title_window.window.attroff(curses.A_REVERSE)
                title_window.stopColoring(1)
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
            # Blink effect
            for _ in range(1):  # Blink n times
                print_menu(current_row, highlight=True)
                curses.napms(40)  # Wait for 40 milliseconds
                print_menu(current_row, highlight=False)
                curses.napms(80)  # Wait for 80 milliseconds

            if current_row == 0:
                create_log_menu(title_window, stdscr)
            elif current_row == 1:
                logs_menu(title_window, stdscr)
            elif current_row == 2:
                manage_activities_menu(title_window, stdscr)
            elif current_row == 3:
                break
        elif key == ord("q"):
            break
        print_menu(current_row)


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()
    load_data()
    main_menu(stdscr)
    save_data()


# Start application
curses.wrapper(main)
