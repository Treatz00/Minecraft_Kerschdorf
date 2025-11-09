# Minecraft_Kerschdorf

Ein kleines Beispielprojekt für einen Discord-Bot, der in Python geschrieben ist und ein paar Standardbefehle zum Testen bereitstellt.

## Voraussetzungen

- Python 3.10 oder neuer
- Ein Discord-Bot-Token (erstelle einen Bot unter <https://discord.com/developers/applications>)

## Einrichtung

1. Repository klonen und in das Projektverzeichnis wechseln.
2. Optional: Eine virtuelle Umgebung erstellen und aktivieren.
3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

4. `.env.example` nach `.env` kopieren und deinen Bot-Token eintragen:

   ```bash
   cp .env.example .env
   # Bearbeite .env und setze DISCORD_TOKEN
   ```

5. Den Bot starten (optional mit zusätzlichen Parametern):

   ```bash
   python bot.py --log-level DEBUG --prefix "?"
   ```

   Ohne Parameter wird automatisch der Präfix `!` verwendet und das Log-Level aus der Umgebung gelesen.

## Befehle

| Befehl | Beschreibung |
| ------ | ------------- |
| `!help` | Zeigt eine Übersicht aller Befehle an. |
| `!ping` | Prüft die Latenz und antwortet mit `Pong!`. |
| `!say <text>` | Wiederholt den angegebenen Text. |
| `!roll [seiten]` | Würfelt eine Zufallszahl zwischen 1 und den angegebenen Seiten (Standard 6, Maximum 10 000). |
| `!add <a> <b>` | Addiert zwei ganze Zahlen. |
| `!choose <Option A> <Option B> [...]` | Wählt zufällig eine der angegebenen Optionen. |
| `!yesno` | Antwortet zufällig mit Ja oder Nein. |
| `!serverinfo` | Zeigt Informationen zum aktuellen Server an. |
| `!userinfo [@Nutzer]` | Zeigt Informationen zum aufrufenden oder angegebenen Nutzer an. |

## Hinweise

- Der Bot benötigt die Berechtigung, Nachrichten lesen und schreiben zu können.
- Für einige Befehle ist die Berechtigung zum Einbetten von Links hilfreich (z. B. `!userinfo`).
- Passe den Präfix oder zusätzliche Befehle nach Bedarf im Quelltext an.
- Die `.env`-Datei wird ohne zusätzliche Bibliotheken eingelesen – stelle nur sicher, dass sie im Projektverzeichnis liegt.
