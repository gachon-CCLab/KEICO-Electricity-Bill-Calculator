import json
with open ("electric_rates.json", "r", encoding="utf-8") as f_rates_json:
    rates_data = json.load(f_rates_json)
    f_rates_json.close()
print(rates_data['electric_rates'][1]['description'])