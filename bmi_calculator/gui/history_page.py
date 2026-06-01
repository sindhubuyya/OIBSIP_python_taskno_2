"""History page showing stored BMI calculations and export options."""
import customtkinter as ctk
from tkinter import ttk, filedialog
from pathlib import Path


class HistoryPage(ctk.CTkFrame):
    """History page with search, sort, delete, and export."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.sort_ascending = False
        self.build_ui()

    def build_ui(self) -> None:
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="History", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 12))

        control_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 12))
        control_frame.grid_columnconfigure(2, weight=1)

        self.search_entry = ctk.CTkEntry(control_frame, placeholder_text="Search history")
        self.search_entry.grid(row=0, column=0, padx=12, pady=12, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _: self.refresh())

        self.sort_button = ctk.CTkButton(control_frame, text="Sort by Date", command=self.toggle_sort)
        self.sort_button.grid(row=0, column=1, padx=12, pady=12)

        self.clear_button = ctk.CTkButton(control_frame, text="Clear All", fg_color="#FF6B6B", hover_color="#FF4D4D", command=self.clear_all)
        self.clear_button.grid(row=0, column=2, padx=12, pady=12, sticky="e")

        self.table_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        self.table_frame.grid(row=2, column=0, sticky="nswe", padx=10, pady=(0, 10))
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        columns = ("date", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        for column in columns:
            self.tree.heading(column, text=column.title())
            self.tree.column(column, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nswe")

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        action_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=12)
        action_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 12))
        action_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.delete_button = ctk.CTkButton(action_frame, text="Delete Selected", command=self.delete_selected)
        self.export_button = ctk.CTkButton(action_frame, text="Export CSV", command=self.export_csv)
        self.status_label = ctk.CTkLabel(action_frame, text="No history loaded yet.")

        self.delete_button.grid(row=0, column=0, padx=12, pady=12, sticky="ew")
        self.export_button.grid(row=0, column=1, padx=12, pady=12, sticky="ew")
        self.status_label.grid(row=0, column=2, padx=12, pady=12, sticky="e")

    def refresh(self) -> None:
        profile_name = self.app.get_current_profile_name()
        self.tree.delete(*self.tree.get_children())
        if profile_name is None:
            self.status_label.configure(text="Load a profile first.")
            return
        records = self.app.data_manager.get_history(profile_name)
        if self.search_entry.get().strip():
            filter_text = self.search_entry.get().strip().lower()
            records = [
                record
                for record in records
                if filter_text in record.get("date", "").lower()
                or filter_text in record.get("category", "").lower()
                or filter_text in record.get("weight", "").lower()
                or filter_text in record.get("height", "").lower()
            ]

        records.sort(key=lambda r: r.get("date", ""), reverse=not self.sort_ascending)

        for record in records:
            self.tree.insert(
                "",
                "end",
                iid=record.get("id"),
                values=(record.get("date"), record.get("weight"), record.get("height"), record.get("bmi"), record.get("category")),
            )

        if records:
            self.status_label.configure(text=f"{len(records)} records shown.")
        else:
            self.status_label.configure(text="No history records found.")

    def toggle_sort(self) -> None:
        self.sort_ascending = not self.sort_ascending
        direction = "ascending" if self.sort_ascending else "descending"
        self.sort_button.configure(text=f"Sort by Date ({direction})")
        self.refresh()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            self.status_label.configure(text="No record selected.")
            return
        record_id = selected[0]
        self.app.data_manager.delete_record(record_id)
        self.refresh()
        self.app.dashboard_page.refresh()
        self.status_label.configure(text="Record deleted.")

    def clear_all(self) -> None:
        profile_name = self.app.get_current_profile_name()
        if profile_name is None:
            self.status_label.configure(text="Load a profile first.")
            return
        self.app.data_manager.clear_history(profile_name)
        self.refresh()
        self.app.dashboard_page.refresh()
        self.status_label.configure(text="History cleared.")

    def export_csv(self) -> None:
        profile_name = self.app.get_current_profile_name()
        if profile_name is None:
            self.status_label.configure(text="Load a profile first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export history to CSV",
        )
        if not path:
            return
        self.app.data_manager.export_history_csv(profile_name, Path(path))
        self.status_label.configure(text="History exported successfully.")
