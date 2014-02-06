from flask import Flask
from flask import render_template
from flask import url_for
import producttitle
import producttext
import productdir
app = Flask(__name__)	

@app.route('/')
def index():
    return 'Ben Chaimberg\'s Flask wrapper. More to come. Be patient.'

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/product/<productid>')
def product(productid):
    return render_template('product.html', product={'id':productid,'title':producttitle.title[productid],'text':producttext.text[productid],'dir':productdir.dir[productid]})

if __name__ == '__main__':
    app.run()
