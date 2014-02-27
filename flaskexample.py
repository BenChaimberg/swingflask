from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from static import producttitle
from static import producttext
from static import productdir
from static import categorytitle
from static import categoryimg
from static import categoryproducts
app = Flask(__name__)	

@app.route('/')
@app.route('/home')
def index():
	if request.query_string == 'french':
		return render_template('frenchmain.html')
	else:
		return render_template('main.html')

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/about')
def about():
	if request.query_string == 'french':
		return render_template('frenchabout.html')
	else:
		return render_template('about.html')

@app.route('/product/<productid>')
def product(productid):
    return render_template('product.html', product={'id':productid,'title':producttitle.title[productid],'text':producttext.text[productid],'dir':productdir.dir[productid]})

@app.route('/category/<categoryid>')
def category(categoryid):
    return render_template('category.html', category={'id':categoryid,'title':categorytitle.title[categoryid],'img':categoryimg.img[categoryid],'products':categoryproducts.products[categoryid]})

if __name__ == '__main__':
    app.run(debug=True)
