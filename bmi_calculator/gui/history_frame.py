"""History UI showing past BMI records with deletion and export."""
import customtkinter as ctk
from tkinter import ttk, filedialog
import pandas as pd

from bmi_calculator.utils.exporter import export_history_csv


class HistoryFrame(ctk.CTkFrame):
    """Frame showing historical entries in a table."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.build()

    def build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(self)
        top.grid(row=0, column=0, sticky="nswe", padx=8, pady=8)
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(top, columns=("date", "weight", "height", "bmi", "category"), show="headings")
        for c in ("date", "weight", "height", "bmi", "category"):
            self.tree.heading(c, text=c.title())
        self.tree.grid(row=0, column=0, sticky="nswe")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=0, pady=6)
        ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_selected).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="Export CSV", command=self.export_csv).grid(row=0, column=1, padx=6)

        self.stats_label = ctk.CTkLabel(self, text="Summary: --")
        self.stats_label.grid(row=2, column=0, pady=6)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not self.app.current_user:
            return
        records = self.app.db.get_records_for_user(self.app.current_user.id)
        for r in records:
            self.tree.insert("", "end", iid=r.id, values=(r.recorded_at, r.weight_kg, r.height_m, r.bmi, r.category))
        s = self.app.db.stats_for_user(self.app.current_user.id)
        self.stats_label.configure(text=f"Count: {s.get('count',0)}  Min: {s.get('min', '--')}  Max: {s.get('max','--')}  Avg: {round(s.get('avg') or 0,2)}")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        for iid in sel:
            self.app.db.delete_record(int(iid))
            self.tree.delete(iid)

    def export_csv(self):
        if not self.app.current_user:
            return
        records = self.app.db.get_records_for_user(self.app.current_user.id)
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        export_history_csv(records, path)
