import os
import platform
import socket
import psutil
import datetime
import sys
import time
import random
import string
import shutil # Für erweitertes Löschen von Ordnern

try:
    import msvcrt
except ImportError:
    msvcrt = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("=" * 70)
    print(f"  {title.center(66)}  ")
    print("=" * 70)
    print("\n")

def press_enter_to_continue():
    print("\n" + "=" * 70)
    print("Drücken Sie Enter, um fortzufahren...")
    input()
    print("=" * 70)

def get_single_keypress():
    """
    Liest einen einzelnen Tastendruck ohne Bestätigung durch Enter.
    Funktioniert nur auf Windows mit msvcrt.
    Fällt auf input() zurück, wenn msvcrt nicht verfügbar ist (z.B. Linux/macOS).
    """
    if msvcrt:
        while True:
            if msvcrt.kbhit(): # Prüft, ob eine Taste gedrückt wurde
                key = msvcrt.getch() # Liest den Tastendruck (als Byte)
                try:
                    return key.decode('utf-8') # Versucht, in UTF-8 zu dekodieren
                except UnicodeDecodeError:
                    # Wenn es kein druckbares Zeichen ist (z.B. Pfeiltasten), ignorieren
                    continue
    else:
        # Fallback für Nicht-Windows-Systeme
        return input("Bitte wählen Sie eine Option (und drücken Sie Enter): ")


# --- Systeminformationen Funktionen ---
def show_basic_system_info():
    print_header("SYSTEM - BASISINFORMATIONEN")
    print(f"Betriebssystem: {platform.system()} {platform.release()} ({platform.version()})\n")
    print(f"Architektur: {platform.machine()}\n")
    print(f"Prozessor: {platform.processor()}\n")
    print(f"Hostname: {socket.gethostname()}\n")
    print(f"Python Version: {platform.python_version()}\n")
    press_enter_to_continue()

def show_ram_cpu_details():
    print_header("SYSTEM - RAM & CPU DETAILS")
    # RAM Informationen
    svmem = psutil.virtual_memory()
    print(f"Totaler RAM: {svmem.total / (1024**3):.2f} GB\n")
    print(f"Verfügbarer RAM: {svmem.available / (1024**3):.2f} GB\n")
    print(f"Genutzter RAM: {svmem.used / (1024**3):.2f} GB ({svmem.percent}%)\n")

    # CPU Informationen
    print(f"Anzahl der CPU-Kerne (physisch): {psutil.cpu_count(logical=False)}\n")
    print(f"Anzahl der CPU-Kerne (logisch): {psutil.cpu_count(logical=True)}\n")
    print(f"Aktuelle CPU-Auslastung: {psutil.cpu_percent(interval=1)}%\n") # Intervall von 1 Sekunde
    press_enter_to_continue()

def show_disk_usage():
    print_header("SYSTEM - FESTPLATTENNUTZUNG")
    partitions = psutil.disk_partitions()
    for p in partitions:
        print(f"Gerät: {p.device}\n")
        print(f"  Mountpoint: {p.mountpoint}\n")
        print(f"  Dateisystemtyp: {p.fstype}\n")
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"  Total: {usage.total / (1024**3):.2f} GB\n")
            print(f"  Genutzt: {usage.used / (1024**3):.2f} GB\n")
            print(f"  Frei: {usage.free / (1024**3):.2f} GB\n")
            print(f"  Prozentsatz: {usage.percent}%\n")
        except PermissionError:
            print("  Zugriff verweigert für dieses Laufwerk.\n")
        print("-" * 66)
    press_enter_to_continue()

