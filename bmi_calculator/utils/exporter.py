"""Export utilities for CSV and chart PNG."""
import csv
from pathlib import Path
from typing import List

from bmi_calculator.database.models import BMIRecord


def export_history_csv(records: List[BMIRecord], path: str) -> str:
    p = Path(path)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "user_id", "weight_kg", "height_m", "bmi", "category", "recorded_at"])
        for r in records:
            writer.writerow([r.id, r.user_id, r.weight_kg, r.height_m, r.bmi, r.category, r.recorded_at])
    return str(p)


def export_chart_png(figure, path: str) -> str:
    p = Path(path)
    figure.savefig(str(p), dpi=150, bbox_inches="tight")
    return str(p)
