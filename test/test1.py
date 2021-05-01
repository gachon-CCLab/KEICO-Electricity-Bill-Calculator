temp1 = 0
required_usage = [0]

for i in range(44):
    if i % 3 == 2:
        temp1 = temp1 - 92
    else:
        temp1 = temp1 - 90
    required_usage.append(temp1)

print(required_usage)