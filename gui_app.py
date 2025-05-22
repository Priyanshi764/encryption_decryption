import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
import os

# ---------- Hover Animation ----------
def add_hover_effects(button):
    def on_enter(e):
        button.config(bg="#2563EB")
    def on_leave(e):
        button.config(bg=PRO_LIGHT_THEME["button_bg"])
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# ---------- Key Functions ----------
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Success", "🔑 Key generated and saved as 'key.key'")

def load_key():
    if not os.path.exists("key.key"):
        messagebox.showerror("Error", "❌ Key file not found. Please generate a key first.")
        return None
    with open("key.key", "rb") as key_file:
        return key_file.read()

def load_key_with_password():
    password = password_entry.get()
    if password != "your_secret_password":
        messagebox.showerror("Error", "❌ Incorrect password!")
        return None
    return load_key()

# ---------- Encrypt/Decrypt ----------
def encrypt_file():
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    with open(filepath, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    new_name = filepath + ".enc"
    with open(new_name, "wb") as file:
        file.write(encrypted)

    messagebox.showinfo("Success", f"✅ Encrypted and saved as: {os.path.basename(new_name)}")

def decrypt_file():
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    with open(filepath, "rb") as file:
        encrypted = file.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        messagebox.showerror("Error", "❌ Decryption failed. Is the key or password correct?")
        return

    new_name = filepath.replace(".enc", "") + "_decrypted"
    with open(new_name, "wb") as file:
        file.write(decrypted)

    messagebox.showinfo("Success", f"✅ Decrypted and saved as: {os.path.basename(new_name)}")

def animate_status_dots(message, count=0):
    dots = "." * (count % 4)
    status_label.config(text=f"{message}{dots}")
    root.after(500, lambda: animate_status_dots(message, count + 1))

def encrypt_all_files_in_folder():
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)
    if total_files == 0:
        messagebox.showinfo("Info", "No files found in the folder.")
        return

    progress['maximum'] = total_files
    progress['value'] = 0

    for i, filename in enumerate(files, start=1):
        full_path = os.path.join(folder_path, filename)
        with open(full_path, "rb") as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        new_file = full_path + ".enc"
        with open(new_file, "wb") as file:
            file.write(encrypted)

        progress['value'] = i
        animate_status_dots(f"Encrypting file {i} of {total_files}")
        root.update_idletasks()

    status_label.config(text="✅ Encryption complete!")
    messagebox.showinfo("Success", f"Encrypted {total_files} files.")

# ---------- Themes ----------
PRO_LIGHT_THEME = {
    "bg": "#F5F7FA",
    "fg": "#2E3440",
    "button_bg": "#3B82F6",
    "button_fg": "#FFFFFF",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#2E3440",
    "check_bg": "#F5F7FA"
}

PRO_DARK_THEME = {
    "bg": "#1E1E2F",
    "fg": "#D8DEE9",
    "button_bg": "#4C6EF5",
    "button_fg": "#FFFFFF",
    "entry_bg": "#2A2D3E",
    "entry_fg": "#D8DEE9",
    "check_bg": "#1E1E2F"
}

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(
                bg=theme["button_bg"], fg=theme["button_fg"],
                activebackground=theme["button_bg"], relief="flat"
            )
        elif isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=theme["entry_bg"], fg=theme["entry_fg"],
                insertbackground=theme["fg"]
            )
        elif isinstance(widget, tk.Checkbutton):
            widget.configure(
                bg=theme["check_bg"], fg=theme["fg"],
                selectcolor=theme["check_bg"], activebackground=theme["check_bg"]
            )
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=theme["bg"])
    style.configure("TProgressbar", background=theme["button_bg"], troughcolor=theme["entry_bg"])

def toggle_theme():
    if dark_mode_var.get():
        apply_theme(PRO_DARK_THEME)
    else:
        apply_theme(PRO_LIGHT_THEME)

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("🔐 File Encryption App")
root.geometry("420x520")
root.resizable(True, True)

style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=20)

# Title with animation
title_label = tk.Label(root, text="", font=("Helvetica", 18))
title_label.pack(pady=10)

def animate_title(text, index=0):
    if index < len(text):
        title_label.config(text=text[:index + 1])
        root.after(100, animate_title, text, index + 1)

animate_title("🔒 Secure File Tool")

# Progress and Status
progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate', style="TProgressbar")
progress.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=(0, 10))

# Password entry
tk.Label(root, text="Enter Password:").pack()
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

# Button frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# Buttons
buttons = [
    ("🔑 Generate Key", generate_key),
    ("🔒 Encrypt Single File", encrypt_file),
    ("🔓 Decrypt File", decrypt_file),
    ("📁 Encrypt All Files in Folder", encrypt_all_files_in_folder),
    ("🚪 Exit", root.quit)
]

for text, command in buttons:
    btn = tk.Button(btn_frame, text=text, width=25, command=command)
    btn.pack(pady=5)
    add_hover_effects(btn)

# Dark Mode Toggle
dark_mode_var = tk.BooleanVar(value=False)
dark_mode_checkbox = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode_var, command=toggle_theme)
dark_mode_checkbox.pack(pady=10)

apply_theme(PRO_LIGHT_THEME)

# Run app
root.mainloop()
