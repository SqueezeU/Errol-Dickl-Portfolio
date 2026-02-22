# run_whisper_auto.py
import os
import whisper
from pathlib import Path

print("🔁 Starte automatische Transkription...")

# 1. Basisverzeichnis berechnen
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "audio_nuevo"
OUTPUT_DIR = BASE_DIR / "transcripts"

# 2. Ausgabeordner sicherstellen
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Whisper-Modell laden (lokal)
print("📥 Lade Whisper-Modell...")
model = whisper.load_model("base")

# 4. Alle Audiodateien im Ordner durchgehen
audio_files = list(AUDIO_DIR.glob("*.wav")) + list(AUDIO_DIR.glob("*.mp3"))

if not audio_files:
    print("⚠️ Keine Audiodateien im Verzeichnis gefunden.")
else:
    for file_path in audio_files:
        print(f"🎧 Verarbeite: {file_path.name}")

        # 5. Transkription starten
        result = model.transcribe(str(file_path))

        # 6. Speichern unter dem gleichen Namen, aber als .txt
        output_file = OUTPUT_DIR / (file_path.stem + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"✅ Transkript gespeichert unter: {output_file.name}")

print("🏁 Alle Dateien verarbeitet.")
