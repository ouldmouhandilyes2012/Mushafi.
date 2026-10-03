from dataclasses import dataclass


@dataclass
class Surah:
    surah_id: int
    name: str
    ayah_count: int = 0
    status: str = "unread"
    memorization_status: str = "unread"