def show_system_uptime():
    print_header("SYSTEM - UPTIME")
    boot_time_timestamp = psutil.boot_time()
    boot_time_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.datetime.now()
    uptime = now - boot_time_datetime
    print(f"System gestartet am: {boot_time_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"System Uptime: {uptime}\n")
    press_enter_to_continue()

def show_environment_variables():
    print_header("SYSTEM - UMGESBUNGSVARIABLEN")
    print("Dies sind die Systemumgebungsvariablen. Vorsicht beim Bearbeiten außerhalb dieses Tools!\n")
    print("-" * 70)
    for key, value in os.environ.items():
        print(f"{key}={value}\n")
    press_enter_to_continue()

# --- Netzwerk Tools Funktionen ---
def show_basic_network_info():
    print_header("NETZWERK - BASISINFORMATIONEN")
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}\n")
        print(f"Lokale IP-Adresse: {ip_address}\n")

        net_if_addrs = psutil.net_if_addrs()
        print("\nNetzwerkschnittstellen:\n")
        for interface_name, interface_addresses in net_if_addrs.items():
            print(f"  Schnittstelle: {interface_name}\n")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET': # IPv4
                    print(f"    IP-Adresse: {address.address}\n")
                    print(f"    Netzmaske: {address.netmask}\n")
                    if address.broadcast:
                        print(f"    Broadcast-IP: {address.broadcast}\n")
                elif str(address.family) == 'AddressFamily.AF_INET6': # IPv6
                    print(f"    IPv6-Adresse: {address.address}\n")
                elif str(address.family) == 'AddressFamily.AF_PACKET': # MAC-Adresse
                    print(f"    MAC-Adresse: {address.address}\n")
            print("-" * 66)
    except Exception as e:
        print(f"Fehler beim Abrufen der Netzwerkinformationen: {e}\n")
    press_enter_to_continue()

def ping_host():
    print_header("NETZWERK - PING TEST")
    host = input("Geben Sie den Host oder die IP-Adresse ein, die Sie pingen möchten: ")
    if not host:
        print("Kein Host eingegeben.\n")
        press_enter_to_continue()
        return
    
    # -n 4 für Windows, -c 4 für Linux/macOS (4 Pakete)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = f"ping {param} 4 {host}"
    
    print(f"Führe '{command}' aus...\n")
    os.system(command) # Führt den Ping-Befehl des Betriebssystems aus
    press_enter_to_continue()

def basic_port_scanner():
    print_header("NETZWERK - EINFACHER PORT SCANNER")
    target = input("Geben Sie die Ziel-IP-Adresse ein: ")
    if not target:
        print("Keine Ziel-IP eingegeben.\n")
        press_enter_to_continue()
        return

    try:
        start_port = int(input("Geben Sie den Start-Port ein (z.B. 1): "))
        end_port = int(input("Geben Sie den End-Port ein (z.B. 1024): "))
        if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port):
            print("Ungültiger Port-Bereich. Ports müssen zwischen 0 und 65535 liegen.\n")
            press_enter_to_continue()
            return
    except ValueError:
        print("Ungültige Port-Nummer.\n")
        press_enter_to_continue()
        return

    print(f"Scanne Ports von {start_port} bis {end_port} auf {target}...\n")
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05) # Kurzes Timeout für Schnelligkeit
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port} ist offen\n")
            sock.close()
        except socket.gaierror:
            print("Fehler: Hostname konnte nicht aufgelöst werden.\n")
            break
        except socket.error as e:
            print(f"Netzwerkfehler beim Scannen: {e}\n")
            break
        except Exception as e:
            print(f"Unerwarteter Fehler beim Scannen von Port {port}: {e}\n")
            break

    if open_ports:
        print(f"\nOffene Ports auf {target}: {open_ports}\n")
    else:
        print(f"\nKeine offenen Ports im Bereich {start_port}-{end_port} auf {target} gefunden.\n")
    press_enter_to_continue()

def check_internet_connection():
    print_header("NETZWERK - INTERNETVERBINDUNG PRÜFEN")
    print("Versuche, eine Verbindung zu einem bekannten Server (Google DNS) herzustellen...\n")
    try:
        # Versuche, eine Verbindung zu Google's DNS-Server herzustellen (IP und Port für DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("ERFOLG: Internetverbindung ist aktiv.\n")
    except OSError:
        print("FEHLER: Keine Internetverbindung erkannt.\n")
    press_enter_to_continue()

