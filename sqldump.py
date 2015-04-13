import time
from time import localtime, strftime
from app import app
from models import db, Infotable, Infolist, Categories, Brands, Products, Frenchinfotable, Frenchinfolist, Frenchcategories, Frenchproducts, Messages, Replies, Brochures

db.init_app(app)

def get_sql():
	brochure = Brochures('testname','test@test.com','testaddress','testcity','teststate','testcode','testcountry',time.strftime("%Y-%m-%d %H:%M:%S", localtime()),'True')
	db.session.add(brochure)
	db.session.commit()

with app.app_context():
	get_sql()
