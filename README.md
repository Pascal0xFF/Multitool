Multitool – Das ultimative Kommandozeilen-Tool

Willkommen zum Multitool! Dieses vielseitige Kommandozeilen-Tool bietet Funktionen für Systeminfos, Netzwerkdiagnose, Dateioperationen, Prozessmanagement, IoT-Simulationen und allgemeine Utilities.

Made by Pascal404
Inhaltsverzeichnis

    Funktionen

    Voraussetzungen

    Installation

    Nutzung

    Wichtige Hinweise

1. Funktionen

Das Multitool bietet folgende Hauptkategorien und Funktionen:

    System Informationen: Basisinfos, RAM/CPU, Festplattennutzung, Uptime, Umgebungsvariablen.

    Netzwerk Tools: Basisinfos, Ping, Port Scanner, Internetprüfung.

    Datei Operationen: Verzeichnisinhalt, Textdatei anzeigen, Datei/Ordner erstellen/löschen.

    Prozess Management: Prozesse auflisten, Prozess beenden.

    'IoT' Simulationen & Daten: Zufällige Sensordaten, Einfache Uhr, Zufälliger Datenstream.

    Utilities: Passwort-Generator, Taschenrechner, Text Kodierer/Dekodierer (Base64).

2. Voraussetzungen

    Betriebssystem: Windows (für volle Funktionalität).

    Python: Python 3.x installiert.

    Python-Module: psutil.

3. Installation
Python installieren

    Herunterladen: Besuchen Sie https://www.python.org/downloads/.

    Installer ausführen: Starten Sie die .exe-Datei.

    WICHTIG: Aktivieren Sie "Add python.exe to PATH" im ersten Fenster des Installers.

    Überprüfen: Öffnen Sie eine neue CMD und geben Sie python --version ein.

Benötigte Python-Module installieren

Installieren Sie psutil in Ihrer Kommandozeile:

pip install psutil

Falls pip nicht erkannt wird:
Verwenden Sie den vollständigen Pfad, z.B.:
"C:\Users\IHR_BENUTZERNAME\AppData\Local\Programs\Python\PythonXX\Scripts\pip.exe" install psutil
4. Nutzung
Skript ausführen

    Speichern: Speichern Sie den Python-Code als multitool.py.

    CMD öffnen & navigieren: cd C:\Pfad\zum\Skript

    Ausführen: python multitool.py

Skript in eine EXE-Datei umwandeln

    PyInstaller installieren: pip install pyinstaller
    (Falls pip nicht erkannt wird, verwenden Sie den vollen Pfad wie oben beschrieben.)

    CMD navigieren: Wechseln Sie zum Skript-Verzeichnis.

    Umwandlung starten:

    pyinstaller --onefile --name "UltraMultitool" multitool.py

    (Falls pyinstaller nicht erkannt wird, verwenden Sie den vollen Pfad zu pyinstaller.exe.)

    EXE finden: Die UltraMultitool.exe finden Sie im Ordner dist in Ihrem Skript-Verzeichnis.

5. Wichtige Hinweise

    Tastatureingabe: Menüauswahl reagiert sofort (Windows). Andere Eingaben erfordern Enter.

    Administratorrechte: Für bestimmte Funktionen können Administratorrechte erforderlich sein.

    Antivirus-Software: PyInstaller-EXEs können fälschlicherweise als verdächtig eingestuft werden.

    Plattformabhängigkeit: EXE ist nur für Windows.
