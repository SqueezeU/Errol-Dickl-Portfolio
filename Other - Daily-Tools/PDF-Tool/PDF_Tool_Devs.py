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


def verarbeite_pdfs(dateien: list, ausgabe_ordner: Path, ausnahmen: list, log_callback):
    if not dateien:
        log_callback("❌ Keine PDFs ausgewählt!\n")
        return

    ausgabe_ordner.mkdir(exist_ok=True)
    log_callback(f"✅ {len(dateien)} PDF(s) wird verarbeitet...\n")

    for pfad in dateien:
        pfad = Path(pfad)
        drehen = pfad.name not in ausnahmen
        info = "180° gedreht" if drehen else "nicht gedreht (Ausnahme)"
        log_callback(f"⏳ {pfad.name} – {info}...")

        try:
            ausgabe = ausgabe_ordner / pfad.name
            doc = fitz.open(str(pfad))
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

            vorher = pfad.stat().st_size
            nachher = ausgabe.stat().st_size
            ersparnis = (1 - nachher / vorher) * 100
            log_callback(f" ✅ {nachher/1_048_576:.1f} MB ({ersparnis:.0f}% kleiner)\n")
        except Exception as e:
            log_callback(f" ❌ Fehler: {e}\n")

    log_callback(f"\n📁 Fertig! Dateien in: {ausgabe_ordner}\n")


def fuehre_zusammen(dateien: list, ordner: Path, ausgabename: str, log_callback):
    if not dateien:
        log_callback("❌ Keine PDFs ausgewählt!\n")
        return

    log_callback(f"Füge {len(dateien)} PDFs zusammen...\n")
    neues_doc = fitz.open()

    for pfad in dateien:
        pfad = Path(pfad)
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