# --- Datei Operationen Funktionen ---
def show_current_directory_content():
    print_header("DATEI - INHALT DES AKTUELLES VERZEICHNISSES")
    current_directory = os.getcwd()
    print(f"Aktuelles Verzeichnis: {current_directory}\n")
    print("\nInhalt:\n")
    try:
        items = os.listdir(current_directory)
        if not items:
            print("  Das Verzeichnis ist leer.\n")
        for item in items:
            item_path = os.path.join(current_directory, item)
            if os.path.isfile(item_path):
                print(f"  [DATEI] {item}\n")
            elif os.path.isdir(item_path):
                print(f"  [ORDNER] {item}\n")
    except Exception as e:
        print(f"Fehler beim Auflisten des Verzeichnisses: {e}\n")
    press_enter_to_continue()

def view_text_file():
    print_header("DATEI - TEXTDATEI ANZEIGEN")
    file_path = input("Geben Sie den Pfad zur Textdatei ein: ")
    if not file_path:
        print("Kein Pfad eingegeben.\n")
        press_enter_to_continue()
        return
    
    if not os.path.exists(file_path):
        print("Datei nicht gefunden.\n")
        press_enter_to_continue()
        return
    if not os.path.isfile(file_path):
        print("Der angegebene Pfad ist keine Datei.\n")
        press_enter_to_continue()
        return

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            print("\n--- INHALT DER DATEI ---\n")
            for line in f:
                print(line.strip())
            print("\n--- ENDE DER DATEI ---\n")
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}\n")
    press_enter_to_continue()

def create_empty_file():
    print_header("DATEI - LEERE DATEI ERSTELLEN")
    file_name = input("Geben Sie den Namen der neuen Datei ein (z.B. meine_datei.txt): ")
    if not file_name:
        print("Kein Dateiname eingegeben.\n")
        press_enter_to_continue()
        return
    
    try:
        with open(file_name, 'w') as f:
            pass # Erstellt eine leere Datei
        print(f"Datei '{file_name}' erfolgreich erstellt im aktuellen Verzeichnis.\n")
    except Exception as e:
        print(f"Fehler beim Erstellen der Datei: {e}\n")
    press_enter_to_continue()

def create_directory():
    print_header("DATEI - ORDNER ERSTELLEN")
    dir_name = input("Geben Sie den Namen des neuen Ordners ein: ")
    if not dir_name:
        print("Kein Ordnername eingegeben.\n")
        press_enter_to_continue()
        return
    
    try:
        os.makedirs(dir_name, exist_ok=True) # exist_ok=True verhindert Fehler, wenn Ordner bereits existiert
        print(f"Ordner '{dir_name}' erfolgreich erstellt (oder existiert bereits).\n")
    except Exception as e:
        print(f"Fehler beim Erstellen des Ordners: {e}\n")
    press_enter_to_continue()

def delete_file_or_directory():
    print_header("DATEI - DATEI/ORDNER LÖSCHEN")
    path_to_delete = input("Geben Sie den Pfad zur Datei oder zum Ordner ein, der gelöscht werden soll: ")
    if not path_to_delete:
        print("Kein Pfad eingegeben.\n")
        press_enter_to_continue()
        return

    if not os.path.exists(path_to_delete):
        print("Der angegebene Pfad existiert nicht.\n")
        press_enter_to_continue()
        return

    confirm = input(f"SIND SIE SICHER, dass Sie '{path_to_delete}' löschen möchten? Dies kann NICHT rückgängig gemacht werden! (ja/nein): ").lower()
    if confirm != 'ja':
        print("Löschvorgang abgebrochen.\n")
        press_enter_to_continue()
        return

    try:
        if os.path.isfile(path_to_delete):
            os.remove(path_to_delete)
            print(f"Datei '{path_to_delete}' erfolgreich gelöscht.\n")
        elif os.path.isdir(path_to_delete):
            shutil.rmtree(path_to_delete) # Löscht Ordner und Inhalt rekursiv
            print(f"Ordner '{path_to_delete}' und sein Inhalt erfolgreich gelöscht.\n")
        else:
            print("Der angegebene Pfad ist weder eine Datei noch ein Ordner.\n")
    except Exception as e:
        print(f"Fehler beim Löschen: {e}\n")
    press_enter_to_continue()

