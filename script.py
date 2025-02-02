import curses
import os
import pickle
import time
from typing import List

from tag import Tag
from log import Log
from task import Task
from window_utils import Window

# Constants for menu titles and messages
TITLE_WELCOME = "Welcome to LogIt"
TITLE_CREATE_LOG = "Create a log"
MSG_SELECT_tag = "What tag to create a log for?"
MSG_SELECT_OPTIONS = "Please select from the following: "
CR_NEW_ACT = "Create New tag"
ENTR_ACT_NAME = "Enter tag Name: "
UTF8 = "utf-8"
MAX_CHARS = 30
NO_TAG_STARTED = "[No Tags Started]"
KEY_FOR_CONTINUE = "Press any key to continue..."
ACT_CREATED = "tag Created"
ACT_ADDED = "' has been added to your tags."
LOG_DATA_FOR = "Log data for "
DURATION_PROMPT = "Duration (minutes): "
ENGAGEMENT_PROMPT = "Engagement (0-5): "
ACT_LOGGED = "tag logged"
tag_LABEL = "tag: "
DURATION_LABEL = "Duration: "
DURATION_UNIT = " minutes"
ENGAGEMENT_LABEL = "Engagement: "

tags: List[Tag] = []  # TODO: Move to DataManager
tasks: List[Task] = []
logs: List[Log] = []  # TODO: Move to DataManager

SAVE_FILE = "data.pkl"  # TODO: Move to DataManager


def save_data():  # TODO: Move to DataManager
    with open(SAVE_FILE, "wb") as f:
        pickle.dump((tags, logs, tasks), f)


def load_data():  # TODO: Move to DataManager
    global tags, logs, tasks
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            tags, logs, tasks = pickle.load(f)
    else:
        tags, logs, tasks = [], [], []


def log_time_menu(window: Window, stdscr):
    current_row = 0
    draw_title_menu(window, stdscr)

    def print_menu(stdscr, selected_row_idx):
        window.clear()
        if len(tags) == 0:
            window.add_text(5, 8, NO_TAG_STARTED)
        else:
            for idx, tag in enumerate(tags):
                if idx == selected_row_idx:
                    window.startColoring(1)
                    window.window.addstr(idx + 6, 8, "> " + tag.name)
                    window.stopColoring(1)
                else:
                    window.window.addstr(idx + 6, 8, tag.name)

        draw_logit_menu(window, stdscr)
        window.add_text(35, 8, "Create new tag (press 'n')")
        window.add_text(36, 8, "Go to main menu (press 'x')")

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tags):
            current_row += 1
        elif key == ord("\n") and current_row < len(tags):
            log_tag_menu(window, stdscr, tags[current_row])
        elif key == ord("n"):
            tag_creation_menu(window, stdscr)
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

    log_name = window.getInputWithPrompt("Create Log", "Enter Log Name: ", MAX_CHARS)
    if isEmptyString(log_name):
        return
    duration = window.getInputWithPrompt(
        "Create Log", "Duration (minutes): ", MAX_CHARS
    )
    if isEmptyString(duration):
        return
    engagement = window.getInputWithPrompt(
        "Create Log", "Engagement (0-5): ", MAX_CHARS
    )
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
            add_log_to_tag_menu(window, stdscr, new_log)
            break
        elif key in [ord("n"), ord("N")]:
            break


