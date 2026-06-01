"""Manage profile and history data using JSON storage."""
import csv
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class DataManager:
    """Load and save profiles and BMI history from JSON files."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = Path(data_dir or Path(__file__).parent)
        self.profiles_path = self.data_dir / "profiles.json"
        self.history_path = self.data_dir / "history.json"
        self.profiles = self._load_json(self.profiles_path, [])
        self.history = self._load_json(self.history_path, [])

    def _load_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            return default

    def _save_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def save_profiles(self) -> None:
        self._save_json(self.profiles_path, self.profiles)

    def save_history(self) -> None:
        self._save_json(self.history_path, self.history)

    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        for profile in self.profiles:
            if profile.get("name", "").strip().lower() == name.strip().lower():
                return profile
        return None

    def add_profile(self, name: str, age: int, gender: str) -> Dict[str, Any]:
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if self.get_profile(name) is not None:
            raise ValueError("Profile already exists")
        profile = {"name": name.strip(), "age": int(age), "gender": gender}
        self.profiles.append(profile)
        self.save_profiles()
        return profile

    def get_profile_names(self) -> List[str]:
        return [profile["name"] for profile in self.profiles]

    def add_record(
        self,
        profile_name: str,
        weight: str,
        height: str,
        system: str,
        bmi: float,
        category: str,
        tip: str,
    ) -> Dict[str, Any]:
        record = {
            "id": uuid.uuid4().hex,
            "profile": profile_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": weight,
            "height": height,
            "system": system,
            "bmi": round(bmi, 2),
            "category": category,
            "tip": tip,
        }
        self.history.append(record)
        self.save_history()
        return record

    def get_history(self, profile_name: str) -> List[Dict[str, Any]]:
        return [record for record in self.history if record.get("profile") == profile_name]

    def delete_record(self, record_id: str) -> None:
        self.history = [record for record in self.history if record.get("id") != record_id]
        self.save_history()

    def clear_history(self, profile_name: str) -> None:
        self.history = [record for record in self.history if record.get("profile") != profile_name]
        self.save_history()

    def export_history_csv(self, profile_name: str, path: Path) -> None:
        records = self.get_history(profile_name)
        if not records:
            return
        with path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Weight", "Height", "System", "BMI", "Category", "Tip"])
            for record in records:
                writer.writerow(
                    [
                        record.get("date", ""),
                        record.get("weight", ""),
                        record.get("height", ""),
                        record.get("system", ""),
                        record.get("bmi", ""),
                        record.get("category", ""),
                        record.get("tip", ""),
                    ]
                )
