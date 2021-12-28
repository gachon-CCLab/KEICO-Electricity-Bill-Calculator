import json
with open ("electric_rates.json", "r", encoding="utf-8") as f_rates_json:
    rates_data = json.load(f_rates_json)
    f_rates_json.close()
print(rates_data['electric_rates'][1]['description'])
tom = (item for item in rates_data['electric_rates'] if item['calc_type'] == 1 and item['class1'] == 0 and item['class2'] == 1 and item['class_contract'] == 0)
for value in tom:
    value2 = value
    
print (value2)
print(value2['description'])
