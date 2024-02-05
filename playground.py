import json
from icecream import ic

with open('logs\softonic\monitoring_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

ic(len(data))

temps = data[:100]
ic(len(temps))

for temp in temps:
    if "on progess" in temp.values(): ic(temp)