from flask import Flask, render_template, url_for, request, abort
from flask.ext.mail import Mail, Message
from flask_wtf import Form, validators
from wtforms.fields import TextField, TextAreaField, SubmitField
import wtforms
from static import producttitle, producttext, productdir, productinfo, productdemo, productforms, frenchproducttitle, frenchproducttext, frenchproductdir, frenchproductinfo, categoryimg, categorytitle, categoryproducts, frenchcategoryimg, frenchcategorytitle, frenchcategoryproducts #import data in .py dictionary form
#import logging
#from logging.handlers import RotatingFileHandler

MAIL_SERVER='mail.swingpaints.com'
MAIL_PORT=25
MAIL_USE_TLS = False
MAIL_USE_SSL= False
MAIL_USERNAME = 'bchaimberg@swingpaints.com'
MAIL_PASSWORD = 'webmaster'

app = Flask(__name__) #created app as instance of Flask
app.config.from_object(__name__)
mail = Mail(app)
app.secret_key = 'blahblahblah' #change later to random

class MyForm(Form):
    visitorname = TextField("Your name:", [wtforms.validators.Required('Please enter your name')])
    visitoremail = TextField("Your email:", [wtforms.validators.Required('Please enter your email'), wtforms.validators.Email()])
    friendname = TextField("Your friend's name:", [wtforms.validators.Required('Please enter your friend&apos;s name')])
    friendemail = TextField("Your friend's email:", [wtforms.validators.Required('Please enter your friend&apos;s email'), wtforms.validators.Email()])

@app.route('/submit', methods=('GET', 'POST'))
def submit():
	form = MyForm()
	if form.validate_on_submit():
		visitorname = form.visitorname.data
		visitoremail = form.visitoremail.data
		friendname = form.friendname.data
		friendemail = form.friendemail.data
		msg = Message()
		msg.recipients = [friendemail]
		msg.sender = (visitorname, visitoremail)
		msg.subject = "Check out Swing Paints!"
		msg.html = "Hey %s,<br />Take a look at this a pretty cool wood finishing company, Swing Paints. Find them online at <a href='swingpaints.herokuapp.com'>swingpaints.com</a>." % (friendname)
		mail.send(msg)
		return "SUCCESS!"
	return render_template('submit.html', form=form)

@app.context_processor
def utility_processor(): #creates template context processor function
	def product_category(category,id): #creates specific category for product function, takes arguments of all products in all categories and product id
		for item in category: #for every category in categories
			for item2 in category[item]: #for every product in category
				if item2 == id: #if product is equal to productid
					return item #return category
				if (id == '1818' or id == '1819') and item2 == '1817': #if productid is 1818 or 1819, not in list, so uses 1817 instead
					return item #return category
	return dict(product_category=product_category) #returns function result

@app.errorhandler(404)
def notfound(e): #if HTTP returns 404 error
    return render_template('404.html'), 404 #render 404 template and return 404 error
    
@app.errorhandler(500)
def apperror(e): #if HTTP returns 500 error
    return render_template('500.html'), 500 #render 500 template and return 500 error
    
@app.errorhandler(403)
def forbidden(e): #if HTTP returns 403 error
    return render_template('403.html'), 403 #render 403 template and return 403 error

@app.route('/')
@app.route('/home')
def index(): #if URL is at root or at home
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchmain.html') #render french home page
	else: #if URL does not end with ?french
		return render_template('main.html') #return english home page

@app.route('/locations')
def locations(): #if URL is at locations
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchlocations.html') #render french locations page
	else: #if URL does not end with ?french
		return render_template('locations.html') #return english locations page

@app.route('/faq')
def faq(): #if URL is at faq
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchfaq.html') #render french locations page
	else: #if URL does not end with ?french
		return render_template('faq.html') #return english locations page
		
@app.route('/contact')
def contact(): #if URL is at contact
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchcontact.html') #render french contact page
	else: #if URL does not end with ?french
		return render_template('contact.html') #return english contact page

@app.route('/marketing')
def marketing(): #if URL is at marketing
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchmarketing.html') #render french marketing page
	else: #if URL does not end with ?french
		return render_template('marketing.html') #return english marketing page

@app.route('/about')
def about(): #if URL is at about
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchabout.html') #render french about page
	else: #if URL does not end with ?french
		return render_template('about.html') #return english about page

@app.route('/product/<productid>')
def product(productid): #if URL is at /product/####
	if request.query_string == 'french': #if URL ends with ?french
		if frenchproducttitle.title.get(productid): #if product exists in list of product titles (should contain all products)
			return render_template('frenchproduct.html', product={ #renders french product page with the following parameters
																'id':productid, #product.id = productid
																'title':frenchproducttitle.title[productid], #product.title = string with product name
																'text':frenchproducttext.text[productid], #product.text = string with product text
																'dir':frenchproductdir.dir[productid], #product.dir = string with product directions
																'info':frenchproductinfo.info[productid] #product.info = string with product info (table)
															})
		else: abort(404) #if product does not exist in list of product titles, go to 404 (top)
	else: #if URL does not end with ?french
		if producttitle.title.get(productid):
			return render_template('product.html',product={
															'id':productid,
															'title':producttitle.title[productid],
															'text':producttext.text[productid],
															'dir':productdir.dir[productid],
															'info':productinfo.info[productid],
															'info2':productinfo.info2[productid],
															'demo':productdemo.demo[productid],
															'canforms':productforms.forms[productid + 'can'],
															'usforms':productforms.forms[productid + 'us'],
															'category':categoryproducts.products,
															'categoryimg':categoryimg.img,
															'categorytitle':categorytitle.title
														})
		else: abort(404)

@app.route('/category/<categoryid>')
def category(categoryid):
	if request.query_string == 'french':
		if frenchcategorytitle.title.get(categoryid):
			return render_template('frenchcategory.html', category={
																	'id':categoryid,
																	'title':frenchcategorytitle.title[categoryid],
																	'img':frenchcategoryimg.img[categoryid],
																	'products':frenchcategoryproducts.products[categoryid],
																	'dictlen':len(frenchcategoryproducts.products[categoryid])
																})
		else: abort(404)
	else:
		if categorytitle.title.get(categoryid):
			return render_template('category.html', category={
																'id':categoryid,
																'title':categorytitle.title[categoryid],
																'img':categoryimg.img[categoryid],
																'products':categoryproducts.products[categoryid],
																'dictlen':len(categoryproducts.products[categoryid])
															})
		else: abort(404)

if __name__ == '__main__': #only run if executed directly from interpreter
    app.run(debug=True) #run server with application (debug on, must be turned off for deployment
