import json
with open('brochurelist', 'r') as file:
	y = json.load(file)
	for x in y:
		print y[x]