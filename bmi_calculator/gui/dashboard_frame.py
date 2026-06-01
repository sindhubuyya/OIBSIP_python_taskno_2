"""Dashboard with embedded Matplotlib charts and summary stats."""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

from bmi_calculator.utils.constants import BMI_RANGES


class DashboardFrame(ctk.CTkFrame):
    """Frame showing BMI and weight trend charts embedded in the GUI."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.build()

    def build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax_bmi = self.fig.add_subplot(211)
        self.ax_weight = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nswe")

    def refresh(self):
        self.ax_bmi.clear()
        self.ax_weight.clear()
        if not self.app.current_user:
            self.canvas.draw()
            return
        records = self.app.db.get_records_for_user(self.app.current_user.id)
        if not records:
            self.canvas.draw()
            return
        df = pd.DataFrame([{
            "date": r.recorded_at,
            "bmi": r.bmi,
            "weight": r.weight_kg,
        } for r in records])
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # BMI chart with background bands
        dates = df["date"]
        bmis = df["bmi"].astype(float)
        self.ax_bmi.plot(dates, bmis, marker="o", label="BMI")
        # moving average (last 5 entries)
        if len(bmis) >= 2:
            ma = bmis.rolling(window=min(5, len(bmis))).mean()
            self.ax_bmi.plot(dates, ma, linestyle="--", label="Moving Avg")

        # background bands
        ymin, ymax = 10, 50
        for name, (low, high, col) in BMI_RANGES.items():
            l = low if low is not None else ymin
            h = high if high is not None else ymax
            self.ax_bmi.axhspan(l, h, color=col, alpha=0.08)

        self.ax_bmi.set_ylabel("BMI")
        self.ax_bmi.legend()

        # weight chart
        self.ax_weight.plot(dates, df["weight"], marker="o", color="#3498db")
        self.ax_weight.set_ylabel("Weight (kg)")
        self.ax_weight.set_xlabel("Date")

        self.fig.tight_layout()
        self.canvas.draw()
