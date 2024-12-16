import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui

# Global variable to control the key pressing thread
running = False

def start_key_presser():
    global running
    running = True
    interval = interval_var.get()

    # Validate interval
    try:
        interval = float(interval)
    except ValueError:
        status_label.config(text="Invalid interval! Enter a number.", foreground="red")
        return

    # Get the list of keys to press
    keys_to_press = key_listbox.get(0, tk.END)
    if not keys_to_press:
        status_label.config(text="No keys selected!", foreground="red")
        return

    # Background thread for key pressing
    def press_keys():
        while running:
            for key in keys_to_press:
                pyautogui.press(key)  # Simulate key press
                if not running:
                    break
                time.sleep(interval)
        status_label.config(text="Stopped.", foreground="green")

    threading.Thread(target=press_keys, daemon=True).start()
    status_label.config(text="Running...", foreground="green")

def stop_key_presser():
    global running
    running = False
    status_label.config(text="Stopping...", foreground="orange")

def add_key():
    key = key_var.get()
    if key and key not in key_listbox.get(0, tk.END):
        key_listbox.insert(tk.END, key)
        status_label.config(text=f"Added key: {key}", foreground="blue")
    else:
        status_label.config(text="Key already added or invalid!", foreground="red")

def remove_key():
    selected_indices = key_listbox.curselection()
    if not selected_indices:
        status_label.config(text="No key selected to remove!", foreground="red")
        return
    for index in reversed(selected_indices):  # Remove from bottom up
        key_listbox.delete(index)
    status_label.config(text="Removed selected keys.", foreground="blue")

# GUI setup
root = tk.Tk()
root.title("Auto Key Presser")
root.geometry("500x400")
root.resizable(True, True)

# Apply modern style
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TCombobox", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 10))

# Main frame
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Key selection frame
key_frame = ttk.LabelFrame(main_frame, text="Key Selection", padding="10 10 10 10")
key_frame.pack(fill=tk.X, padx=10, pady=5)

key_var = tk.StringVar(value="a")
keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "space", "enter"]
key_dropdown = ttk.Combobox(key_frame, values=keys, textvariable=key_var, state="readonly")
key_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

add_button = ttk.Button(key_frame, text="Add Key", command=add_key)
add_button.grid(row=0, column=1, padx=5, pady=5)

remove_button = ttk.Button(key_frame, text="Remove Selected Key", command=remove_key)
remove_button.grid(row=0, column=2, padx=5, pady=5)

# Key list frame
list_frame = ttk.LabelFrame(main_frame, text="Keys to Press", padding="10 10 10 10")
list_frame.pack(fill=tk.X, padx=10, pady=5)

key_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10, font=("Arial", 10))
key_listbox.pack(fill=tk.X, padx=5, pady=5)

# Interval frame
interval_frame = ttk.LabelFrame(main_frame, text="Interval (seconds)", padding="10 10 10 10")
interval_frame.pack(fill=tk.X, padx=10, pady=5)

interval_var = tk.StringVar(value="1")
interval_entry = ttk.Entry(interval_frame, textvariable=interval_var)
interval_entry.pack(fill=tk.X, padx=5, pady=5)

# Buttons frame
button_frame = ttk.Frame(main_frame, padding="10 10 10 10")
button_frame.pack(fill=tk.X, padx=10, pady=5)

start_button = ttk.Button(button_frame, text="Start", command=start_key_presser)
start_button.grid(row=0, column=0, padx=5)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_key_presser)
stop_button.grid(row=0, column=1, padx=5)

# Status label
status_label = ttk.Label(main_frame, text="Idle", foreground="blue", anchor="center")
status_label.pack(fill=tk.X, padx=10, pady=10)

# Run the GUI loop
root.mainloop()
