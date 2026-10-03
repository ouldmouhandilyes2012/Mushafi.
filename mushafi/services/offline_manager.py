import json
from pathlib import Path


class OfflineManager:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)

    def list_quran_sources(self):
        base = self.base_dir / "assets" / "quran"
        results = []
        if base.exists():
            for item in sorted(base.iterdir()):
                if item.is_dir() and any(child.suffix in {".json", ".db"} for child in item.iterdir()):
                    results.append({"name": item.name, "path": str(item)})
        return results

    def list_tafsir_sources(self):
        base = self.base_dir / "assets" / "tafsir"
        results = []
        if base.exists():
            for item in sorted(base.iterdir()):
                if item.is_file() and item.suffix in {".json", ".db"}:
                    results.append({"name": item.name, "path": str(item), "size": item.stat().st_size})
        return results

    def list_local_audio(self):
        base = self.base_dir / "assets" / "audio"
        results = []
        if base.exists():
            for item in sorted(base.rglob("*")):
                if item.is_file() and item.suffix.lower() in {".mp3", ".wav", ".ogg", ".m4a"}:
                    results.append({"name": item.name, "path": str(item), "size": item.stat().st_size})
        return results

    def get_quran_import_template(self, rio_name: str):
        target = self.base_dir / "assets" / "quran" / rio_name
        target.mkdir(parents=True, exist_ok=True)
        file_path = target / f"{rio_name}.json"
        if not file_path.exists():
            file_path.write_text(
                json.dumps([
                    {"surah_number": 1, "surah_name": "الفاتحة", "ayah_number": 1, "text": "..."}
                ], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return str(file_path)

    def get_tafsir_import_template(self, name: str = "tafsir"):
        file_path = self.base_dir / "assets" / "tafsir" / f"{name}.json"
        if not file_path.exists():
            file_path.write_text(
                json.dumps([
                    {"surah_number": 1, "ayah_number": 1, "tafsir": "..."}
                ], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return str(file_path)
