"""BMI calculator page with metric/imperial conversion and results card."""
import customtkinter as ctk
from tkinter import Canvas
from datetime import datetime

from bmi_calculator.constants import BMI_CATEGORIES, HEALTH_TIPS, CATEGORY_COLORS
from bmi_calculator.utils.bmi_utils import calculate_imperial_bmi, calculate_metric_bmi, classify_bmi


class CalculatorPage(ctk.CTkFrame):
    """Calculator page where users input measurements and see BMI results."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.measurement_system = "Metric"
        self.build_ui()

    def build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="BMI Calculator", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(8, 12), padx=10)

        self.form_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_rowconfigure(1, weight=1)
        self.form_frame.grid_rowconfigure(2, weight=1)

        self.system_toggle = ctk.CTkSegmentedButton(
            self.form_frame,
            values=["Metric", "Imperial"],
            command=self.on_system_change,
            width=220,
        )
        self.system_toggle.set("Metric")
        self.system_toggle.grid(row=0, column=0, columnspan=2, padx=20, pady=(16, 16), sticky="w")

        self.metric_frame = ctk.CTkFrame(self.form_frame, fg_color="#232323", corner_radius=10)
        self.metric_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 12))
        self.metric_frame.grid_columnconfigure(0, weight=1)

        self.weight_kg = ctk.CTkEntry(self.metric_frame, placeholder_text="Weight (kg)")
        self.height_cm = ctk.CTkEntry(self.metric_frame, placeholder_text="Height (cm)")
        self.weight_kg.grid(row=0, column=0, padx=12, pady=8, sticky="ew")
        self.height_cm.grid(row=1, column=0, padx=12, pady=8, sticky="ew")

        self.imperial_frame = ctk.CTkFrame(self.form_frame, fg_color="#232323", corner_radius=10)
        self.imperial_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 12))
        self.imperial_frame.grid_columnconfigure((0, 1), weight=1)

        self.weight_lbs = ctk.CTkEntry(self.imperial_frame, placeholder_text="Weight (lbs)")
        self.height_feet = ctk.CTkEntry(self.imperial_frame, placeholder_text="Feet")
        self.height_inches = ctk.CTkEntry(self.imperial_frame, placeholder_text="Inches")
        self.weight_lbs.grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="ew")
        self.height_feet.grid(row=1, column=0, padx=(12, 6), pady=8, sticky="ew")
        self.height_inches.grid(row=1, column=1, padx=(6, 12), pady=8, sticky="ew")

        self.error_label = ctk.CTkLabel(self.form_frame, text="", text_color="#FF6B6B")
        self.error_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="w")

        self.calculate_button = ctk.CTkButton(self.form_frame, text="Calculate BMI", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 16), sticky="ew")

        self.result_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.result_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.result_frame.grid_columnconfigure(0, weight=1)

        self.bmi_value_label = ctk.CTkLabel(self.result_frame, text="BMI: --", font=ctk.CTkFont(size=28, weight="bold"))
        self.category_label = ctk.CTkLabel(self.result_frame, text="Category: --", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label = ctk.CTkLabel(self.result_frame, text="Status: --")
        self.tip_label = ctk.CTkLabel(self.result_frame, text="Tip: --", wraplength=760)
        self.progress = ctk.CTkProgressBar(self.result_frame)
        self.date_label = ctk.CTkLabel(self.result_frame, text="Date: --")

        self.bmi_value_label.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 6))
        self.category_label.grid(row=1, column=0, sticky="w", padx=20, pady=4)
        self.status_label.grid(row=2, column=0, sticky="w", padx=20, pady=4)
        self.tip_label.grid(row=3, column=0, sticky="w", padx=20, pady=4)
        self.progress.grid(row=4, column=0, sticky="ew", padx=20, pady=12)
        self.date_label.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 16))

        ctk.CTkLabel(self.result_frame, text="BMI Gauge Meter", font=ctk.CTkFont(size=14, weight="bold")).grid(row=6, column=0, sticky="w", padx=20, pady=(0, 4))
        self.gauge_canvas = Canvas(self.result_frame, width=760, height=180, bg="#1E1E1E", highlightthickness=0)
        self.gauge_canvas.grid(row=7, column=0, padx=20, pady=(0, 20))

        self.imperial_frame.grid_remove()

    def refresh(self) -> None:
        if self.app.current_profile is None:
            self.error_label.configure(text="Please load a profile on the Profile page before calculating.")
        else:
            self.error_label.configure(text="")

    def on_system_change(self, system: str) -> None:
        self.measurement_system = system
        if system == "Metric":
            self.metric_frame.grid()
            self.imperial_frame.grid_remove()
        else:
            self.metric_frame.grid_remove()
            self.imperial_frame.grid()
        self.clear_errors()

    def clear_errors(self) -> None:
        self.error_label.configure(text="")

    def calculate(self) -> None:
        if self.app.current_profile is None:
            self.error_label.configure(text="Load a profile first before calculating BMI.")
            return

        values = {}
        if self.measurement_system == "Metric":
            values["weight"] = self.weight_kg.get().strip()
            values["height"] = self.height_cm.get().strip()
        else:
            values["weight"] = self.weight_lbs.get().strip()
            values["feet"] = self.height_feet.get().strip()
            values["inches"] = self.height_inches.get().strip()

        errors = self.validate_values(values)
        if errors:
            self.error_label.configure(text=errors)
            return

        bmi, category = self.compute_bmi(values)
        status = BMI_CATEGORIES[category]["status"]
        tip = HEALTH_TIPS.get(category, "Keep tracking your progress.")
        formatted_height = self.format_height(values)
        self.update_results(bmi, category, status, tip)

        self.app.data_manager.add_record(
            profile_name=self.app.current_profile["name"],
            weight=values["weight"],
            height=formatted_height,
            system=self.measurement_system,
            bmi=bmi,
            category=category,
            tip=tip,
        )
        self.app.history_page.refresh()
        self.app.dashboard_page.refresh()
        self.clear_inputs()
        self.calculate_button.configure(text="Calculated ✓")
        self.after(1800, lambda: self.calculate_button.configure(text="Calculate BMI"))

    def validate_values(self, values: dict) -> str:
        if self.measurement_system == "Metric":
            if not values["weight"] or not values["height"]:
                return "Please enter both weight and height."
            if not self.is_positive_number(values["weight"]):
                return "Weight must be a positive number."
            if not self.is_positive_number(values["height"]):
                return "Height must be a positive number."
            if float(values["weight"]) <= 0 or float(values["height"]) <= 0:
                return "Numbers must be greater than zero."
        else:
            if not values["weight"] or not values["feet"] or not values["inches"]:
                return "Please enter weight, feet, and inches."
            if not self.is_positive_number(values["weight"]):
                return "Weight must be a positive number."
            if not values["feet"].isdigit() or not values["inches"].isdigit():
                return "Feet and inches must be whole numbers."
            if int(values["feet"]) <= 0 or int(values["inches"]) < 0:
                return "Height values must be positive."
        return ""

    def is_positive_number(self, value: str) -> bool:
        try:
            return float(value) > 0
        except ValueError:
            return False

    def compute_bmi(self, values: dict) -> tuple[float, str]:
        if self.measurement_system == "Metric":
            bmi = calculate_metric_bmi(float(values["weight"]), float(values["height"]))
        else:
            bmi = calculate_imperial_bmi(float(values["weight"]), int(values["feet"]), int(values["inches"]))
        category = classify_bmi(bmi)
        return bmi, category

    def format_height(self, values: dict) -> str:
        if self.measurement_system == "Metric":
            return f"{values['height']} cm"
        return f"{values['feet']} ft {values['inches']} in"

    def update_results(self, bmi: float, category: str, status: str, tip: str) -> None:
        category_color = CATEGORY_COLORS.get(category, "#3CB371")
        self.bmi_value_label.configure(text=f"BMI: {bmi}")
        self.category_label.configure(text=f"Category: {category}", text_color=category_color)
        self.status_label.configure(text=f"Status: {status}")
        self.tip_label.configure(text=f"Tip: {tip}")
        self.date_label.configure(text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        position = min(max((bmi / 40), 0), 1)
        self.progress.set(position)
        self.draw_gauge(position, category_color)

    def clear_inputs(self) -> None:
        self.weight_kg.delete(0, "end")
        self.height_cm.delete(0, "end")
        self.weight_lbs.delete(0, "end")
        self.height_feet.delete(0, "end")
        self.height_inches.delete(0, "end")

    def draw_gauge(self, position: float, color: str) -> None:
        self.gauge_canvas.delete("all")
        width = 760
        height = 180
        self.gauge_canvas.create_arc(20, 20, width - 20, height * 2, start=180, extent=180, outline="#555555", width=16)
        self.gauge_canvas.create_arc(20, 20, width - 20, height * 2, start=180, extent=180 * position, outline=color, width=16)
        angle = 180 * position
        from math import cos, radians, sin

        center_x = width / 2
        center_y = height
        radius = 100
        needle_x = center_x + radius * cos(radians(180 - angle))
        needle_y = center_y - radius * sin(radians(180 - angle))
        self.gauge_canvas.create_line(center_x, center_y, needle_x, needle_y, fill="#FFFFFF", width=4)
        self.gauge_canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="#FFFFFF", outline="")
