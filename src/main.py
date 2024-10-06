import tkinter as tk

def start():
    print("Start button clicked")

root = tk.Tk()
root.title("Toggl Tracker Assistant")
start_button = tk.Button(root, text="Start", command=start)
start_button.pack()
root.mainloop()
