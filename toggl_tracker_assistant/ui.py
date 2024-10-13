import tkinter as tk
from tkinter import ttk
from pydantic import BaseModel

class UserInput(BaseModel):
    """Class to represent the user input."""
    project: str
    description: str

class TogglUI:
    """Class to manage the UI of the application."""
    def __init__(self, project_names):
        self.root = tk.Tk()
        self.root.title("Toggl Tracker Assistant")
        self.root.resizable(False, False)  # Disables window resizing (removes maximize button)

        # Project selection label
        self.project_label = tk.Label(self.root, text="Select Project:", font=("Helvetica", 14))
        self.project_label.pack(pady=(20, 5))

        # Project dropdown
        self.selected_project = tk.StringVar(value=project_names[0])
        self.project_dropdown = ttk.Combobox(self.root, textvariable=self.selected_project, values=project_names, state='readonly', font=("Helvetica", 14))
        self.project_dropdown.pack(pady=(0, 20))

        # Description label
        self.description_label = tk.Label(self.root, text="Enter Description:", font=("Helvetica", 14))
        self.description_label.pack(pady=(0, 5))

        # Description entry
        self.description_entry = ttk.Entry(self.root, width=30, font=("Helvetica", 14))
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

        # Variables to store user input
        self.project = None
        self.description = None

    def start(self):
        self.project = self.selected_project.get()
        self.description = self.description_entry.get()
        
        if len(self.description) > 20:
            self.description = self.description[:20] + "..."
        
        if not self.project:
            self.output_label.config(text="Please select a project.")
        else:
            self.output_label.config(text=f"Project: {self.project}\nDescription: {self.description}")
            self.root.quit()

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()
        return UserInput(project=self.project, description=self.description)

# # List of projects to populate the dropdown
# projects = ["Project A", "Project B", "Project C"]

# # Create and run the UI
# app = TogglUI(projects)
# project, description = app.run()
# print(f"Selected Project: {project}")
# print(f"Entered Description: {description}")