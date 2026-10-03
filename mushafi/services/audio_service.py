import os
import subprocess
import sys
from pathlib import Path


class AudioService:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.audio_dir = self.base_dir / "assets" / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def ensure_audio_directory(self):
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def list_audio_files(self):
        files = []
        for item in sorted(self.audio_dir.rglob('*')):
            if item.is_file() and item.suffix.lower() in {'.mp3', '.wav', '.ogg', '.m4a'}:
                files.append(str(item))
        return files

    def record_local_audio(self, output_name: str, duration_seconds: int = 15):
        output = self.audio_dir / output_name
        output.parent.mkdir(parents=True, exist_ok=True)

        try:
            import sounddevice as sd
            import numpy as np

            fs = 44100
            recording = sd.rec(int(duration_seconds * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()
            wav_path = str(output.with_suffix('.wav'))
            import wave
            with wave.open(wav_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                samples = np.clip(recording, -1.0, 1.0)
                int_samples = (samples * 32767).astype('<i2')
                wf.writeframes(int_samples.tobytes())
            return wav_path
        except Exception:
            fallback = output.with_suffix('.txt')
            fallback.write_text(
                "Local recording stub created. Import verified audio file into assets/audio/ to play it in the app.",
                encoding='utf-8',
            )
            return str(fallback)

    def delete_recording(self, file_path: str):
        target = Path(file_path)
        if target.exists():
            target.unlink(missing_ok=True)
            return True
        return False
