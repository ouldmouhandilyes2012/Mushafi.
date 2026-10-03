import sqlite3
from pathlib import Path


class MigrationManager:
    """Simple migration scaffold for future expansion."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def run_migrations(self):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL DEFAULT 1)"
            )
            cursor.execute("SELECT version FROM schema_version LIMIT 1")
            row = cursor.fetchone()
            if row is None:
                cursor.execute("INSERT INTO schema_version (version) VALUES (1)")
            conn.commit()
        finally:
            conn.close()
