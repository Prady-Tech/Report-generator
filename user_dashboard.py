import tkinter as tk
from tkinter import messagebox

class UserDashboard:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("User Dashboard")
        self.root.geometry("400x300")

        label = tk.Label(self.root, text=f"Welcome, {username}", font=("Arial", 14))
        label.pack(pady=20)

        logout_btn = tk.Button(self.root, text="Logout", command=self.logout)
        logout_btn.pack(pady=20)

        self.root.mainloop()

    def logout(self):
        messagebox.showinfo("Logout", "You have been logged out.")
        self.root.destroy()
