# 📄 PDF Tool – DND Labs

**Auto-rotate · Compress · Merge PDF files**

A lightweight Windows desktop app to fix scanned PDFs: automatically detect and correct page rotation (90°, 180°, 270°), compress file size, and merge multiple PDFs into one. Built with Python & PyMuPDF.

---

## ✨ Features

- 🔄 **Auto-rotation correction** – detects whether pages are rotated 90°, 180° or 270° and corrects them losslessly
- 🗜️ **Compression** – typically saves 40–80% file size (garbage collection, deflate)
- 📎 **Merge** – combine multiple PDFs into one document, in any order
- 📁 **Flexible selection** – choose an entire folder or individual files directly
- ✅ **Exceptions** – exclude specific files from rotation
- 🖥️ **Simple GUI** – no terminal, no Python knowledge required (for the .exe version)

---

## 🚀 For End Users – Ready-to-use .exe (no Python required)

> **The easiest option:** Ready-made Windows app, works instantly with a double-click.

👉 **[Buy on Gumroad – €4.99](https://dndlabs.gumroad.com)**

Package includes:
- `PDF Tool User.exe` – runs immediately, no installation needed
- User manual as PDF

---

## 🛠️ For Developers – Build it yourself

### Requirements

```bash
pip install pymupdf pyinstaller
```

### Run from source

```bash
python PDF_Tool_Devs.py
```

### Build the .exe yourself

```bash
pyinstaller "PDF Tool User.spec"
```

Or simply double-click `exe_erstellen.bat` – automatically detects Anaconda.

The finished .exe will be in `dist\PDF Tool User.exe`.

---

## 📁 File Overview

| File | Description |
|------|-------------|
| `PDF_Tool_Devs.py` | Main file – GUI + logic in one file |
| `PDF Tool User.spec` | PyInstaller configuration |
| `exe_erstellen.bat` | Automatic build helper for Anaconda |

---

## 🔧 Tech Stack

| | |
|---|---|
| **Language** | Python 3.10+ |
| **PDF Library** | PyMuPDF (fitz) |
| **GUI** | Tkinter |
| **EXE Builder** | PyInstaller |

### Rotation correction (core logic)

```python
doc = fitz.open(str(path))
for nr in range(len(doc)):
    page = doc[nr]
    if page.rotation != 0:
        page.set_rotation(0)  # 90/180/270 → 0, lossless
doc.save(output, garbage=4, deflate=True, deflate_images=True,
         deflate_fonts=True, clean=True)
```

> `set_rotation(0)` corrects the PDF structure directly – no quality loss from pixel rendering.

---

## 💡 Possible Extensions

- OCR integration via `pytesseract`
- Drag & Drop support (tkinterdnd2)
- Page preview before rotation
- Password protection for output PDFs
- Migration to PyQt6/PySide6

---

## 📜 License

MIT License – free to use, modify and distribute the source code.

The **ready-made .exe** including DND Labs branding is commercial and not included in this repo.

---

<p align="center">
  © 2025 <a href="https://www.dndlabs.de">DND Labs UG (haftungsbeschränkt)</a> · Data · Nimbus · Dickl
</p>
