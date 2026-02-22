# 📄 PDF Tool

**Rotate · Compress · Merge PDF files — no technical knowledge required**

A lightweight Windows desktop app to fix scanned PDFs: rotate upside-down pages, compress file size, and merge multiple PDFs into one. Built with Python & PyMuPDF.

---

## ✨ Features

- 🔄 Rotate all pages by 180° (with optional exceptions per file)
- 📦 Compress PDFs and normalize to 75% DIN A4
- 📎 Merge multiple PDFs into a single document — in any order
- 🖥️ Simple GUI — no command line needed

---

## 🚀 For End Users (no Python required)

👉 Available on request — contact us at [dndlabs.de](https://www.dndlabs.de)

---

## 🛠️ For Developers

### Requirements
```bash
pip install pymupdf pyinstaller
```

### Run from source
```bash
python pdf_tool_devs.py
```

### Build the .exe yourself
```bash
pyinstaller --onefile --windowed --name "PDF Tool" pdf_tool_devs.py
```
Or just double-click `exe_erstellen.bat`.

### File overview

| File | Description |
|------|-------------|
| `pdf_tool_devs.py` | Main app — GUI + all logic in one file |
| `exe_erstellen.bat` | Builds the .exe via PyInstaller |

### How it works

Each page is rendered as a high-res pixel image (2x scale = 144 dpi) using PyMuPDF. This approach correctly resolves any embedded PDF rotation values before applying the 180° flip. Pages are then saved at 75% DIN A4 with maximum compression flags.

**Key settings to customize:**
```python
A4_WIDTH  = int(595 * 0.75)   # Output width  — change 0.75 for different scale
A4_HEIGHT = int(842 * 0.75)   # Output height

# Compression flags in neues_doc.save():
garbage=4, deflate=True, deflate_images=True, deflate_fonts=True
```

### Possible extensions
- OCR integration via `pytesseract`
- Drag & Drop via `tkinterdnd2`
- Page preview before rotation
- Password protection for output PDFs
- Auto-rotation detection via Tesseract OSD

---

## 📋 License

Free to use and modify. Built by [DND Labs](https://www.dndlabs.de)
