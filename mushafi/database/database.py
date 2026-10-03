import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path: str | Path = "mushafi.db"):
        self.db_path = str(db_path)
        self.init_db()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS surahs (
                    surah_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    ayah_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'unread',
                    memorization_status TEXT DEFAULT 'unread'
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS verses (
                    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_number INTEGER NOT NULL,
                    ayah_number INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    color_status TEXT DEFAULT 'unread',
                    memorization_status TEXT DEFAULT 'unread'
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS riwayat (
                    riwayah_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    source_file TEXT,
                    is_active INTEGER DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS readers (
                    reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    riwayah TEXT,
                    audio_path TEXT,
                    is_active INTEGER DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS surah_progress (
                    surah_id INTEGER PRIMARY KEY,
                    status TEXT DEFAULT 'unread',
                    memorized INTEGER DEFAULT 0,
                    reviewed INTEGER DEFAULT 0,
                    last_review TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS verse_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_number INTEGER NOT NULL,
                    ayah_number INTEGER NOT NULL,
                    status TEXT DEFAULT 'unread',
                    last_review TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah INTEGER NOT NULL,
                    ayah_start INTEGER NOT NULL,
                    ayah_end INTEGER NOT NULL,
                    due_date TEXT,
                    interval INTEGER DEFAULT 1,
                    mistakes INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    last_review TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bookmarks (
                    bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_number INTEGER NOT NULL,
                    ayah_number INTEGER NOT NULL,
                    label TEXT,
                    created_at TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_number INTEGER,
                    ayah_number INTEGER,
                    note TEXT NOT NULL,
                    updated_at TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS recitations (
                    recitation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah INTEGER NOT NULL,
                    ayah_start INTEGER NOT NULL,
                    ayah_end INTEGER NOT NULL,
                    created_at TEXT,
                    notes TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS recordings (
                    recording_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recitation_id INTEGER,
                    file_path TEXT NOT NULL,
                    created_at TEXT,
                    duration REAL DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS statistics (
                    stat_key TEXT PRIMARY KEY,
                    stat_value TEXT
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_verses_surah ON verses (surah_number, ayah_number)"
            )
            conn.commit()

            self.seed_surahs(cursor)
            self.seed_default_settings(cursor)
            conn.commit()
        finally:
            conn.close()

    def seed_surahs(self, cursor):
        surah_names = [
            "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة",
            "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم",
            "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت",
            "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر",
            "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات",
            "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر",
            "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم",
            "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات",
            "النبأ", "النازعات", "عبس", "التكوير", "الإنفطار", "المطففين", "الإنشقاق", "البروج", "الطارق",
            "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق",
            "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل",
            "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"
        ]
        for index, name in enumerate(surah_names, start=1):
            cursor.execute(
                "INSERT OR IGNORE INTO surahs (surah_id, name, ayah_count) VALUES (?, ?, 0)",
                (index, name),
            )

    def seed_default_settings(self, cursor):
        defaults = {
            "user_name": "مستخدم",
            "preferred_riwayah": "hafs",
            "preferred_reader": "",
            "font_size": "20",
            "night_mode": "0",
            "local_alerts": "1",
            "goal_memorization": "30",
            "goal_review": "10"
        }
        for key, value in defaults.items():
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, value),
            )

    def get_setting(self, key, default=None):
        with self.connect() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            if row is None:
                return default
            return row["value"]

    def set_setting(self, key, value):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, str(value)),
            )
            conn.commit()

    def execute(self, query, params=()):
        with self.connect() as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch_all(self, query, params=()):
        with self.connect() as conn:
            return conn.execute(query, params).fetchall()

    def fetch_one(self, query, params=()):
        with self.connect() as conn:
            return conn.execute(query, params).fetchone()
