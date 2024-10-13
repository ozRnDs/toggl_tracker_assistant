import tkinter as tk
from tkinter import ttk
from typing import List
from config import AppConfig

class TogglConfigUI:
    """Class to manage the UI of the application."""
    def __init__(self, project_names: List[str], current_config: AppConfig):
        self.root = tk.Tk()
        self.root.title("Toggl Tracker Configuration")
        self.root.resizable(False, False)  # Disables window resizing (removes maximize button)

        # Project selection label
        self.project_label = tk.Label(self.root, text="Select Projects:", font=("Helvetica", 14))
        self.project_label.pack(pady=(20, 5))

        # Project listbox for multiple selection
        project_names = [project.lower() for project in project_names]
        self.project_listbox = tk.Listbox(self.root, selectmode='multiple', font=("Helvetica", 14), height=6)
        for project in project_names:
            self.project_listbox.insert(tk.END, project)
        for project in current_config.PROJECTS_LIST:
            idx = project_names.index(project) if project.lower() in project_names else None
            if idx is not None:
                self.project_listbox.select_set(idx)
        self.project_listbox.pack(pady=(0, 20))

        # Workspace ID label
        self.workspace_label = tk.Label(self.root, text="Enter Workspace ID:", font=("Helvetica", 14))
        self.workspace_label.pack(pady=(0, 5))

        # Workspace ID entry
        self.workspace_entry = ttk.Entry(self.root, width=30, font=("Helvetica", 14))
        self.workspace_entry.insert(0, current_config.TOGGL_WORKSPACE)
        self.workspace_entry.pack(pady=(0, 20))

        # API Key label
        self.api_key_label = tk.Label(self.root, text="Enter API Key:", font=("Helvetica", 14))
        self.api_key_label.pack(pady=(0, 5))

        # API Key entry
        self.api_key_entry = ttk.Entry(self.root, width=30, font=("Helvetica", 14), show="*")
        self.api_key_entry.insert(0, current_config.TOGGL_API_KEY)
        self.api_key_entry.pack(pady=(0, 20))

        # Save button
        self.save_button = tk.Button(
            self.root,
            text="Save",
            command=self.save,
            bg="blue",         # Background color
            fg="white",        # Text color
            padx=40,            # Increased padding in x direction to make the button wider
            pady=20             # Increased padding in y direction to make the button taller
        )
        self.save_button.config(font=("Helvetica", 24, "bold"))  # Increased font size for better visibility
        self.save_button.pack(pady=20)

        # Output label
        self.output_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.output_label.pack(pady=(10, 20))

        # Variables to store user input
        self.projects = []
        self.description = None
        self.workspace_id = None
        self.api_key = None

    def save(self):
        selected_indices = self.project_listbox.curselection()
        self.projects = [self.project_listbox.get(i) for i in selected_indices]
        self.workspace_id = self.workspace_entry.get()
        self.api_key = self.api_key_entry.get()
        
        if not self.projects:
            self.output_label.config(text="Please select at least one project.")
        elif not self.workspace_id:
            self.output_label.config(text="Please enter a workspace ID.")
        elif not self.api_key:
            self.output_label.config(text="Please enter an API key.")
        else:
            self.output_label.config(text="Configuration saved successfully.")
            self.root.quit()

    def run(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()
        return AppConfig(TOGGL_WORKSPACE=self.workspace_id, TOGGL_API_KEY=self.api_key, PROJECTS_LIST=self.projects)