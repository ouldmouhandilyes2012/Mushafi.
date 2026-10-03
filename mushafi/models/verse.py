from dataclasses import dataclass


@dataclass
class Verse:
    verse_id: int
    surah_number: int
    ayah_number: int
    text: str = ""
    color_status: str = "unread"
    memorization_status: str = "unread"
