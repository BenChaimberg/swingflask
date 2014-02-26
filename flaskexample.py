from flask import Flask
from flask import render_template
from flask import url_for
from static import producttitle
from static import producttext
from static import productdir
from static import categorytitle
from static import categoryimg
from static import categoryproducts
app = Flask(__name__)	

@app.route('/')
def index():
	if request.args.get('french'):
        return 'french french french french'
	else:
		return 'Ben Chaimberg\'s Flask wrapper. More to come. Be patient.'

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product/<productid>')
def product(productid):
    return render_template('product.html', product={'id':productid,'title':producttitle.title[productid],'text':producttext.text[productid],'dir':productdir.dir[productid]})

@app.route('/category/<categoryid>')
def category(categoryid):
    return render_template('category.html', category={'id':categoryid,'title':categorytitle.title[categoryid],'img':categoryimg.img[categoryid],'products':categoryproducts.products[categoryid]})

if __name__ == '__main__':
    app.run(debug=True)
