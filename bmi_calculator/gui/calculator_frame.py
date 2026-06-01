"""Main calculator UI with inputs, validation, animation, and saving."""
import customtkinter as ctk
from tkinter import Canvas
import threading

from bmi_calculator.core.calculator import calculate_bmi, kg_from_lbs, m_from_ft_in, classify_bmi, healthy_weight_range_for_height
from bmi_calculator.core.validator import validate_measurements
from bmi_calculator.utils.constants import HEALTH_TIPS, BMI_RANGES


class CalculatorFrame(ctk.CTkFrame):
    """Calculator frame where users input measurements and see results."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.metric = True
        self._anim_lock = threading.Lock()
        self.build()

    def build(self):
        left = ctk.CTkFrame(self, width=420)
        left.grid(row=0, column=0, sticky="nswe", padx=8, pady=8)
        right = ctk.CTkFrame(self)
        right.grid(row=0, column=1, sticky="nswe", padx=8, pady=8)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(left, text="Measurements", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=6)

        self.unit_switch = ctk.CTkSegmentedButton(left, values=["Metric", "Imperial"], command=self.on_unit_change)
        self.unit_switch.grid(row=1, column=0, pady=4)
        self.unit_switch.set("Metric")

        self.entry_weight = ctk.CTkEntry(left, placeholder_text="Weight (kg)")
        self.entry_height = ctk.CTkEntry(left, placeholder_text="Height (m)")
        # Imperial fields
        self.entry_feet = ctk.CTkEntry(left, placeholder_text="Feet")
        self.entry_inches = ctk.CTkEntry(left, placeholder_text="Inches")

        self.entry_weight.grid(row=2, column=0, sticky="ew", pady=4)
        self.entry_height.grid(row=3, column=0, sticky="ew", pady=4)
        self.entry_feet.grid(row=4, column=0, sticky="ew", pady=4)
        self.entry_inches.grid(row=5, column=0, sticky="ew", pady=4)

        self.err_weight = ctk.CTkLabel(left, text="", text_color="#e74c3c")
        self.err_height = ctk.CTkLabel(left, text="", text_color="#e74c3c")
        self.err_weight.grid(row=6, column=0)
        self.err_height.grid(row=7, column=0)

        self.btn_calc = ctk.CTkButton(left, text="Calculate", command=self.calculate)
        self.btn_calc.grid(row=8, column=0, pady=8)

        # Right: results and gauge
        self.canvas = Canvas(right, width=400, height=220, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=8)
        self.bmi_label = ctk.CTkLabel(right, text="BMI: --", font=ctk.CTkFont(size=28, weight="bold"))
        self.bmi_label.grid(row=1, column=0)
        self.category_badge = ctk.CTkLabel(right, text="Category", fg_color="#dddddd")
        self.category_badge.grid(row=2, column=0, pady=6)
        self.tip_label = ctk.CTkLabel(right, text="Tip: ", wraplength=380)
        self.tip_label.grid(row=3, column=0, pady=6)

        self.on_unit_change("Metric")

    def on_unit_change(self, val):
        self.metric = val == "Metric"
        if self.metric:
            self.entry_weight.configure(placeholder_text="Weight (kg)")
            self.entry_height.configure(state="normal")
            self.entry_feet.configure(state="disabled")
            self.entry_inches.configure(state="disabled")
        else:
            self.entry_weight.configure(placeholder_text="Weight (lbs)")
            self.entry_height.configure(state="disabled")
            self.entry_feet.configure(state="normal")
            self.entry_inches.configure(state="normal")

    def calculate(self):
        # gather inputs
        weight = self.entry_weight.get()
        if self.metric:
            height = self.entry_height.get()
            errs = validate_measurements(weight, height_m=height, metric=True)
        else:
            feet = self.entry_feet.get()
            inches = self.entry_inches.get()
            errs = validate_measurements(weight, feet=feet, inches=inches, metric=False)

        self.err_weight.configure(text=errs.get("weight", ""))
        self.err_height.configure(text=errs.get("height", errs.get("feet_inches", "")))

        if errs:
            return

        if self.metric:
            w = float(weight)
            h = float(self.entry_height.get())
        else:
            w = kg_from_lbs(float(weight))
            h = m_from_ft_in(int(self.entry_feet.get()), int(self.entry_inches.get()))

        bmi = calculate_bmi(w, h)
        category = classify_bmi(bmi)
        self.bmi_label.configure(text=f"BMI: {bmi}")
        color = BMI_RANGES.get(category, (None, None, "#cccccc"))[2]
        self.category_badge.configure(text=category, fg_color=color)
        self.tip_label.configure(text=HEALTH_TIPS.get(category, ""))

        # animate gauge
        self.animate_gauge(bmi)

        # save record
        if self.app.current_user:
            self.app.db.add_bmi_record(self.app.current_user.id, w, h, bmi, category)

    def animate_gauge(self, bmi_value: float):
        # semicircular gauge from 10 to 50 bmi mapped to 0..180 degrees
        min_bmi, max_bmi = 10, 50
        pct = min(max((bmi_value - min_bmi) / (max_bmi - min_bmi), 0.0), 1.0)
        target_deg = 180 * pct

        with self._anim_lock:
            self.canvas.delete("all")
            # draw semicircle background
            self.canvas.create_arc(10, 10, 390, 390, start=180, extent=180, style="arc", width=30, outline="#ecf0f1")

            # draw colored ranges
            start = 180
            for name, (low, high, col) in BMI_RANGES.items():
                # map ranges to extents
                l = low if low is not None else min_bmi
                h = high if high is not None else max_bmi
                s_pct = min(max((l - min_bmi) / (max_bmi - min_bmi), 0.0), 1.0)
                e_pct = min(max((h - min_bmi) / (max_bmi - min_bmi), 0.0), 1.0)
                extent = (e_pct - s_pct) * 180
                self.canvas.create_arc(10, 10, 390, 390, start=180 + s_pct * 180, extent=extent, style="arc", width=30, outline=col)

            # draw needle
            cx, cy = 200, 200
            length = 140

            # animate steps
            current = 0

            def step():
                nonlocal current
                if current > target_deg:
                    return
                self.canvas.delete("needle")
                import math

                ang = math.radians(180 - current)
                x = cx + length * math.cos(ang)
                y = cy - length * math.sin(ang)
                self.canvas.create_line(cx, cy, x, y, width=4, fill="#2c3e50", tags=("needle",))
                current += max(1, target_deg / 30)
                self.after(16, step)

            step()