# --- Prozess Management Funktionen ---
def list_processes():
    print_header("PROZESS - LAUFENDE PROZESSE ANZEIGEN")
    print(f"{'PID':<8} {'Name':<30} {'Status':<15} {'CPU (%)':<10} {'RAM (MB)':<10}\n")
    print("-" * 80)
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
        try:
            mem_info = proc.info['memory_info']
            print(f"{proc.info['pid']:<8} {proc.info['name'][:28]:<30} {proc.info['status']:<15} {proc.info['cpu_percent']:<10.2f} {mem_info.rss / (1024**2):<10.2f}\n")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass # Prozess existiert nicht mehr oder Zugriff verweigert
    press_enter_to_continue()

def kill_process():
    print_header("PROZESS - PROZESS BEENDEN")
    try:
        pid = int(input("Geben Sie die PID des Prozesses ein, den Sie beenden möchten: "))
    except ValueError:
        print("Ungültige PID. Bitte geben Sie eine Zahl ein.\n")
        press_enter_to_continue()
        return

    try:
        process = psutil.Process(pid)
        print(f"Prozess gefunden: PID={process.pid}, Name={process.name()}\n")
        confirm = input(f"SIND SIE SICHER, dass Sie Prozess '{process.name()}' (PID: {pid}) beenden möchten? (ja/nein): ").lower()
        if confirm == 'ja':
            process.terminate()
            print(f"Prozess {pid} '{process.name()}' wurde beendet.\n")
        else:
            print("Beenden des Prozesses abgebrochen.\n")
    except psutil.NoSuchProcess:
        print(f"Prozess mit PID {pid} nicht gefunden.\n")
    except psutil.AccessDenied:
        print(f"Zugriff verweigert. Möglicherweise benötigen Sie Administratorrechte, um diesen Prozess zu beenden.\n")
    except Exception as e:
        print(f"Fehler beim Beenden des Prozesses: {e}\n")
    press_enter_to_continue()

# --- "IoT" Simulationen & Daten Funktionen ---
def generate_sensor_data():
    print_header("IOT - ZUFÄLLIGE SENSORDATEN")
    print("Simulierte Sensordaten (zufällig generiert):\n")
    print(f"  Temperatur: {random.uniform(18.0, 30.0):.2f} °C\n")
    print(f"  Luftfeuchtigkeit: {random.uniform(40.0, 70.0):.2f} %\n")
    print(f"  Luftdruck: {random.uniform(980.0, 1020.0):.2f} hPa\n")
    print(f"  Lichtstärke: {random.randint(0, 1000)} Lux\n")
    print(f"  Bodenfeuchte: {random.uniform(0.0, 100.0):.2f} %\n")
    print(f"  CO2-Konzentration: {random.randint(400, 2000)} ppm\n")
    press_enter_to_continue()

def simple_clock():
    print_header("IOT - EINFACHE UHR")
    print("Aktuelle Uhrzeit (aktualisiert sich für 10 Sekunden):\n")
    for _ in range(10):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\r{current_time}", end="", flush=True) # Überschreibt die Zeile
        time.sleep(1)
    print("\n\n") # Neue Zeile nach der Uhr
    press_enter_to_continue()

def generate_random_data_stream():
    print_header("IOT - ZUFÄLLIGER DATENSTREAM")
    print("Generiere einen simulierten Datenstream (10 Einträge):\n")
    for i in range(1, 11):
        device_id = f"Device-{random.randint(100, 999)}"
        value = random.uniform(0.0, 100.0)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = random.choice(["OK", "WARNING", "ERROR"])
        print(f"[{i:02}] {timestamp} | ID: {device_id} | Wert: {value:.2f} | Status: {status}\n")
        time.sleep(0.5) # Eine kleine Pause
    press_enter_to_continue()

# --- Utilities Funktionen ---
def generate_password():
    print_header("UTILITIES - ZUFÄLLIGES PASSWORT")
    try:
        length = int(input("Geben Sie die gewünschte Länge des Passworts ein: "))
    except ValueError:
        print("Ungültige Länge. Bitte geben Sie eine Zahl ein.\n")
        press_enter_to_continue()
        return
    
    if length <= 0:
        print("Länge muss größer als 0 sein.\n")
        press_enter_to_continue()
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    print(f"Generiertes Passwort: {password}\n")
    press_enter_to_continue()

