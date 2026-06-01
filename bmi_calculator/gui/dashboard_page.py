"""Dashboard page showing analytics and charts for user history."""
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bmi_calculator.constants import CATEGORY_COLORS


class DashboardPage(ctk.CTkFrame):
    """Dashboard page with statistics and Matplotlib charts."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.build_ui()

    def build_ui(self) -> None:
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 12))

        stat_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        stat_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 12))
        stat_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.total_label = ctk.CTkLabel(stat_frame, text="Total Calculations\n0", justify="left", font=ctk.CTkFont(size=14, weight="bold"))
        self.latest_label = ctk.CTkLabel(stat_frame, text="Latest BMI\n--", justify="left", font=ctk.CTkFont(size=14, weight="bold"))
        self.average_label = ctk.CTkLabel(stat_frame, text="Average BMI\n--", justify="left", font=ctk.CTkFont(size=14, weight="bold"))
        self.common_label = ctk.CTkLabel(stat_frame, text="Most Common\n--", justify="left", font=ctk.CTkFont(size=14, weight="bold"))

        self.total_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.latest_label.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        self.average_label.grid(row=0, column=2, padx=20, pady=20, sticky="w")
        self.common_label.grid(row=0, column=3, padx=20, pady=20, sticky="w")

        self.chart_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.chart_frame.grid(row=2, column=0, sticky="nswe", padx=10, pady=(0, 10))
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure((0, 1), weight=1)

        self.figure = Figure(figsize=(10, 7), dpi=100)
        self.figure.patch.set_facecolor("#1E1E1E")
        self.bmi_axis = self.figure.add_subplot(221)
        self.pie_axis = self.figure.add_subplot(222)
        self.bar_axis = self.figure.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nswe")

        self.hover_annotation = self.figure.text(
            0.5,
            0.01,
            "",
            color="#FFFFFF",
            ha="center",
            va="bottom",
            fontsize=10,
            bbox={"facecolor": "#1E1E1E", "edgecolor": "#555555", "boxstyle": "round,pad=0.4"},
            visible=False,
        )
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def refresh(self) -> None:
        profile_name = self.app.get_current_profile_name()
        self.clear_charts()
        self.total_label.configure(text="Total Calculations\n0")
        self.latest_label.configure(text="Latest BMI\n--")
        self.average_label.configure(text="Average BMI\n--")
        self.common_label.configure(text="Most Common\n--")

        if profile_name is None:
            self.canvas.draw()
            return

        records = self.app.data_manager.get_history(profile_name)
        if not records:
            self.canvas.draw()
            return

        bmi_values = [record.get("bmi", 0) for record in records]
        categories = [record.get("category", "Unknown") for record in records]
        dates = [record.get("date", "") for record in records]

        self.current_dates = dates
        self.current_bmi_values = bmi_values
        self.current_categories = categories

        self.total_label.configure(text=f"Total Calculations\n{len(records)}")
        self.latest_label.configure(text=f"Latest BMI\n{bmi_values[-1]}")
        average = round(sum(bmi_values) / len(bmi_values), 2)
        self.average_label.configure(text=f"Average BMI\n{average}")
        self.common_label.configure(text=f"Most Common\n{self.most_common_category(categories)}")

        self.bmi_axis.set_facecolor("#1E1E1E")
        trend_line = self.bmi_axis.plot(dates, bmi_values, marker="o", color="#3CB371", linewidth=2)[0]
        self.trend_line = trend_line
        self.bmi_axis.set_title("BMI Trend")
        self.bmi_axis.set_ylabel("BMI")
        self.bmi_axis.set_xlabel("Date")
        self.bmi_axis.tick_params(colors="#FFFFFF", labelrotation=30)
        self.bmi_axis.spines["bottom"].set_color("#555555")
        self.bmi_axis.spines["left"].set_color("#555555")

        category_counts = {}
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1

        colors = [CATEGORY_COLORS.get(key, "#CCCCCC") for key in category_counts.keys()]
        labels = list(category_counts.keys())
        sizes = [category_counts[key] for key in labels]
        percentages = [size / sum(sizes) * 100 for size in sizes]
        self.current_pie_labels = labels
        self.current_pie_percentages = percentages
        self.pie_axis.set_facecolor("#1E1E1E")
        wedges, texts, autotexts = self.pie_axis.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            textprops={"color": "white", "fontsize": 10},
        )
        self.pie_wedges = wedges
        self.pie_axis.set_title("Category Distribution")
        self.pie_axis.axis("equal")

        self.bar_axis.set_facecolor("#1E1E1E")
        bars = self.bar_axis.bar(dates, bmi_values, color="#FFB366")
        self.bar_rects = bars
        self.bar_axis.set_ylabel("BMI")
        self.bar_axis.set_xlabel("Date")
        self.bar_axis.set_title("BMI History")
        self.bar_axis.tick_params(axis="x", rotation=45, colors="#FFFFFF")
        self.bar_axis.spines["bottom"].set_color("#555555")
        self.bar_axis.spines["left"].set_color("#555555")

        for label in self.bar_axis.get_xticklabels():
            label.set_ha("right")

        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def clear_charts(self) -> None:
        self.bmi_axis.clear()
        self.pie_axis.clear()
        self.bar_axis.clear()
        self.hover_annotation.set_visible(False)

    def on_hover(self, event) -> None:
        if event.inaxes == self.bmi_axis and hasattr(self, "trend_line"):
            self._update_line_hover(event)
        elif event.inaxes == self.bar_axis and hasattr(self, "bar_rects"):
            self._update_bar_hover(event)
        elif event.inaxes == self.pie_axis and hasattr(self, "pie_wedges"):
            self._update_pie_hover(event)
        else:
            self.hover_annotation.set_visible(False)
            self.canvas.draw_idle()

    def _update_line_hover(self, event) -> None:
        if event.xdata is None or event.ydata is None:
            self.hover_annotation.set_visible(False)
            self.canvas.draw_idle()
            return

        x_data = list(range(len(self.current_dates)))
        y_data = self.current_bmi_values
        closest_index = min(range(len(x_data)), key=lambda i: abs(event.xdata - x_data[i]))
        if abs(event.xdata - x_data[closest_index]) < 0.4:
            date = self.current_dates[closest_index]
            bmi = y_data[closest_index]
            self.hover_annotation.set_text(f"{date}: BMI {bmi}")
            self.hover_annotation.set_visible(True)
        else:
            self.hover_annotation.set_visible(False)
        self.canvas.draw_idle()

    def _update_bar_hover(self, event) -> None:
        found = False
        for rect, date, bmi in zip(self.bar_rects, self.current_dates, self.current_bmi_values):
            contains, _ = rect.contains(event)
            if contains:
                self.hover_annotation.set_text(f"{date}: BMI {bmi}")
                self.hover_annotation.set_visible(True)
                found = True
                break
        if not found:
            self.hover_annotation.set_visible(False)
        self.canvas.draw_idle()

    def _update_pie_hover(self, event) -> None:
        found = False
        for wedge, label, pct in zip(self.pie_wedges, self.current_pie_labels, self.current_pie_percentages):
            if wedge.contains_point((event.x, event.y)):
                self.hover_annotation.set_text(f"{label}: {pct:.1f}%")
                self.hover_annotation.set_visible(True)
                found = True
                break
        if not found:
            self.hover_annotation.set_visible(False)
        self.canvas.draw_idle()

    def most_common_category(self, categories: list[str]) -> str:
        counts = {}
        for category in categories:
            counts[category] = counts.get(category, 0) + 1
        return max(counts, key=counts.get)
