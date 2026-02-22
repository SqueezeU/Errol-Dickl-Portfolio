"""
PDF Tool - GUI App
Tkinter-basierte Oberfläche für PDF drehen, komprimieren, zusammenführen
"""

import sys
import os
import threading
from pathlib import Path

def install_requirements():
    import subprocess
    for pkg in ["pymupdf"]:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import fitz
except ImportError:
    install_requirements()
    import fitz

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

A4_WIDTH  = int(595 * 0.75)
A4_HEIGHT = int(842 * 0.75)


def verarbeite_pdfs(ordner: Path, ausnahmen: list, ausgabe_ordner: Path, log_callback):
    pdfs = sorted(ordner.glob("*.pdf"))
    if not pdfs:
        log_callback("❌ Keine PDFs gefunden!\n")
        return

    ausgabe_ordner.mkdir(exist_ok=True)
    log_callback(f"✅ {len(pdfs)} PDF(s) gefunden...\n")

    for pdf in pdfs:
        drehen = pdf.name not in ausnahmen
        info = "180° gedreht" if drehen else "nicht gedreht (Ausnahme)"
        log_callback(f"⏳ {pdf.name} – {info}...")

        try:
            ausgabe = ausgabe_ordner / pdf.name
            doc = fitz.open(str(pdf))
            neues_doc = fitz.open()
            for nr in range(len(doc)):
                seite = doc[nr]
                winkel = 180 if drehen else 0
                matrix = fitz.Matrix(2, 2).prerotate(winkel)
                pix = seite.get_pixmap(matrix=matrix, alpha=False)
                if pix.width > pix.height:
                    zb, zh = A4_HEIGHT, A4_WIDTH
                else:
                    zb, zh = A4_WIDTH, A4_HEIGHT
                neue_seite = neues_doc.new_page(width=zb, height=zh)
                neue_seite.insert_image(neue_seite.rect, pixmap=pix)
            neues_doc.save(str(ausgabe), garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True)
            neues_doc.close()
            doc.close()

            vorher = pdf.stat().st_size
            nachher = ausgabe.stat().st_size
            ersparnis = (1 - nachher / vorher) * 100
            log_callback(f" ✅ {nachher/1_048_576:.1f} MB ({ersparnis:.0f}% kleiner)\n")
        except Exception as e:
            log_callback(f" ❌ Fehler: {e}\n")

    log_callback(f"\n📁 Fertig! Dateien in: {ausgabe_ordner}\n")


def fuehre_zusammen(ordner: Path, reihenfolge: list, ausgabename: str, log_callback):
    if reihenfolge:
        dateiliste = [ordner / name.strip() for name in reihenfolge if name.strip()]
    else:
        dateiliste = sorted(ordner.glob("*.pdf"))
        dateiliste = [f for f in dateiliste if f.name != ausgabename]

    if not dateiliste:
        log_callback("❌ Keine PDFs gefunden!\n")
        return

    log_callback(f"Füge {len(dateiliste)} PDFs zusammen...\n")
    neues_doc = fitz.open()

    for pfad in dateiliste:
        if not pfad.exists():
            log_callback(f"   ❌ Nicht gefunden: {pfad.name}\n")
            continue
        doc = fitz.open(str(pfad))
        neues_doc.insert_pdf(doc)
        doc.close()
        log_callback(f"   ✅ {pfad.name}\n")

    ausgabe = ordner / ausgabename
    neues_doc.save(str(ausgabe), garbage=4, deflate=True, clean=True)
    neues_doc.close()
    log_callback(f"\n📄 Gespeichert als: {ausgabe.name}  ({ausgabe.stat().st_size/1_048_576:.1f} MB)\n")


class PDFToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tool")
        self.geometry("700x600")
        self.resizable(True, True)
        self.configure(bg="#f0f0f0")

        # Farben
        self.blau   = "#2563EB"
        self.hell   = "#EFF6FF"
        self.gruen  = "#16A34A"
        self.grau   = "#6B7280"

        self._build_ui()

    def _build_ui(self):
        # Titel
        tk.Label(self, text="📄 PDF Tool", font=("Segoe UI", 20, "bold"),
                 bg="#f0f0f0", fg="#1e1e1e").pack(pady=(20, 4))
        tk.Label(self, text="Drehen · Komprimieren · Zusammenführen",
                 font=("Segoe UI", 10), bg="#f0f0f0", fg=self.grau).pack(pady=(0, 16))

        # Notebook (Tabs)
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[12, 6])
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._tab_drehen(nb)
        self._tab_zusammen(nb)

    # ── TAB 1: Drehen & Komprimieren ─────────────────────────────
    def _tab_drehen(self, nb):
        frame = tk.Frame(nb, bg="#f0f0f0")
        nb.add(frame, text="  🔄  Drehen & Komprimieren  ")

        # Ordner wählen
        tk.Label(frame, text="PDF-Ordner:", font=("Segoe UI", 10, "bold"),
                 bg="#f0f0f0").pack(anchor="w", padx=20, pady=(16, 2))
        ordner_frame = tk.Frame(frame, bg="#f0f0f0")
        ordner_frame.pack(fill="x", padx=20)
        self.dreh_ordner = tk.StringVar()
        tk.Entry(ordner_frame, textvariable=self.dreh_ordner, font=("Segoe UI", 10),
                 width=50).pack(side="left", fill="x", expand=True)
        tk.Button(ordner_frame, text="Durchsuchen", command=self._waehle_dreh_ordner,
                  bg=self.blau, fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=10).pack(side="left", padx=(6, 0))

        # Ausnahmen
        tk.Label(frame, text="Ausnahmen (nicht drehen) – eine Datei pro Zeile:",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(14, 2))
        tk.Label(frame, text="z.B.:  Seite 2.pdf   oder leer lassen wenn alle gedreht werden sollen",
                 font=("Segoe UI", 9), bg="#f0f0f0", fg=self.grau).pack(anchor="w", padx=20)
        self.ausnahmen_text = tk.Text(frame, height=4, font=("Segoe UI", 10),
                                      relief="solid", bd=1)
        self.ausnahmen_text.pack(fill="x", padx=20, pady=(4, 0))

        # Start-Button
        tk.Button(frame, text="▶  Starten", command=self._starte_drehen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=14)

        # Log
        self.dreh_log = self._log_widget(frame)

    def _tab_zusammen(self, nb):
        frame = tk.Frame(nb, bg="#f0f0f0")
        nb.add(frame, text="  📎  Zusammenführen  ")

        tk.Label(frame, text="PDF-Ordner:", font=("Segoe UI", 10, "bold"),
                 bg="#f0f0f0").pack(anchor="w", padx=20, pady=(16, 2))
        ordner_frame = tk.Frame(frame, bg="#f0f0f0")
        ordner_frame.pack(fill="x", padx=20)
        self.zus_ordner = tk.StringVar()
        tk.Entry(ordner_frame, textvariable=self.zus_ordner, font=("Segoe UI", 10),
                 width=50).pack(side="left", fill="x", expand=True)
        tk.Button(ordner_frame, text="Durchsuchen", command=self._waehle_zus_ordner,
                  bg=self.blau, fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=10).pack(side="left", padx=(6, 0))

        tk.Label(frame, text="Reihenfolge (eine Datei pro Zeile, leer = alphabetisch alle):",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(14, 2))
        tk.Label(frame, text="z.B.:  Seite 1.pdf  /  Seite 2.pdf  /  ...",
                 font=("Segoe UI", 9), bg="#f0f0f0", fg=self.grau).pack(anchor="w", padx=20)
        self.reihenfolge_text = tk.Text(frame, height=5, font=("Segoe UI", 10),
                                        relief="solid", bd=1)
        self.reihenfolge_text.pack(fill="x", padx=20, pady=(4, 0))

        tk.Label(frame, text="Name der fertigen Datei:",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(12, 2))
        self.ausgabename = tk.StringVar(value="Zusammengefuehrt.pdf")
        tk.Entry(frame, textvariable=self.ausgabename, font=("Segoe UI", 10),
                 width=40, relief="solid", bd=1).pack(anchor="w", padx=20)

        tk.Button(frame, text="▶  Zusammenführen", command=self._starte_zusammen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=14)

        self.zus_log = self._log_widget(frame)

    def _log_widget(self, parent):
        log = tk.Text(parent, height=8, font=("Consolas", 9), bg="#1e1e1e",
                      fg="#d4d4d4", relief="flat", state="disabled")
        log.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        return log

    def _log(self, widget, text):
        widget.config(state="normal")
        widget.insert("end", text)
        widget.see("end")
        widget.config(state="disabled")
        self.update_idletasks()

    def _waehle_dreh_ordner(self):
        d = filedialog.askdirectory()
        if d:
            self.dreh_ordner.set(d)

    def _waehle_zus_ordner(self):
        d = filedialog.askdirectory()
        if d:
            self.zus_ordner.set(d)

    def _starte_drehen(self):
        ordner = Path(self.dreh_ordner.get())
        if not ordner.exists():
            messagebox.showerror("Fehler", "Bitte einen gültigen Ordner auswählen.")
            return
        ausnahmen = [z.strip() for z in self.ausnahmen_text.get("1.0", "end").splitlines() if z.strip()]
        ausgabe = ordner / "komprimiert"
        self.dreh_log.config(state="normal"); self.dreh_log.delete("1.0", "end"); self.dreh_log.config(state="disabled")
        threading.Thread(target=verarbeite_pdfs,
                         args=(ordner, ausnahmen, ausgabe, lambda t: self._log(self.dreh_log, t)),
                         daemon=True).start()

    def _starte_zusammen(self):
        ordner = Path(self.zus_ordner.get())
        if not ordner.exists():
            messagebox.showerror("Fehler", "Bitte einen gültigen Ordner auswählen.")
            return
        reihenfolge = [z.strip() for z in self.reihenfolge_text.get("1.0", "end").splitlines() if z.strip()]
        ausgabename = self.ausgabename.get().strip() or "Zusammengefuehrt.pdf"
        self.zus_log.config(state="normal"); self.zus_log.delete("1.0", "end"); self.zus_log.config(state="disabled")
        threading.Thread(target=fuehre_zusammen,
                         args=(ordner, reihenfolge, ausgabename, lambda t: self._log(self.zus_log, t)),
                         daemon=True).start()


if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()
