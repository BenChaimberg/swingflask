from flask import Flask, render_template, url_for, request, abort
from jinja2 import Environment
from static import producttitle, producttext, productdir, productinfo, productdemo, productforms, frenchproducttitle, frenchproducttext, frenchproductdir, frenchproductinfo, categoryimg, categorytitle, categoryproducts, frenchcategoryimg, frenchcategorytitle, frenchcategoryproducts
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.context_processor
def utility_processor():
	def product_category(category,id):
		for item in category:
			for item2 in category[item]:
				if item2 == id:
					return item
				if (id == '1818' or id == '1819') and item2 == '1817':
					return item
	return dict(product_category=product_category)

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def apperror(e):
    return render_template('500.html'), 500
    
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.route('/')
@app.route('/home')
def index():
	if request.query_string == 'french':
		return render_template('frenchmain.html')
	else:
		return render_template('main.html')

@app.route('/locations')
def locations():
	if request.query_string == 'french':
		return render_template('frenchlocations.html')
	else:
		return render_template('locations.html')

@app.route('/faq')
def faq():
	if request.query_string == 'french':
		return render_template('frenchfaq.html')
	else:
		return render_template('faq.html')
		
@app.route('/contact')
def contact():
	if request.query_string == 'french':
		return render_template('frenchcontact.html')
	else:
		return render_template('contact.html')

@app.route('/marketing')
def marketing():
	if request.query_string == 'french':
		return render_template('frenchmarketing.html')
	else:
		return render_template('marketing.html')

@app.route('/about')
def about():
	if request.query_string == 'french':
		return render_template('frenchabout.html')
	else:
		return render_template('about.html')

@app.route('/product/<productid>')
def product(productid):
	if request.query_string == 'french':
		if frenchproducttitle.title.get(productid):
			return render_template('frenchproduct.html', product={
																'id':productid,
																'title':frenchproducttitle.title[productid],
																'text':frenchproducttext.text[productid],
																'dir':frenchproductdir.dir[productid],
																'info':frenchproductinfo.info[productid]
															})
		else: abort(404)
	else:
		if producttitle.title.get(productid):
			if productforms.forms[productid + 'can']:
				return render_template('product.html',product={
																'id':productid,
																'title':producttitle.title[productid],
																'text':producttext.text[productid],
																'dir':productdir.dir[productid],
																'info':productinfo.info[productid],
																'demo':productdemo.demo[productid],
																'canforms':productforms.forms[productid + 'can'],
																'usforms':productforms.forms[productid + 'us'],
																'category':categoryproducts.products,
																'categoryimg':categoryimg.img,
																'categorytitle':categorytitle.title
															})
			else: abort(403)
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

if __name__ == '__main__':
    app.run(debug=True)
