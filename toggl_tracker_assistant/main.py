import time
import tkinter as tk
import sys
from loguru import logger

from toggl_service import TogglAPI
from config import AppConfig

class ArgumentHandler:
    """Class to handle command-line arguments."""
    def __init__(self):
        if len(sys.argv) > 1:
            self.argument = " ".join(sys.argv[1:])  # Combine all arguments into a single string
        else:
            self.argument = "No arguments passed"

    def get_argument(self):
        return self.argument


class TogglUI:
    """Class to manage the UI of the application."""
    def __init__(self, argument_handler):
        self.argument_handler = argument_handler
        self.root = tk.Tk()
        self.root.title("Toggl Tracker Assistant")
        self.root.resizable(False, False)  # Disables window resizing (removes maximize button)

        # Argument label
        self.argument_label = tk.Label(self.root, text=f"Argument: {self.argument_handler.get_argument()}", font=("Helvetica", 14))
        self.argument_label.pack(pady=(20, 5))

        # Description label
        self.description_label = tk.Label(self.root, text="Enter Description:", font=("Helvetica", 14))
        self.description_label.pack(pady=(20, 5))

        # Description entry
        self.description_entry = tk.Entry(self.root, width=30, font=("Helvetica", 14), validatecommand=self.check_text, validate="focusout")
        self.description_entry.pack(pady=(0, 20))

        # Start button
        self.start_button = tk.Button(
            self.root,
            text="Start",
            command=self.start,
            bg="green",         # Background color
            fg="white",         # Text color
            padx=40,            # Increased padding in x direction to make the button wider
            pady=20             # Increased padding in y direction to make the button taller
        )
        self.start_button.config(font=("Helvetica", 24, "bold"))  # Increased font size for better visibility
        self.start_button.pack(pady=20)

        # Output label
        self.output_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.output_label.pack(pady=(10, 20))

    def start(self):
        description = self.description_entry.get()
        if len(description) > 20:
            description = description[:20] + "..."
        self.output_label.config(text=f"Start button clicked with description: {description}")

    def check_text(self):
        description = self.description_entry.get()
        if len(description) > 20:
            return False
        return True

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()


if __name__ == "__main__":

    app_config = AppConfig()
    toggl_service = TogglAPI(api_key=app_config.TOGGL_API_KEY, workspace_id=app_config.TOGGL_WORKSPACE)

    # toggl_service.start_entry("Creating Quick Toggle APP")
    logger.info(f"Started a new track: {toggl_service.start_entry("New start test").id}")
    time.sleep(10)
    logger.info(f"Stopped a new track: {toggl_service.stop_running_entry().id}")

    projects_list = toggl_service.get_projects()
    logger.info(f"Get Projects: {[item.name for item in projects_list]}")

    # # Create the argument handler
    # argument_handler = ArgumentHandler()

    # # Create and run the UI
    # app = TogglUI(argument_handler)
    # app.run()
