import json
with open('brochurelist', 'r') as file:
	y = json.load(file)
	for x in range(0,2679):
		for z in y[str(x)]:
			print y[str(x)][z]