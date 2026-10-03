from datetime import datetime, timedelta


class ReviewEngine:
    def __init__(self, database):
        self.db = database

    def build_review_queue(self):
        rows = self.db.fetch_all(
            "SELECT surah, ayah_start, ayah_end, due_date, interval, mistakes, success_count, last_review FROM reviews ORDER BY due_date ASC"
        )
        return [dict(r) for r in rows]

    def add_or_update_review(self, surah, ayah_start=1, ayah_end=1, interval=1, mistakes=0, success_count=0):
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.execute(
            "INSERT INTO reviews (surah, ayah_start, ayah_end, due_date, interval, mistakes, success_count, last_review) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (surah, ayah_start, ayah_end, today, interval, mistakes, success_count, today),
        )

    def update_review_after_recitation(self, surah, mistakes):
        row = self.db.fetch_one(
            "SELECT * FROM reviews WHERE surah = ? ORDER BY review_id DESC LIMIT 1",
            (surah,),
        )
        if row is None:
            self.add_or_update_review(surah, mistakes=mistakes, success_count=1 if mistakes == 0 else 0)
            return
        new_interval = row["interval"]
        if mistakes == 0:
            new_interval = max(3, row["interval"] + 2)
            success_count = row["success_count"] + 1
        else:
            new_interval = max(1, row["interval"] // 2)
            success_count = max(0, row["success_count"] - 1)
        due_date = (datetime.now() + timedelta(days=new_interval)).strftime("%Y-%m-%d")
        self.db.execute(
            "UPDATE reviews SET due_date = ?, interval = ?, mistakes = ?, success_count = ?, last_review = ? WHERE review_id = ?",
            (due_date, new_interval, mistakes, success_count, datetime.now().strftime("%Y-%m-%d"), row["review_id"]),
        )

    def stats(self):
        total = self.db.fetch_one("SELECT COUNT(*) as total FROM reviews")["total"]
        due_today = self.db.fetch_one("SELECT COUNT(*) as total FROM reviews WHERE due_date <= date('now')")["total"]
        delayed = self.db.fetch_one("SELECT COUNT(*) as total FROM reviews WHERE due_date < date('now')")["total"]
        return {"total": total, "due_today": due_today, "delayed": delayed}
