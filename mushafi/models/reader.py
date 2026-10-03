from dataclasses import dataclass


@dataclass
class Reader:
    reader_id: int
    name: str
    riwayah: str = ""
    audio_path: str = ""
    is_active: int = 0
