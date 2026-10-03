from datetime import datetime


class RecitationEngine:
    def __init__(self, database):
        self.db = database

    def add_recitation(self, surah, ayah_start, ayah_end, notes=""):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute(
            "INSERT INTO recitations (surah, ayah_start, ayah_end, created_at, notes) VALUES (?, ?, ?, ?, ?)",
            (surah, ayah_start, ayah_end, now, notes),
        )
        row = self.db.fetch_one(
            "SELECT recitation_id FROM recitations WHERE surah = ? AND ayah_start = ? AND ayah_end = ? AND created_at = ? ORDER BY recitation_id DESC LIMIT 1",
            (surah, ayah_start, ayah_end, now),
        )
        if row is not None:
            return row["recitation_id"]
        return None

    def add_recording(self, recitation_id, file_path, duration=0.0):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute(
            "INSERT INTO recordings (recitation_id, file_path, created_at, duration) VALUES (?, ?, ?, ?)",
            (recitation_id, file_path, now, duration),
        )

    def list_recitations(self):
        return self.db.fetch_all(
            "SELECT recitation_id, surah, ayah_start, ayah_end, created_at, notes FROM recitations ORDER BY recitation_id DESC"
        )

    def list_recordings(self):
        return self.db.fetch_all(
            "SELECT recording_id, recitation_id, file_path, created_at, duration FROM recordings ORDER BY recording_id DESC"
        )
