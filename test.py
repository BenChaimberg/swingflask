import json
x = {
'1201':'Swing Paints Circa 1850 Chair-Loc Wood Sweller',

'1300':'Swing Paints Circa 1850 Maple Scraper',
'1301':'Swing Paints Circa 1850 Stripping Gloves',
'1302':'Swing Paints Circa 1850 Stripping Tool',
'1303':'Swing Paints Circa 1850 Finishing Pads',
'1310':'Swing Paints Circa 1850 Cheese Cloth',
'1315':'Swing Paints Circa 1850 Staining Essentials',
'1316':'Swing Paints Circa 1850 Staining &amp, Mixing Essentials',

'1418':'Swing Paints Circa 1850 Aqua Varnish'
}
with open('brochurelist', 'a') as file:
	json.dump(x,file)
with open('brochurelist', 'r') as file:
	y = json.load(file)
	print y['1201']