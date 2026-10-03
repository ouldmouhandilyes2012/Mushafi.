from dataclasses import dataclass


@dataclass
class Riwayah:
    riwayah_id: int
    name: str
    source_file: str = ""
    is_active: int = 0
