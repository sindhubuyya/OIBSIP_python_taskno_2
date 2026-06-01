"""Data models for users and BMI records."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    age: int
    gender: str


@dataclass
class BMIRecord:
    id: Optional[int]
    user_id: int
    weight_kg: float
    height_m: float
    bmi: float
    category: str
    recorded_at: Optional[str] = None
