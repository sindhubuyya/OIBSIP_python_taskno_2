Advanced BMI Calculator
This is a beginner-friendly BMI Calculator desktop app built with CustomTkinter and Matplotlib.

Quick start
From C:\Users\BUYYA SINDHU\OneDrive\Documents:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r bmi_calculator/requirements.txt
python -m bmi_calculator.main
Features
Profile registration and loading
Metric and Imperial calculators
BMI history with search, sort, delete, and CSV export
Dashboard analytics with charts
JSON-based persistent storage
Modern dark theme and beginner-friendly layout
Notes
The app stores profiles in profiles.json and history in history.json inside the bmi_calculator folder.

Packaging into a single executable (Windows):

Install PyInstaller (already included in requirements.txt):
pip install pyinstaller
Create a single-file build (from project root):
pyinstaller --onefile --windowed --add-data "bmi_data.db;." bmi_calculator/main.py
The produced executable will be in the dist folder.
