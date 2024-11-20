import tkinter as tk
from tkinter import ttk
import time
import threading

import get_info

# Aggiornamento dei dati
def update_info():
    global last_update_label
    ink_levels, paper_levels = get_info.get_info()
    if ink_levels and paper_levels:
        # Aggiorna testo e barre del toner
        for color, value in zip(["Black", "Cyan", "Magenta", "Yellow"], ink_levels):
            toner_labels[color].set(f"{color}: {value:.0f}%")
            toner_bars[color]["value"] = value  # Imposta il valore della barra

        # Aggiorna testo dei vassoi
        tray_labels[1].set(f"Vassoio 1 - A4: {paper_levels[0]}%")
        tray_labels[2].set(f"Vassoio 2 - A4: {paper_levels[1]}%")
        tray_labels[3].set(f"Vassoio 3 - A3: {paper_levels[2]}%")

        # Aggiorna il timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        last_update_label.set(f"Aggiornato: {timestamp}")
    else:
        last_update_label.set("Errore durante l'aggiornamento")

# Aggiornamento automatico ogni 30 minuti
def auto_update():
    while True:
        time.sleep(30 * 60)
        update_info()

# Interfaccia Grafica
root = tk.Tk()
root.title("RICOH IM C3010")
root.geometry("250x340")
root.resizable(False,False)

# Layout
frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Configura uno stile per ogni colore della progress bar
style = ttk.Style()
style.theme_use("default")  # Usa il tema base per personalizzazioni

# Stili per i diversi colori
style.configure("Black.Horizontal.TProgressbar", troughcolor="white", background="black")
style.configure("Cyan.Horizontal.TProgressbar", troughcolor="white", background="cyan")
style.configure("Magenta.Horizontal.TProgressbar", troughcolor="white", background="magenta")
style.configure("Yellow.Horizontal.TProgressbar", troughcolor="white", background="yellow")

# Sezione toner con miglior allineamento
ttk.Label(frame, text="Livelli Toner", font=("Arial", 14, "bold")).pack(pady=5)
toner_labels = {}
toner_bars = {}

for i, color in enumerate(["Black", "Cyan", "Magenta", "Yellow"]):
    # Frame per organizzare label e barra
    frame_toner = ttk.Frame(frame)
    frame_toner.pack(fill="x", pady=2, padx=10)
    
    # Label per il testo con la percentuale (fissa a sinistra)
    toner_labels[color] = tk.StringVar(value=f"{color}: ---")
    label = ttk.Label(frame_toner, textvariable=toner_labels[color], font=("Arial", 10), width=12, anchor="w")
    label.grid(row=0, column=0, padx=5, sticky="w")
    
    # Barra per rappresentare graficamente il livello (espandibile)
    toner_bars[color] = ttk.Progressbar(
        frame_toner, orient="horizontal", length=100, mode="determinate",
        style=f"{color}.Horizontal.TProgressbar"
    )
    toner_bars[color].grid(row=0, column=1, padx=5, sticky="ew")
    
    # Configura la colonna 1 per essere ridimensionabile
    frame_toner.columnconfigure(1, weight=1)

# Sezione vassoi
ttk.Label(frame, text="Livelli Carta", font=("Arial", 14, "bold")).pack(pady=10)
tray_labels = {}
for i in range(1, 4):
    tray_labels[i] = tk.StringVar(value=f"Vassoio {i}: ---")
    ttk.Label(frame, textvariable=tray_labels[i], font=("Arial", 12)).pack(anchor="w", padx=20)

# Timestamp ultimo aggiornamento OK
last_update_label = tk.StringVar(value="Ultimo aggiornamento: ---")
ttk.Label(frame, textvariable=last_update_label, font=("Arial", 10, "italic")).pack(pady=10)

# Pulsante aggiorna OK
ttk.Button(frame, text="AGGIORNA", command=update_info).pack(pady=10)

# Thread per aggiornamento automatico
threading.Thread(target=auto_update, daemon=True).start()

# Avvia l'interfaccia grafica
update_info()  # Aggiorna i dati all'avvio
root.mainloop()
