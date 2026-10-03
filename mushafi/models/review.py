from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewItem:
    review_id: int
    surah: int
    ayah_start: int
    ayah_end: int
    due_date: str = ""
    interval: int = 1
    mistakes: int = 0
    success_count: int = 0
    last_review: str = ""
