import json
import time
import plotly.graph_objects as go
from w1thermsensor import W1ThermSensor
from datetime import datetime

sensor = W1ThermSensor()
list_hist = []

fig = go.Figure()

def write_temperature_to_file():
    temperature = sensor.get_temperature()
    data = {"temperature": temperature}
    with open('/var/www/html/temperature.json', 'w') as json_file:
        json.dump(data, json_file)
    return temperature

def history(temp):
    entry = {"temp": temp, "zeit": datetime.now()}
    list_hist.insert(0, entry)
    
    if len(list_hist) > 100:
        list_hist.pop()
    
    temps = [entry["temp"] for entry in list_hist]
    times = [entry["zeit"] for entry in list_hist]
    
    return times, temps

def plot_temperature_data(times, temps):
    fig.data = []
    fig.add_trace(go.Scatter(x=times, y=temps, mode='lines+markers', name='Temperatur'))
    fig.update_layout(
        title="Temperaturverlauf",
        xaxis_title="Zeit",
        yaxis_title="Temperatur (°C)",
        showlegend=True
    )
    fig.show()

if __name__ == '__main__':
    while True:
        temp = write_temperature_to_file()
        times, temps = history(temp)
        plot_temperature_data(times, temps)
        time.sleep(2)
