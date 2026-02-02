import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


# =========================
# Configuration / Style
# =========================

# ---- Fonts ----
DEFAULT_FONT = ("Segoe UI", 12)
TITLE_FONT   = ("Segoe UI", 12, "bold")
TEXT_FONT    = ("Consolas", 10)

# ---- Colors ----
BG_COLOR        = "#FFFFC8"
LABEL_COLOR     = "#333333"
LEFT_BG_COLOR   = "#FFE1E1" 
RIGHT_BG_COLOR  = "#FFE1C8"
LEFT_TEXT_COLOR = "#222222"
RIGHT_TEXT_COLOR = "#222222"


# =========================
# Core Logic
# =========================
def compare_filenames(folder1, folder2):
    """
    Compare filenames (non-recursive) between two folders.

    Returns:
        only_in_1 (set): files only in folder1
        only_in_2 (set): files only in folder2
    """
    files1 = {
        f for f in os.listdir(folder1)
        if os.path.isfile(os.path.join(folder1, f))
    }
    files2 = {
        f for f in os.listdir(folder2)
        if os.path.isfile(os.path.join(folder2, f))
    }
    return files1 - files2, files2 - files1


# =========================
# UI Helper Functions
# =========================
def select_folder(var):
    """Open folder selection dialog and update StringVar."""
    path = filedialog.askdirectory()
    if path:
        var.set(path)


def run_compare():
    """Validate input and update comparison results."""
    folder1 = folder1_var.get()
    folder2 = folder2_var.get()

    if not folder1 or not folder2:
        messagebox.showwarning(
            "Missing Input",
            "Please select both folders before comparing."
        )
        return

    try:
        only_in_1, only_in_2 = compare_filenames(folder1, folder2)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Reset result panels
    left_box.delete("1.0", tk.END)
    right_box.delete("1.0", tk.END)

    for f in sorted(only_in_1):
        left_box.insert(tk.END, f + "\n")

    for f in sorted(only_in_2):
        right_box.insert(tk.END, f + "\n")


# =========================
# UI Layout
# =========================
root = tk.Tk()
root.title("Folder Filename Comparator")
root.geometry("700x500")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# ---- ttk Style ----
style = ttk.Style()
style.theme_use("default")

style.configure("TLabel", font=DEFAULT_FONT, foreground=LABEL_COLOR)
style.configure("TEntry", font=DEFAULT_FONT)
style.configure("TButton", font=TITLE_FONT, padding=6)

style.configure(
    "White.TFrame",
    background=BG_COLOR
)


# ---- Top Section ----
main_frame = ttk.Frame(root, padding=12, style="White.TFrame")
main_frame.pack(fill="x")

folder1_var = tk.StringVar()
folder2_var = tk.StringVar()

ttk.Label(main_frame, text="Folder 1").grid(row=0, column=0, sticky="w", pady=5)
ttk.Entry(main_frame, textvariable=folder1_var, width=60).grid(row=0, column=1, padx=5)
ttk.Button(
    main_frame,
    text="Browse",
    command=lambda: select_folder(folder1_var)
).grid(row=0, column=2)

ttk.Label(main_frame, text="Folder 2").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(main_frame, textvariable=folder2_var, width=60).grid(row=1, column=1, padx=5)
ttk.Button(
    main_frame,
    text="Browse",
    command=lambda: select_folder(folder2_var)
).grid(row=1, column=2)

ttk.Button(
    main_frame,
    text="Compare",
    command=run_compare
).grid(row=2, column=1, pady=12)

# ---- Result Section ----
result_frame = ttk.Frame(root, padding=(12, 6), style="White.TFrame")
result_frame.pack(fill="both", expand=True)

ttk.Label(result_frame, text="Only in Folder 1").grid(row=0, column=0, sticky="w")
ttk.Label(result_frame, text="Only in Folder 2").grid(row=0, column=1, sticky="w")

left_box = ScrolledText(
    result_frame, width=45, height=18, wrap=tk.NONE,
    font=TEXT_FONT, bg=LEFT_BG_COLOR, fg=LEFT_TEXT_COLOR,
    insertbackground="#000000"
)
right_box = ScrolledText(
    result_frame, width=45, height=18, wrap=tk.NONE,
    font=TEXT_FONT, bg=RIGHT_BG_COLOR, fg=RIGHT_TEXT_COLOR,
    insertbackground="#000000"
)

left_box.grid(row=1, column=0, padx=(0, 8), pady=5)
right_box.grid(row=1, column=1, pady=5)

root.mainloop()
