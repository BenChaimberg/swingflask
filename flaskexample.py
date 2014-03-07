from flask import Flask, render_template, url_for, request
from static import producttitle, producttext, productdir, productinfo, frenchproducttitle, frenchproducttext, frenchproductdir, frenchproductinfo, categoryimg, categorytitle, categoryproducts, frenchcategoryimg, frenchcategorytitle, frenchcategoryproducts
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

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

@app.route('/faq')
def faq():
	if request.query_string == 'french':
		return render_template('frenchfaq.html')
	else:
		return render_template('faq.html')
		
@app.route('/faq/<id>')
def faqa(id):
    return render_template('faqa.html', faqa={'id':id})
		
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
		return render_template('frenchproduct.html', product={'id':productid,'title':frenchproducttitle.title[productid],'text':frenchproducttext.text[productid],'dir':frenchproductdir.dir[productid],'info':frenchproductinfo.info[productid],'info2':frenchproductinfo.info2[productid]})
	else:
		return render_template('product.html', product={'id':productid,'title':producttitle.title[productid],'text':producttext.text[productid],'dir':productdir.dir[productid],'info':productinfo.info[productid],'info2':productinfo.info2[productid]})

@app.route('/category/<categoryid>')
def category(categoryid):
	if request.query_string == 'french':
		return render_template('frenchcategory.html', category={'id':categoryid,'title':frenchcategorytitle.title[categoryid],'img':frenchcategoryimg.img[categoryid],'products':frenchcategoryproducts.products[categoryid],'dictlen':len(frenchcategoryproducts.products[categoryid])})
	else:
		return render_template('category.html', category={'id':categoryid,'title':categorytitle.title[categoryid],'img':categoryimg.img[categoryid],'products':categoryproducts.products[categoryid],'dictlen':len(categoryproducts.products[categoryid])})

if __name__ == '__main__':
    app.run(debug=True)
