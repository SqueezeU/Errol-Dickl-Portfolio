# 📄 PDF Tool – DND Labs

**PDFs automatisch korrigieren · komprimieren · zusammenführen**

A lightweight Windows desktop app to fix scanned PDFs: automatically detect and correct page rotation (90°, 180°, 270°), compress file size, and merge multiple PDFs into one. Built with Python & PyMuPDF.

---

## ✨ Features

- 🔄 **Automatische Rotationskorrektur** – erkennt ob Seiten 90°, 180° oder 270° gedreht sind und korrigiert sie verlustfrei
- 🗜️ **Komprimierung** – spart typischerweise 40–80% Dateigröße (garbage collection, deflate)
- 📎 **Zusammenführen** – mehrere PDFs zu einem Dokument, in beliebiger Reihenfolge
- 📁 **Flexible Auswahl** – ganzen Ordner oder einzelne Dateien direkt auswählen
- ✅ **Ausnahmen** – bestimmte Dateien vom Drehen ausschließen
- 🖥️ **Einfache GUI** – kein Terminal, kein Python-Wissen nötig (für die .exe Version)

---

## 🚀 Für Endnutzer – Fertige .exe (kein Python nötig)

> **Die einfachste Option:** Fertige Windows-App, sofort nutzbar per Doppelklick.

👉 **[Jetzt auf Gumroad kaufen – €4,99](https://dndlabs.gumroad.com)**

Im Paket enthalten:
- `PDF Tool User.exe` – startet sofort, keine Installation
- Benutzerhandbuch als PDF

---

## 🛠️ Für Entwickler – Selbst bauen

### Voraussetzungen

```bash
pip install pymupdf pyinstaller
```

### Direkt aus dem Quellcode starten

```bash
python PDF_Tool_Devs.py
```

### .exe selbst bauen

```bash
pyinstaller "PDF Tool User.spec"
```

Oder einfach `exe_erstellen.bat` doppelklicken – erkennt Anaconda automatisch.

Die fertige .exe liegt danach in `dist\PDF Tool User.exe`.

---

## 📁 Dateiübersicht

| Datei | Beschreibung |
|-------|-------------|
| `PDF_Tool_Devs.py` | Hauptdatei – GUI + Logik in einer Datei |
| `PDF Tool User.spec` | PyInstaller Konfiguration |
| `exe_erstellen.bat` | Automatischer Build-Helper für Anaconda |

---

## 🔧 Technischer Stack

| | |
|---|---|
| **Sprache** | Python 3.10+ |
| **PDF-Bibliothek** | PyMuPDF (fitz) |
| **GUI** | Tkinter |
| **EXE-Builder** | PyInstaller |

### Rotationskorrektur (Kernlogik)

```python
doc = fitz.open(str(pfad))
for nr in range(len(doc)):
    seite = doc[nr]
    if seite.rotation != 0:
        seite.set_rotation(0)  # 90/180/270 → 0, verlustfrei
doc.save(ausgabe, garbage=4, deflate=True, deflate_images=True,
         deflate_fonts=True, clean=True)
```

> `set_rotation(0)` korrigiert die PDF-Struktur direkt – kein Qualitätsverlust durch Pixel-Rendering.

---

## 💡 Mögliche Erweiterungen

- OCR-Integration via `pytesseract`
- Drag & Drop (tkinterdnd2)
- Seitenvorschau vor dem Drehen
- Passwortschutz für Ausgabe-PDFs
- Migration zu PyQt6/PySide6

---

## 📜 Lizenz

MIT License – freie Nutzung, Änderung und Weitergabe des Quellcodes.

Die **fertige .exe** inklusive DND Labs Branding ist kommerziell und nicht im Repo enthalten.

---

<p align="center">
  © 2025 <a href="https://www.dndlabs.de">DND Labs UG (haftungsbeschränkt)</a> · Data · Nimbus · Dickl
</p>
