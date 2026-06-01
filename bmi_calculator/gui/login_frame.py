"""Login and registration UI."""
import customtkinter as ctk
from tkinter import ttk

from bmi_calculator.core.validator import validate_user


class LoginFrame(ctk.CTkFrame):
    """Frame for user login and registration."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.build()

    def build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, sticky="nswe", padx=12, pady=12)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Welcome to BMI Calculator", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(8, 16))

        # Existing users list
        ctk.CTkLabel(left, text="Existing profiles:").grid(row=1, column=0, sticky="w")
        self.user_combo = ttk.Combobox(left, state="readonly")
        self.user_combo.grid(row=2, column=0, sticky="ew", pady=4)
        ctk.CTkButton(left, text="Load", command=self.load_user).grid(row=3, column=0, pady=6)

        sep = ctk.CTkLabel(left, text=" ")
        sep.grid(row=4, column=0)

        # Registration
        ctk.CTkLabel(left, text="Register new profile:").grid(row=5, column=0, sticky="w")
        self.entry_username = ctk.CTkEntry(left, placeholder_text="Username")
        self.entry_age = ctk.CTkEntry(left, placeholder_text="Age")
        # Use CustomTkinter option menu for better visibility across themes
        self.gender_combo = ctk.CTkOptionMenu(left, values=["Male", "Female", "Other"])
        self.gender_label = ctk.CTkLabel(left, text="Gender:")
        self.gender_label.grid(row=8, column=0, sticky="w", pady=(4, 0))
        self.gender_combo.grid(row=9, column=0, sticky="ew", pady=4)
        self.entry_username.grid(row=6, column=0, sticky="ew", pady=4)
        self.entry_age.grid(row=7, column=0, sticky="ew", pady=4)
        # default selection
        try:
            self.gender_combo.set("Male")
        except Exception:
            pass

        self.err_label = ctk.CTkLabel(left, text="", text_color="#e74c3c")
        self.err_label.grid(row=9, column=0, pady=4)

        ctk.CTkButton(left, text="Register", command=self.register).grid(row=10, column=0, pady=8)

        self.refresh()

    def refresh(self):
        users = self.app.db.list_users()
        names = [u.username for u in users]
        self.user_combo["values"] = names

    def load_user(self):
        sel = self.user_combo.get()
        if not sel:
            return
        user = self.app.db.get_user_by_username(sel)
        if user:
            self.app.set_current_user(user)
            self.app.show_frame("calculator")

    def register(self):
        username = self.entry_username.get()
        age = self.entry_age.get()
        gender = self.gender_combo.get()
        errs = validate_user(username, age, gender)
        if errs:
            self.err_label.configure(text="; ".join(errs.values()))
            return
        user = self.app.db.add_user(username, int(age), gender)
        self.app.set_current_user(user)
        self.app.show_frame("calculator")