def simple_calculator():
    print_header("UTILITIES - EINFACHER TASCHENRECHNER")
    print("Unterstützte Operationen: +, -, *, /\n")
    try:
        num1 = float(input("Geben Sie die erste Zahl ein: "))
        operator = input("Geben Sie den Operator ein (+, -, *, /): ")
        num2 = float(input("Geben Sie die zweite Zahl ein: "))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Fehler: Division durch Null ist nicht erlaubt.\n")
                result = "Fehler"
            else:
                result = num1 / num2
        else:
            result = "Ungültiger Operator"
        
        print(f"Ergebnis: {result}\n")
    except ValueError:
        print("Ungültige Zahleneingabe.\n")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}\n")
    press_enter_to_continue()

def text_encoder_decoder():
    print_header("UTILITIES - TEXT ENCODER/DECODER")
    print("1. Text in Base64 kodieren\n")
    print("2. Text aus Base64 dekodieren\n")
    sub_choice = input("Wählen Sie eine Option (1-2): ")

    if sub_choice == '1':
        import base64
        text = input("Geben Sie den Text ein, der kodiert werden soll: ")
        encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        print(f"Kodierter Text (Base64): {encoded_text}\n")
    elif sub_choice == '2':
        import base64
        text = input("Geben Sie den Base64-Text ein, der dekodiert werden soll: ")
        try:
            decoded_text = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            print(f"Dekodierter Text: {decoded_text}\n")
        except Exception as e:
            print(f"Fehler beim Dekodieren: {e}. Ist es gültiger Base64-Text?\n")
    else:
        print("Ungültige Eingabe.\n")
    press_enter_to_continue()

# --- Menüfunktionen ---
def system_info_menu():
    while True:
        print_header("HAUPTMENÜ > SYSTEM INFORMATIONEN")
        print("1. Basis System Info\n")
        print("2. RAM & CPU Details\n")
        print("3. Festplattennutzung\n")
        print("4. System Uptime\n")
        print("5. Umgebungsvariablen\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': show_basic_system_info()
        elif choice == '2': show_ram_cpu_details()
        elif choice == '3': show_disk_usage()
        elif choice == '4': show_system_uptime()
        elif choice == '5': show_environment_variables()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2) # Kurze Pause

def network_tools_menu():
    while True:
        print_header("HAUPTMENÜ > NETZWERK TOOLS")
        print("1. Basis Netzwerkinformationen\n")
        print("2. Ping Host\n")
        print("3. Einfacher Port Scanner\n")
        print("4. Internet Verbindung prüfen\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': show_basic_network_info()
        elif choice == '2': ping_host()
        elif choice == '3': basic_port_scanner()
        elif choice == '4': check_internet_connection()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2)

def file_operations_menu():
    while True:
        print_header("HAUPTMENÜ > DATEI OPERATIONEN")
        print("1. Inhalt des aktuellen Verzeichnisses anzeigen\n")
        print("2. Textdatei anzeigen\n")
        print("3. Leere Datei erstellen\n")
        print("4. Ordner erstellen\n")
        print("5. Datei/Ordner löschen\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': show_current_directory_content()
        elif choice == '2': view_text_file()
        elif choice == '3': create_empty_file()
        elif choice == '4': create_directory()
        elif choice == '5': delete_file_or_directory()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2)

def process_management_menu():
    while True:
        print_header("HAUPTMENÜ > PROZESS MANAGEMENT")
        print("1. Laufende Prozesse auflisten\n")
        print("2. Prozess beenden\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': list_processes()
        elif choice == '2': kill_process()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2)

def iot_simulations_menu():
    while True:
        print_header("HAUPTMENÜ > 'IOT' SIMULATIONEN & DATEN")
        print("1. Zufällige Sensordaten generieren\n")
        print("2. Einfache Uhr anzeigen\n")
        print("3. Zufälliger Datenstream generieren\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': generate_sensor_data()
        elif choice == '2': simple_clock()
        elif choice == '3': generate_random_data_stream()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2)

