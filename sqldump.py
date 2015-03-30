from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import update
from static import frenchproducttitle, frenchproducttext, frenchproductdir, frenchproductinfo, frenchproductdemo, frenchproductforms, frenchcategorytitle, frenchcategoryproducts

app = Flask(__name__) #created app as instance of Flask
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://swingpaint305734:103569@sql.megasqlservers.com:3306/circa1850_swingpaints_com'
db = SQLAlchemy(app)

class Infotable(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Text(convert_unicode=True),nullable=False)
    quantity = db.Column(db.Text(convert_unicode=True),nullable=False)

    def __init__(self, productid, size, quantity):
        self.productid = productid
        self.size = size
        self.quantity = quantity

class Infolist(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    infolist = db.Column(db.Text(convert_unicode=True),nullable=True)

    def __init__(self, productid, infolist):
        self.productid = productid
        self.infolist = infolist

class Categories(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    category = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, category, name):
        self.category = category
        self.name = name

class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(250),nullable=False)
    demo = db.Column(db.String(250),nullable=True)
    text = db.Column(db.Text(),nullable=False)
    directions = db.Column(db.Text(),nullable=True)
    forms_us = db.Column(db.Text(),nullable=True)
    forms_can = db.Column(db.Text(),nullable=True)
    category = db.Column(db.Text(),nullable=False)

    def __init__(self, id, title, demo, text, directions, forms_us, forms_can, category):
        self.id = id
        self.title = title
        self.demo = demo
        self.text = text
        self.directions = directions
        self.forms_us = forms_us
        self.forms_can = forms_can
        self.category = category

class Frenchinfotable(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Text(convert_unicode=True),nullable=False)
    quantity = db.Column(db.Text(convert_unicode=True),nullable=False)

    def __init__(self, productid, size, quantity):
        self.productid = productid
        self.size = size
        self.quantity = quantity

class Frenchinfolist(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    infolist = db.Column(db.Text(convert_unicode=True),nullable=True)

    def __init__(self, productid, infolist):
        self.productid = productid
        self.infolist = infolist

class Frenchcategories(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    category = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, category, name):
        self.category = category
        self.name = name

class Frenchproducts(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(250),nullable=False)
    demo = db.Column(db.String(250),nullable=True)
    text = db.Column(db.Text(),nullable=False)
    directions = db.Column(db.Text(),nullable=True)
    forms_us = db.Column(db.Text(),nullable=True)
    forms_can = db.Column(db.Text(),nullable=True)
    category = db.Column(db.Text(),nullable=False)

    def __init__(self, id, title, demo, text, directions, forms_us, forms_can, category):
        self.id = id
        self.title = title
        self.demo = demo
        self.text = text
        self.directions = directions
        self.forms_us = forms_us
        self.forms_can = forms_can
        self.category = category

def get_sql():
	infothings = Infotable.query.filter_by(productid=1555).order_by(Infotable.id.asc()).all()
	for infothing in infothings:
		print infothing.size,infothing.quantity

def add_products_sql():
	for product in frenchproducttitle.title:
		for item in frenchcategoryproducts.products: #for every category in categories
			for item2 in frenchcategoryproducts.products[item]: #for every product in category
				if item2 == product: #if product is equal to productid
					category = item #return category
				if (product == '1818' or product == '1819') and item2 == '1817': #if productid is 1818 or 1819, not in list, so uses 1817 instead
					category = item #return category
		if frenchproductdemo.demo[product] is not 'No Directions Available':
			demo = frenchproductdemo.demo[product]
		else: demo = ''
		new_product = Frenchproducts(product,
			frenchproducttitle.title[product],
			demo,
			frenchproducttext.text[product],
			frenchproductdir.dir[product],
			frenchproductforms.forms[product+'us'],
			frenchproductforms.forms[product+'can'],
			category
		)
		db.session.add(new_product)
		for i in range(0,len(frenchproductinfo.info[product])/2):
			info = frenchproductinfo.info[product].pop(0)
			for j in range(0,len(frenchproductinfo.info[product])/2+1):
				info2 = frenchproductinfo.info[product].pop(0)
				new_infotable = Frenchinfotable(product,info,info2)
				break
			db.session.add(new_infotable)
		for info in productinfo.info2[product]:
			new_infolist = Frenchinfolist(product,info)
			db.session.add(new_infolist)
	db.session.commit()

def add_category_sql():
	for category in frenchcategorytitle.title:
		new_category = Frenchcategories(category,categorytitle.title[category])
		db.session.add(new_category)
	db.session.commit()

db.create_all()
add_products_sql()
add_category_sql()
#get_sql()
