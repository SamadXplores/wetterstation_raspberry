import json
import time
from w1thermsensor import W1ThermSensor
from datetime import datetime

sensor = W1ThermSensor()
history_data = {"temperatures": [], "times": []}

def write_temperature_to_file():
    try:
        temperature = sensor.get_temperature()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Lade bestehende Historie
        try:
            with open('/var/www/html/temperature_history.json', 'r') as json_file:
                history_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            history_data = {"temperatures": [], "times": []}
        
        # Füge neue Daten hinzu
        history_data["temperatures"].insert(0, temperature)
        history_data["times"].insert(0, current_time)
        
        # Begrenze auf 100 Einträge
        if len(history_data["temperatures"]) > 100:
            history_data["temperatures"].pop()
            history_data["times"].pop()
        
        # Schreibe aktuelle Temperatur
        with open('/var/www/html/temperature.json', 'w') as json_file:
            json.dump({"temperature": temperature}, json_file)
        
        # Schreibe Historie
        with open('/var/www/html/temperature_history.json', 'w') as json_file:
            json.dump(history_data, json_file)
        
        return temperature
    except Exception as e:
        print(f"Fehler beim Lesen/Schreiben der Daten: {e}")
        return None

if __name__ == '__main__':
    while True:
        write_temperature_to_file()
        time.sleep(2)
