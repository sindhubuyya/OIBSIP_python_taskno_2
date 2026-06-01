"""Profile management page for registration and loading users."""
import customtkinter as ctk


class ProfilePage(ctk.CTkFrame):
    """Profile page with registration and existing profile loading."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.profile_buttons = []
        self.build_ui()

    def build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Profile Management", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(8, 12))

        card = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        card.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        card.grid_columnconfigure((0, 1), weight=1)

        form_label = ctk.CTkLabel(card, text="Register New Profile", font=ctk.CTkFont(size=18, weight="bold"))
        form_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(12, 6), padx=12)

        self.name_entry = ctk.CTkEntry(card, placeholder_text="Name")
        self.age_entry = ctk.CTkEntry(card, placeholder_text="Age")
        self.gender_menu = ctk.CTkOptionMenu(card, values=["--  --", "Male", "Female", "Other"], width=200)
        self.gender_menu.set("--  --")

        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=6)
        self.age_entry.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        self.gender_menu.grid(row=2, column=1, sticky="ew", padx=12, pady=6)

        self.profile_message = ctk.CTkLabel(card, text="", text_color="#FFB366")
        self.profile_message.grid(row=3, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 6))

        self.save_button = ctk.CTkButton(card, text="Save Profile", command=self.save_profile)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=12, pady=(0, 16), sticky="ew")

        self.current_profile_card = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.current_profile_card.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.current_profile_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.current_profile_card, text="Current Profile", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", pady=(12, 6), padx=12)
        self.current_profile_label = ctk.CTkLabel(self.current_profile_card, text="No profile loaded.", font=ctk.CTkFont(size=14))
        self.current_profile_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 12))

        self.profiles_card = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.profiles_card.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.profiles_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.profiles_card, text="Existing Profiles", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", pady=(12, 6), padx=12)
        self.profile_list_frame = ctk.CTkScrollableFrame(self.profiles_card, fg_color="#1E1E1E", corner_radius=8, height=260)
        self.profile_list_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.profile_list_frame.grid_columnconfigure(0, weight=1)

    def refresh(self) -> None:
        self.refresh_profile_list()
        if self.app.current_profile:
            profile = self.app.current_profile
            self.current_profile_label.configure(
                text=f"Name: {profile.get('name')}\nAge: {profile.get('age')}\nGender: {profile.get('gender')}"
            )
        else:
            self.current_profile_label.configure(text="No profile loaded.")
            self.profile_message.configure(text="")

    def refresh_profile_list(self) -> None:
        for widget in self.profile_list_frame.winfo_children():
            widget.destroy()

        profile_names = self.app.data_manager.get_profile_names()
        if not profile_names:
            ctk.CTkLabel(self.profile_list_frame, text="No profiles yet.", text_color="#CCCCCC").grid(row=0, column=0, sticky="w", padx=10, pady=10)
            return

        for index, name in enumerate(profile_names):
            profile_line = ctk.CTkFrame(self.profile_list_frame, fg_color="#252526", corner_radius=8)
            profile_line.grid(row=index, column=0, sticky="ew", padx=8, pady=6)
            profile_line.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(profile_line, text=name, font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
            ctk.CTkButton(profile_line, text="Load", fg_color="#3CB371", hover_color="#33AA5E", command=lambda n=name: self.load_profile_name(n)).grid(row=0, column=1, padx=10, pady=10)

    def save_profile(self) -> None:
        name = self.name_entry.get().strip()
        age_value = self.age_entry.get().strip()
        gender = self.gender_menu.get()

        if not name:
            self.profile_message.configure(text="Name cannot be empty.", text_color="#FF6B6B")
            return
        if not age_value.isdigit() or int(age_value) <= 0:
            self.profile_message.configure(text="Age must be a positive number.", text_color="#FF6B6B")
            return
        if gender == "--  --":
            self.profile_message.configure(text="Please choose a gender.", text_color="#FF6B6B")
            return

        try:
            self.app.data_manager.add_profile(name, int(age_value), gender)
            self.profile_message.configure(text="Profile saved successfully!", text_color="#3CB371")
            self.name_entry.delete(0, "end")
            self.age_entry.delete(0, "end")
            self.gender_menu.set("--  --")
            self.refresh()
        except ValueError as error:
            self.profile_message.configure(text=str(error), text_color="#FF6B6B")

    def load_profile_name(self, name: str) -> None:
        profile = self.app.data_manager.get_profile(name)
        if profile:
            self.app.set_current_profile(profile)
            self.profile_message.configure(text=f"Loaded {name}", text_color="#3CB371")
            self.refresh()
        else:
            self.profile_message.configure(text="Could not load that profile.", text_color="#FF6B6B")
