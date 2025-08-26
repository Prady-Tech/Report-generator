import tkinter as tk
from tkinter import filedialog, messagebox
from report_logic import generate_summary_report

def open_file(role):
    if role != "admin" and role != "user":
        messagebox.showerror("Access Denied", "You don't have permission to generate reports.")
        return

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if file_path:
        try:
            report_path = generate_summary_report(file_path)
            messagebox.showinfo("Success", f"Report saved at:\n{report_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{e}")

def run_gui(role):
    root = tk.Tk()
    root.title(f"Excel Report Generator - Logged in as {role}")
    root.geometry("400x200")

    if role == "admin":
        label = tk.Label(root, text="Admin Dashboard", font=("Arial", 14))
    else:
        label = tk.Label(root, text="User Dashboard", font=("Arial", 14))
    label.pack(pady=20)

    open_btn = tk.Button(root, text="Select Excel File", command=lambda: open_file(role), width=20)
    open_btn.pack(pady=10)

    root.mainloop()