def add_log_to_tag_menu(window: Window, stdscr, log: Log):
    if not tags:
        window.emptyOut()
        window.add_text(4, 6, "No tags available. Log saved without association.")
        window.add_text(35, 8, "Press any key to continue...")
        stdscr.getch()
        return

    current_row = 0
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Add Log to tag")
        window.add_text(4, 6, "Select an tag or press 'q' to keep log independent:")
        for idx, tag in enumerate(tags):
            if idx == current_row:
                window.startColoring(1)
                window.add_text(idx + 5, 8, f"> {tag.name}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 5, 8, f"  {tag.name}")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tags) - 1:
            current_row += 1
        elif key == ord("\n"):
            tags[current_row].add_log(log)
            window.emptyOut()
            window.add_text(4, 6, f"Log added to '{tags[current_row].name}'")
            window.add_text(35, 8, "Press any key to continue...")
            stdscr.getch()
            break
        elif key == ord("q"):
            break


def enable_input():  # TODO: Create util class for this
    """Enable echo and show cursor."""
    curses.echo()
    curses.curs_set(1)


def disable_input():  # TODO: Create util class for this
    """Disable echo and hide cursor."""
    curses.curs_set(0)
    curses.noecho()


def tag_creation_menu(window: Window, stdscr):
    window.emptyOut()
    enable_input()

    tag_name = window.getInputWithPrompt(CR_NEW_ACT, ENTR_ACT_NAME, MAX_CHARS)

    if tag_name:
        # Add tag to the list
        tags.append(Tag(tag_name))

        # Show confirmation
        window.emptyOut()
        window.add_title(2, 4, ACT_CREATED)
        window.add_text(4, 6, f"'{tag_name}" + ACT_ADDED)
        window.add_text(36, 8, KEY_FOR_CONTINUE)

    disable_input()
    stdscr.getch()  # Wait for user input before returning


def log_tag_menu(window: Window, stdscr, tag: Tag):
    window.emptyOut()
    enable_input()

    duration = window.getInputWithPrompt(
        LOG_DATA_FOR + tag.__str__(), DURATION_PROMPT, MAX_CHARS
    )

    # Prompt for engagement, need to add function for window to do more than one prompt.
    window.add_text(5, 8, ENGAGEMENT_PROMPT)
    window.window.move(6, 8)
    engagement = window.getInput(MAX_CHARS)

    tag.add_log(duration)

    # Log confirmation
    window.emptyOut()
    window.add_title(2, 4, ACT_LOGGED)
    window.add_text(4, 6, f"{tag_LABEL + tag.__str__()}")
    window.add_text(5, 8, f"{DURATION_LABEL + duration + DURATION_UNIT}")
    window.window.addstr(6, 8, f"{ENGAGEMENT_LABEL + engagement}")
    window.add_text(36, 8, KEY_FOR_CONTINUE)

    disable_input()
    stdscr.getch()


def ifLogsEmpty(window: Window, stdscr):
    if not logs:
        window.add_text(4, 6, "No Logs Created")
        window.add_text(
            window.height - 3, 6, "Press any key to continue...", attribute=curses.A_DIM
        )
        window.refresh()
        stdscr.getch()
        return


def delete_log(log, window: Window, stdscr):
    if confirmation_menu(
        window, stdscr, f"Are you sure you want to delete the log: {log.name}?"
    ):
        logs.remove(log)
        window.clear()
        window.add_border()
        window.add_text(2, 4, "Log deleted successfully!", attribute=curses.A_BOLD)
        window.add_text(4, 4, "Press any key to continue...", attribute=curses.A_DIM)
        window.refresh()
        stdscr.getch()
        return True
    else:
        window.clear()
        window.add_border()
        window.add_text(2, 4, "Deletion cancelled", attribute=curses.A_BOLD)
        window.add_text(4, 4, "Press any key to continue...", attribute=curses.A_DIM)
        window.refresh()
        stdscr.getch()
        return False


def assign_log_to_tag(log, window: Window, stdscr):
    def tag_menu():
        selected = 0
        while True:
            window.clear()
            window.add_border()
            window.add_title(2, 4, "Select an tag to assign the log to:")
            for idx, tag in enumerate(tags):
                if idx == selected:
                    window.startColoring(1)
                    window.add_text(idx + 4, 3, f"> {tag.name}")
                    window.stopColoring(1)
                else:
                    window.add_text(idx + 4, 3, f"  {tag.name}")
            window.add_text(
                window.height - 2,
                2,
                "↑↓: Navigate  Enter: Select  q: Cancel",
                attribute=curses.A_DIM,
            )
            window.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(tags) - 1:
                selected += 1
            elif key == ord("\n"):
                return tags[selected]
            elif key == ord("q"):
                return None

    selected_tag = tag_menu()
    if selected_tag:
        if confirmation_menu(
            window,
            stdscr,
            f"Assign log '{log.name}' to tag '{selected_tag.name}'?",
        ):
            log.add_to_tag(selected_tag)
            window.clear()
            window.add_border()
            window.add_text(2, 4, "Log assigned successfully!", attribute=curses.A_BOLD)
            window.add_text(
                4, 4, "Press any key to continue...", attribute=curses.A_DIM
            )
            window.refresh()
            stdscr.getch()
        else:
            window.clear()
            window.add_border()
            window.add_text(2, 4, "Assignment cancelled", attribute=curses.A_BOLD)
            window.add_text(
                4, 4, "Press any key to continue...", attribute=curses.A_DIM
            )
            window.refresh()
            stdscr.getch()


def edit_log(log, window, stdscr):
    def edit_menu():
        options = ["Name", "Duration", "Engagement", "Cancel"]
        selected = 0
        while True:
            window.clear()
            window.add_border()
            window.add_title(2, 4, f"Edit log: {log.name}")
            for idx, option in enumerate(options):
                if idx == selected:
                    window.startColoring(1)
                    window.add_text(idx + 4, 3, f"> {option}")
                    window.stopColoring(1)
                else:
                    window.add_text(idx + 4, 3, f"  {option}")
            window.add_text(
                window.height - 2,
                2,
                "↑↓: Navigate  Enter: Select",
                attribute=curses.A_DIM,
            )
            window.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(options) - 1:
                selected += 1
            elif key == ord("\n"):
                return options[selected]

    def get_input(prompt):
        curses.echo()
        window.clear()
        window.add_border()
        window.add_text(2, 4, prompt)
        window.refresh()
        input_str = stdscr.getstr(4, 4, 30).decode(UTF8)
        curses.noecho()
        return input_str

    while True:
        choice = edit_menu()
        if choice == "Name":
            new_name = get_input("Enter new name:")
            if new_name:
                log.name = new_name
        elif choice == "Duration":
            new_duration = get_input("Enter new duration (minutes):")
            if new_duration.isdigit():
                log.duration = int(new_duration)
        elif choice == "Engagement":
            new_engagement = get_input("Enter new engagement (0-5):")
            if new_engagement.isdigit() and 0 <= int(new_engagement) <= 5:
                log.engagement = int(new_engagement)
        elif choice == "Cancel":
            break

        window.clear()
        window.add_border()
        window.add_text(2, 4, "Log updated successfully!", attribute=curses.A_BOLD)
        window.add_text(4, 4, "Press any key to continue...", attribute=curses.A_DIM)
        window.refresh()
        stdscr.getch()


# Helper function for confirmation prompts
def confirmation_menu(window, stdscr, prompt):
    options = ["Yes", "No"]
    selected = 0
    while True:
        window.clear()
        window.add_border()
        window.add_title(2, 4, prompt)
        for idx, option in enumerate(options):
            if idx == selected:
                window.startColoring(1)
                window.add_text(idx + 4, 3, f"> {option}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 4, 3, f"  {option}")
        window.add_text(
            window.height - 2, 2, "↑↓: Navigate  Enter: Select", attribute=curses.A_DIM
        )
        window.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("\n"):
            return options[selected] == "Yes"


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

    left_width = window.width // 2
    content_height = window.height - 6
    current_row = 0

    def draw_logs_list(selected_idx):
        for idx, log in enumerate(logs):
            if idx < content_height:
                if idx == selected_idx:
                    window.startColoring(1)
                    window.add_text(idx + 4, 3, f"> {log.name[: left_width - 4]}")
                    window.stopColoring(1)
                else:
                    window.add_text(idx + 4, 3, f"  {log.name[: left_width - 4]}")

    def draw_log_details(log):
        window.add_text(4, left_width + 2, f"Name: {log.name}", wrap=True)
        window.add_text(
            5,
            left_width + 2,
            f"tag: {log.tag.name if log.tag else 'No tag'}",
            wrap=True,
        )
        window.add_text(6, left_width + 2, f"Duration: {log.duration} minutes")
        window.add_text(7, left_width + 2, f"Engagement: {log.engagement}")

    def blink_selection(row):
        for _ in range(1):  # Blink twice
            window.startColoring(1)
            window.window.attron(curses.A_REVERSE)
            window.add_text(row + 4, 3, f"> {logs[row].name[: left_width - 4]}")
            window.window.attroff(curses.A_REVERSE)
            window.stopColoring(1)
            window.refresh()
            curses.napms(40)
            window.add_text(row + 4, 3, f"  {logs[row].name[: left_width - 4]}")
            window.refresh()
            curses.napms(80)

    def action_menu(log):
        options = [
            "Delete the Log",
            "Assign the Log to an tag",
            "Edit the log",
            "Back",
        ]
        selected = 0
        while True:
            window.clear()
            window.add_border()
            window.add_title(2, 4, f"Actions for: {log.name}")
            for idx, option in enumerate(options):
                if idx == selected:
                    window.startColoring(1)
                    window.add_text(idx + 4, 3, f"> {option}")
                    window.stopColoring(1)
                else:
                    window.add_text(idx + 4, 3, f"  {option}")
            window.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(options) - 1:
                selected += 1
            elif key == ord("\n"):
                if selected == 0:
                    if delete_log(log, window, stdscr):
                        return True  # log deleated
                elif selected == 1:
                    assign_log_to_tag(log, window, stdscr)
                elif selected == 2:
                    edit_log(log, window, stdscr)
                else:
                    break
            window.refresh()
        return False  # log not deleted

    while True:
        if not logs:
            window.clear()
            window.add_border()
            window.add_text(4, 6, "No logs remaining")
            window.add_text(
                window.height - 3,
                6,
                "Press any key to continue...",
                attribute=curses.A_DIM,
            )
            window.refresh()
            stdscr.getch()
            break

        if current_row >= len(logs):
            current_row = len(logs) - 1

        window.clear()
        window.add_border()
        window.add_title(2, 4, "Logs")
        for y in range(4, window.height - 3):
            window.add_text(y, left_width, "│")
        draw_logs_list(current_row)
        draw_log_details(logs[current_row])
        window.add_text(
            window.height - 2,
            2,
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
            blink_selection(current_row)
            if action_menu(logs[current_row]):  # If log was deleted
                continue  # skip the rest of the loop and start over
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
    draw_menu(window, stdscr, TITLE_CREATE_LOG, MSG_SELECT_tag)


def manage_tags_menu(window: Window, stdscr):
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Manage tags")
        window.add_text(4, 6, "1. Create new tag")
        window.add_text(5, 6, "2. View/Edit tags")
        window.add_text(6, 6, "3. Delete tag")
        window.add_text(7, 6, "4. Back to main menu")

        key = stdscr.getch()
        if key == ord("1"):
            tag_creation_menu(window, stdscr)
        elif key == ord("2"):
            view_edit_tags_menu(window, stdscr)
        elif key == ord("3"):
            delete_tag_menu(window, stdscr)
        elif key == ord("4") or key == ord("q"):
            break


def delete_tag_menu(window: Window, stdscr):
    if not tags:
        window.emptyOut()
        window.add_text(4, 6, "No tags to delete.")
        window.add_text(35, 8, "Press any key to continue...")
        stdscr.getch()
        return

    current_row = 0
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Delete tag")
        for idx, tag in enumerate(tags):
            if idx == current_row:
                window.startColoring(1)
                window.add_text(idx + 4, 6, f"> {tag.name}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 4, 6, f"  {tag.name}")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tags) - 1:
            current_row += 1
        elif key == ord("\n"):
            window.emptyOut()
            window.add_title(2, 4, "Deleting tag")
            window.add_text(
                4,
                6,
                f"Are you sure you want to delete '{tags[current_row].name}'? (y/n)",
            )
            confirm = stdscr.getch()
            if confirm in [ord("y"), ord("Y")]:
                del tags[current_row]
                window.add_text(35, 8, "tag deleted. Press any key to continue...")
                stdscr.getch()
                break
        elif key == ord("q"):
            break


def view_edit_tags_menu(window: Window, stdscr):
    # Need to add the view/edit functionality
    pass  # Placeholder for now


def manage_tasks_menu(window: Window, stdscr):
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Manage Tasks")
        window.add_text(4, 6, "1. Create new task")
        window.add_text(5, 6, "2. Start/Pause/Resume/Stop a task")
        window.add_text(6, 6, "3. Back to main menu")

        key = stdscr.getch()
        if key == ord("1"):
            create_task(window, stdscr)
        elif key == ord("2"):
            tasks_screen(window, stdscr)
        elif key in [ord("3"), ord("q")]:
            break


def create_task(window: Window, stdscr):
    window.emptyOut()
    enable_input()

    task_name = window.getInputWithPrompt("New Task", "Enter Task Name: ", MAX_CHARS)
    if not task_name:
        disable_input()
        return

    time_goal_str = window.getInputWithPrompt(
        "New Task", "Enter goal (minutes): ", MAX_CHARS
    )
    if not time_goal_str or not time_goal_str.isdigit():
        disable_input()
        return

    new_task = Task(task_name)
    new_task.time_goal_minutes = int(time_goal_str)

    tasks.append(new_task)
    # show confirmation, etc. (TODO)

    disable_input()


def tasks_screen(window: Window, stdscr):
    if not tasks:
        window.emptyOut()
        window.add_text(4, 6, "No tasks available.")
        window.add_text(35, 8, "Press any key to continue...")
        stdscr.getch()
        return

    current_row = 0
    while True:
        window.emptyOut()
        window.add_title(2, 4, "Select a Task to work on (Enter) or 'q' to return")

        for idx, t in enumerate(tasks):
            # progress in percentage
            if t.time_goal_minutes > 0:
                pct = (t.total_seconds_worked / (t.time_goal_minutes * 60)) * 100
            else:
                pct = 0

            display_status = "(paused)" if t.is_paused else "(running)"
            row_text = f"{t.name} {display_status}"

            if idx == current_row:
                window.startColoring(1)
                window.add_text(idx + 4, 6, f"> {row_text}")
                window.stopColoring(1)
            else:
                window.add_text(idx + 4, 6, f"  {row_text}")

            # Draw progress bar on the right at X=30 for now
            draw_progress_bar(window, idx + 4, 30, 20, pct)

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tasks) - 1:
            current_row += 1
        elif key == ord("\n"):
            run_task_timer(window, stdscr, tasks[current_row])
        elif key == ord("q"):
            break


def draw_progress_bar(window: Window, y: int, x: int, width: int, percentage: float):
    """
    Draw a progress bar at (y, x) in the given window,
    with 'width' (characters) of total space.
    percentage should be 0 <= percentage <= 100.
    """
    # Ensure percentage is clamped
    pct = max(0, min(100, percentage))
    num_hashes = int((pct / 100) * width)
    bar = "[" + "#" * num_hashes + " " * (width - num_hashes) + "]"
    window.add_text(y, x, f"{bar} {pct:.1f}%")


def run_task_timer(window: Window, stdscr, task: Task):
    task.start()

    while True:
        window.emptyOut()
        window.add_title(2, 4, f"Working on: {task.name}")

        total_elapsed = task.total_seconds_worked
        if not task.is_paused:
            total_elapsed += time.time() - task.start_time

        # Convert to min/sec
        minutes = int(total_elapsed // 60)
        seconds = int(total_elapsed % 60)

        # Show "00:01:12 / 00:20:00" style
        goal_mins = task.time_goal_minutes
        time_str = f"{minutes:02d}:{seconds:02d}"
        goal_str = f"{goal_mins:02d}:00"  # for only tracking minute level goals

        window.add_text(4, 6, f"Time Elapsed: {time_str} / {goal_str}")

        # Show progress bar
        if goal_mins > 0:
            pct = (total_elapsed / (goal_mins * 60)) * 100
        else:
            pct = 0
        draw_progress_bar(window, 6, 6, 40, pct)

        status_msg = (
            "Press 'p' to pause" if not task.is_paused else "Press 'r' to resume"
        )
        window.add_text(8, 6, f"{status_msg}, 's' to stop")

        window.refresh()

        stdscr.nodelay(True)
        curses.napms(1000)
        key = stdscr.getch()
        stdscr.nodelay(False)

        if key == ord("p") and not task.is_paused:
            task.pause()
        elif key == ord("r") and task.is_paused:
            task.start()
        elif key == ord("s"):
            total_minutes = task.stop()
            create_log_from_task(window, stdscr, task, total_minutes)
            break


def create_log_from_task(window: Window, stdscr, task: Task, total_minutes: int):
    enable_input()
    engagement_str = window.getInputWithPrompt(
        "Stop Task", "Enter engagement (0-5): ", MAX_CHARS
    )
    disable_input()

    if not engagement_str:
        return

    new_log = Log(task.name, total_minutes, int(engagement_str))
    logs.append(new_log)

    add_log_to_tag_menu(window, stdscr, new_log)

    # Possibly reset the Task to re-use the same Task in the future
    # or we can remove it from `tasks` if it’s “complete" (still need to add a way to complete).
    # tasks.remove(task)
    window.emptyOut()
    window.add_text(4, 6, f"Task '{task.name}' has been converted to a log.")
    window.add_text(35, 8, KEY_FOR_CONTINUE)
    stdscr.getch()


def main_menu(stdscr):
    title_window: Window = Window(
        40, 120
    )  # Maybe title_window can be renamed for clarity
    draw_title_menu(title_window, stdscr)
    curses.curs_set(0)
    menu = [
        "Create Log",
        "View Logs",
        "Manage Tags",
        "Manage Tasks",
        "Exit",
    ]
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
                manage_tags_menu(title_window, stdscr)
            elif current_row == 3:
                manage_tasks_menu(title_window, stdscr)
            elif current_row == 4:
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