def utilities_menu():
    while True:
        print_header("HAUPTMENÜ > UTILITIES")
        print("1. Zufälliges Passwort generieren\n")
        print("2. Einfacher Taschenrechner\n")
        print("3. Text Kodierer/Dekodierer (Base64)\n")
        print("0. Zurück zum Hauptmenü\n")
        print("-" * 70)
        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1': generate_password()
        elif choice == '2': simple_calculator()
        elif choice == '3': text_encoder_decoder()
        elif choice == '0': break
        else: print("Ungültige Eingabe, bitte versuchen Sie es erneut.\n")
        time.sleep(0.2)

# Hauptmenü des Multitools
def main_menu():
    while True:
        clear_screen()
        # ASCII Art für "MULTITOOL"
        print(" /$$      /$$ /$$   /$$ /$$    /$$$$$$$$ /$$$$$$ /$$$$$$$$ /$$$$$$   /$$$$$$  /$$      ")
        print("| $$$    /$$$| $$  | $$| $$   |__  $$__/|_  $$_/|__  $$__//$$__  $$ /$$__  $$| $$      ")
        print("| $$$$  /$$$$| $$  | $$| $$      | $$     | $$     | $$  | $$  \ $$| $$  \ $$| $$      ")
        print("| $$ $$/$$ $$| $$  | $$| $$      | $$     | $$     | $$  | $$  | $$| $$  | $$| $$      ")
        print("| $$  $$$| $$| $$  | $$| $$      | $$     | $$     | $$  | $$  | $$| $$  | $$| $$      ")
        print("| $$\  $ | $$| $$  | $$| $$      | $$     | $$     | $$  | $$  | $$| $$  | $$| $$          ") 
        print("| $$ \/  | $$|  $$$$$$/| $$$$$$$$| $$    /$$$$$$   | $$  |  $$$$$$/|  $$$$$$/| $$$$$$$$    ")
        print("|__/     |__/ \______/ |________/|__/   |______/   |__/   \______/  \______/ |________/     ")
        print("                                                                                                     ")                                                                       
        print("                                                                 Made by Pascal404")
        print("\n")
        print("======================================================================")
        print("                 WILLKOMMEN ZUM ULTIMATIVEN MULTITOOL!                ")
        print("======================================================================")
        print("1. System Informationen (Hardware, OS, Umgebung)\n")
        print("2. Netzwerk Tools (Ping, Scan, Verbindung)\n")
        print("3. Datei Operationen (Verzeichnis, Erstellen, Löschen)\n")
        print("4. Prozess Management (Prozesse anzeigen/beenden)\n")
        print("5. 'IoT' Simulationen & Daten (Sensoren, Streams)\n")
        print("6. Utilities (Passwort, Rechner, Encoder)\n")
        print("0. MULTITOOL BEENDEN\n")
        print("======================================================================")

        choice = get_single_keypress() # Hier wird get_single_keypress verwendet

        if choice == '1':
            system_info_menu()
        elif choice == '2':
            network_tools_menu()
        elif choice == '3':
            file_operations_menu()
        elif choice == '4':
            process_management_menu()
        elif choice == '5':
            iot_simulations_menu()
        elif choice == '6':
            utilities_menu()
        elif choice == '0':
            clear_screen()
            print("======================================================================")
            print("           Multitool wird beendet. Auf Wiedersehen, Commander!        ")
            print("======================================================================")
            sys.exit() # Beendet das Skript sauber
        else:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl zwischen 0 und 6 ein.\n")
            time.sleep(1) # Kurze Pause, damit die Meldung gelesen werden kann

# Startpunkt des Skripts
if __name__ == "__main__":
    # Überprüfen, ob psutil installiert ist, da es für detailliertere Infos benötigt wird
    try:
        import psutil
    except ImportError:
        print("Das 'psutil'-Modul ist nicht installiert.\n")
        print("Bitte installieren Sie es mit: pip install psutil\n")
        print("Das Tool kann ohne 'psutil' nur eingeschränkt funktionieren.\n")
        print("Drücken Sie Enter, um fortzufahren oder beenden Sie das Programm.\n")
        input() # Hier muss noch input() verwendet werden, da es vor der get_single_keypress-Funktion liegt
    
    main_menu()
