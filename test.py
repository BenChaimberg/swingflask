from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import urllib2
from urllib2 import Request, urlopen, URLError
from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import update

app = Flask(__name__) #created app as instance of Flask
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://swingpaint305734:103569@sql.megasqlservers.com:3306/circa1850_swingpaints_com'
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(250),nullable=False)
    demo = db.Column(db.String(250),nullable=True)
    text = db.Column(db.Text(),nullable=False)
    directions = db.Column(db.Text(),nullable=True)
    forms_us = db.Column(db.Text(),nullable=True)
    forms_can = db.Column(db.Text(),nullable=True)
    category = db.Column(db.Text(),nullable=False)
    brand = db.Column(db.Text(),nullable=True)

    def __init__(self, id, title, demo, text, directions, forms_us, forms_can, category, brand):
        self.id = id
        self.title = title
        self.demo = demo
        self.text = text
        self.directions = directions
        self.forms_us = forms_us
        self.forms_can = forms_can
        self.category = category
        self.brand = brand

for x in Products.query.all():
    req = Request('http://www.swingpaints.com/'  + str(x.id) + 'can.htm')
    try:
        response = urlopen(req)
    except URLError as e:
		pass
    else:
		html = response.read()
		html = html.decode('latin-1')

		class MyHTMLParser(HTMLParser):
			def __init__(self):
				HTMLParser.__init__(self)
				self.recording = False
				self.datalist = []
				self.start = 0
				self.end = 0
			def handle_starttag(self, tag, attrs):
				if tag == 'select':
					self.recording = True
				if tag == 'option':
					self.datalist.append('<option ')
					for attr in attrs:
						self.datalist.append(str(attr[0])+'="'+str(attr[1])+'"')
					self.datalist.append('>')
			def handle_endtag(self, tag):
				if tag == 'select':
					self.recording = False
				if tag == 'option':
					self.datalist.append('</option>')
			def handle_data(self, data):
				if self.recording == True:
					self.datalist.append(data)
			def handle_entityref(self, name):
				c = unichr(name2codepoint[name])
				if self.recording == True:
					self.datalist.append('&'+name+';')
			
			def handle_charref(self, name):
				if name.startswith('x'):
				    c = int(name[1:], 16)
				else:
				    c = int(name)
				if self.recording == True:
					self.datalist.append(c)

		parser = MyHTMLParser()
		parser.feed(html)
		wholedata = ''
		for datum in parser.datalist:
			wholedata += datum
		if x.forms_can == '':
			print 'blank'
			print wholedata
db.session.commit()
