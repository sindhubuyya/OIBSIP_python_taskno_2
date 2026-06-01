import os
import tempfile

from bmi_calculator.database.db_manager import DBManager


def test_db_create_and_user_and_record():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = DBManager(path)
        user = db.add_user("tester", 40, "Other")
        assert user.username == "tester"
        rec = db.add_bmi_record(user.id, 70.0, 1.75, 22.86, "Normal weight")
        records = db.get_records_for_user(user.id)
        assert len(records) == 1
        stats = db.stats_for_user(user.id)
        assert stats["count"] == 1
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
