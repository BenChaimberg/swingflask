import json,time
with open('brochurelist', 'r') as file:
	y = json.load(file)
	print time.strptime(y['0']['time'],"%a %b %d %H:%M:%S %Y")[0]