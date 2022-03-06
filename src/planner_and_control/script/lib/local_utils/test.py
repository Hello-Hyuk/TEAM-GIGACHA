data = '3723.08111'

deg = float(data[0:2])
min = float(data[2:])

min = min / 60

lat = deg+min

print(lat)