class DateiListe(tk.Frame):
    """Wiederverwendbare Dateiliste mit Checkboxen und Drag-Reihenfolge"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#f0f0f0", **kwargs)
        self.vars = {}   # filename -> BooleanVar
        self.order = []  # Reihenfolge der Dateien
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg="#f0f0f0")
        header.pack(fill="x")
        tk.Button(header, text="☑ Alle", font=("Segoe UI", 9),
                  bg="#e5e7eb", relief="flat", padx=8, pady=3,
                  command=self.alle_auswaehlen).pack(side="left", padx=(0,4))
        tk.Button(header, text="☐ Keine", font=("Segoe UI", 9),
                  bg="#e5e7eb", relief="flat", padx=8, pady=3,
                  command=self.keine_auswaehlen).pack(side="left")

        # Scrollbare Liste
        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(fill="both", expand=True, pady=(6,0))

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=1,
                                highlightbackground="#d1d5db")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.liste_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.liste_frame, anchor="nw")
        self.liste_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas.itemconfig(self.canvas_window, width=e.width)

    def lade_ordner(self, ordner: Path):
        """Lädt alle PDFs aus einem Ordner"""
        for widget in self.liste_frame.winfo_children():
            widget.destroy()
        self.vars.clear()
        self.order.clear()

        pdfs = sorted(ordner.glob("*.pdf"))
        if not pdfs:
            tk.Label(self.liste_frame, text="Keine PDFs gefunden",
                     font=("Segoe UI", 10), bg="white", fg="#9ca3af").pack(pady=20)
            return

        for i, pdf in enumerate(pdfs):
            var = tk.BooleanVar(value=True)
            self.vars[str(pdf)] = var
            self.order.append(str(pdf))

            zeile = tk.Frame(self.liste_frame, bg="white" if i % 2 == 0 else "#f9fafb")
            zeile.pack(fill="x")

            cb = tk.Checkbutton(zeile, variable=var, bg=zeile["bg"],
                                activebackground=zeile["bg"])
            cb.pack(side="left", padx=(8, 0))

            groesse = pdf.stat().st_size / 1_048_576
            tk.Label(zeile, text=pdf.name, font=("Segoe UI", 10),
                     bg=zeile["bg"], anchor="w").pack(side="left", fill="x",
                     expand=True, padx=(4,0), pady=6)
            tk.Label(zeile, text=f"{groesse:.1f} MB", font=("Segoe UI", 9),
                     bg=zeile["bg"], fg="#6b7280").pack(side="right", padx=12)

    def alle_auswaehlen(self):
        for var in self.vars.values():
            var.set(True)

    def keine_auswaehlen(self):
        for var in self.vars.values():
            var.set(False)

    def get_ausgewaehlt(self):
        """Gibt die ausgewählten Dateipfade zurück"""
        return [p for p in self.order if self.vars.get(p, tk.BooleanVar()).get()]

    def get_ordner(self):
        if self.order:
            return Path(self.order[0]).parent
        return None


class PDFToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tool")
        self.geometry("750x680")
        self.resizable(True, True)
        self.configure(bg="#f0f0f0")

        self.blau   = "#2563EB"
        self.hell   = "#EFF6FF"
        self.gruen  = "#16A34A"
        self.grau   = "#6B7280"

        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="📄 PDF Tool", font=("Segoe UI", 20, "bold"),
                 bg="#f0f0f0", fg="#1e1e1e").pack(pady=(20, 4))
        tk.Label(self, text="Drehen · Komprimieren · Zusammenführen",
                 font=("Segoe UI", 10), bg="#f0f0f0", fg=self.grau).pack(pady=(0, 16))

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[12, 6])
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._tab_drehen(nb)
        self._tab_zusammen(nb)

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

        # Dateiliste
        tk.Label(frame, text="PDFs im Ordner – Auswahl per Checkbox:",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(14, 2))
        self.dreh_liste = DateiListe(frame, height=160)
        self.dreh_liste.pack(fill="x", padx=20, ipady=0)

        # Ausnahmen
        tk.Label(frame, text="Nicht drehen (Dateinamen, eine pro Zeile):",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(10, 2))
        self.ausnahmen_text = tk.Text(frame, height=3, font=("Segoe UI", 10),
                                      relief="solid", bd=1)
        self.ausnahmen_text.pack(fill="x", padx=20, pady=(0, 0))

        tk.Button(frame, text="▶  Starten", command=self._starte_drehen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=10)

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

        # Dateiliste
        tk.Label(frame, text="PDFs im Ordner – Reihenfolge per Checkbox wählen:",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(14, 2))
        tk.Label(frame, text="Die Reihenfolge in der Liste bestimmt die Reihenfolge im Ergebnis",
                 font=("Segoe UI", 9), bg="#f0f0f0", fg=self.grau).pack(anchor="w", padx=20)
        self.zus_liste = DateiListe(frame, height=180)
        self.zus_liste.pack(fill="x", padx=20)

        tk.Label(frame, text="Name der fertigen Datei:",
                 font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(10, 2))
        self.ausgabename = tk.StringVar(value="Zusammengefuehrt.pdf")
        tk.Entry(frame, textvariable=self.ausgabename, font=("Segoe UI", 10),
                 width=40, relief="solid", bd=1).pack(anchor="w", padx=20)

        tk.Button(frame, text="▶  Zusammenführen", command=self._starte_zusammen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=10)

        self.zus_log = self._log_widget(frame)

    def _log_widget(self, parent):
        log = tk.Text(parent, height=6, font=("Consolas", 9), bg="#1e1e1e",
                      fg="#d4d4d4", relief="flat", state="disabled")
        log.pack(fill="both", expand=True, padx=20, pady=(0, 12))
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
            self.dreh_liste.lade_ordner(Path(d))

    def _waehle_zus_ordner(self):
        d = filedialog.askdirectory()
        if d:
            self.zus_ordner.set(d)
            self.zus_liste.lade_ordner(Path(d))

    def _starte_drehen(self):
        ausgewaehlt = self.dreh_liste.get_ausgewaehlt()
        if not ausgewaehlt:
            messagebox.showerror("Fehler", "Bitte mindestens eine PDF auswählen.")
            return
        ordner = Path(ausgewaehlt[0]).parent
        ausgabe = ordner / "komprimiert"
        ausnahmen = [z.strip() for z in self.ausnahmen_text.get("1.0", "end").splitlines() if z.strip()]
        self.dreh_log.config(state="normal"); self.dreh_log.delete("1.0", "end"); self.dreh_log.config(state="disabled")
        threading.Thread(target=verarbeite_pdfs,
                         args=(ausgewaehlt, ausgabe, ausnahmen, lambda t: self._log(self.dreh_log, t)),
                         daemon=True).start()

    def _starte_zusammen(self):
        ausgewaehlt = self.zus_liste.get_ausgewaehlt()
        if not ausgewaehlt:
            messagebox.showerror("Fehler", "Bitte mindestens eine PDF auswählen.")
            return
        ordner = Path(ausgewaehlt[0]).parent
        ausgabename = self.ausgabename.get().strip() or "Zusammengefuehrt.pdf"
        self.zus_log.config(state="normal"); self.zus_log.delete("1.0", "end"); self.zus_log.config(state="disabled")
        threading.Thread(target=fuehre_zusammen,
                         args=(ausgewaehlt, ordner, ausgabename, lambda t: self._log(self.zus_log, t)),
                         daemon=True).start()


if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()
