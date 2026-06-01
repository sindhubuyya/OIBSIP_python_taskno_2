"""Main application window and frame controller."""
import customtkinter as ctk
from typing import Any, Dict, Optional

from bmi_calculator.assets.styles import setup_theme
from bmi_calculator.data_manager import DataManager
from bmi_calculator.gui.profile_page import ProfilePage
from bmi_calculator.gui.calculator_page import CalculatorPage
from bmi_calculator.gui.history_page import HistoryPage
from bmi_calculator.gui.dashboard_page import DashboardPage


class BMIApp(ctk.CTk):
    """Main CTk application that coordinates the pages and data manager."""

    def __init__(self):
        super().__init__()
        setup_theme()
        self.title("BMI Calculator")
        self.geometry("1100x720")
        self.minsize(1000, 680)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.data_manager = DataManager()
        self.current_profile = None

        self.sidebar = ctk.CTkFrame(self, fg_color="#252526", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="BMI Calculator",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, padx=20, pady=(24, 12), sticky="w")

        self.user_label = ctk.CTkLabel(
            self.sidebar,
            text="No profile loaded",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC",
        )
        self.user_label.grid(row=1, column=0, padx=20, pady=(0, 24), sticky="w")

        self.btn_profile = ctk.CTkButton(
            self.sidebar,
            text="Profile",
            fg_color="#3CB371",
            hover_color="#33AA5E",
            command=lambda: self.show_page("profile"),
        )
        self.btn_calculator = ctk.CTkButton(
            self.sidebar,
            text="Calculator",
            fg_color="#3CB371",
            hover_color="#33AA5E",
            command=lambda: self.show_page("calculator"),
        )
        self.btn_history = ctk.CTkButton(
            self.sidebar,
            text="History",
            fg_color="#FFB366",
            hover_color="#E6A05A",
            command=lambda: self.show_page("history"),
        )
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            fg_color="#FFB366",
            hover_color="#E6A05A",
            command=lambda: self.show_page("dashboard"),
        )

        self.btn_profile.grid(row=2, column=0, padx=20, pady=6, sticky="ew")
        self.btn_calculator.grid(row=3, column=0, padx=20, pady=6, sticky="ew")
        self.btn_history.grid(row=4, column=0, padx=20, pady=6, sticky="ew")
        self.btn_dashboard.grid(row=5, column=0, padx=20, pady=6, sticky="ew")

        self.container = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.container.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {
            "profile": ProfilePage(self.container, self),
            "calculator": CalculatorPage(self.container, self),
            "history": HistoryPage(self.container, self),
            "dashboard": DashboardPage(self.container, self),
        }

        self.profile_page = self.pages["profile"]
        self.calculator_page = self.pages["calculator"]
        self.history_page = self.pages["history"]
        self.dashboard_page = self.pages["dashboard"]

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nswe")

        self.show_page("profile")

    def show_page(self, page_name: str) -> None:
        page = self.pages.get(page_name)
        if page is None:
            return
        page.tkraise()
        if hasattr(page, "refresh"):
            page.refresh()

    def set_current_profile(self, profile: Dict[str, Any]) -> None:
        self.current_profile = profile
        self.user_label.configure(text=f"Logged in: {profile.get('name')}")
        self.show_page("calculator")

    def get_current_profile_name(self) -> Optional[str]:
        return self.current_profile.get("name") if self.current_profile else None
