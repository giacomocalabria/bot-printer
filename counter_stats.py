import schedule
import time
from datetime import datetime
from get_counter import get_counter  # Importa la funzione da get_counter.py

# Percorso del file log
LOG_FILE = "printer_log.txt"

# Funzione per salvare il contatore giornaliero
def save_daily_counter():
    try:
        counter = get_counter()  # Ottieni il contatore tramite get_counter
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as log:
            log.write(f"{current_date},{counter}\n")
        print(f"Contatore salvato: {current_date} - {counter}")
    except Exception as e:
        print(f"Errore durante il salvataggio del contatore: {e}")

# Funzione per calcolare le statistiche del giorno
def get_daily_stats():
    today = datetime.now().strftime("%Y-%m-%d")
    total_count = 0
    daily_count = 0

    try:
        with open(LOG_FILE, "r") as log:
            lines = log.readlines()
            for line in lines:
                date, count = line.strip().split(",")
                if today in date:
                    daily_count = int(count) - total_count
                    total_count = int(count)
    except FileNotFoundError:
        print("File di log non trovato.")
    except Exception as e:
        print(f"Errore nella lettura del log: {e}")

    return total_count, daily_count

# Pianificazione del salvataggio giornaliero
schedule.every().day.at("00:00").do(save_daily_counter)

# Loop principale
if __name__ == "__main__":
    print("Applicazione avviata. Salvataggio giornaliero pianificato.")
    while True:
        schedule.run_pending()
        time.sleep(1)