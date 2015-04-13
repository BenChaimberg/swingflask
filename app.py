import json,time
from time import localtime, strftime
from flask import Flask, render_template, url_for, request, abort, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required, fresh_login_required, LoginManager, UserMixin
from flask.ext.mail import Mail, Message
from werkzeug.routing import BaseConverter
import feedparser
from static.search_products import products_search
from static.search_forum import forum_search
import pymysql
from sqlalchemy import update
from forms import MessageForm, ForumSearchForm, LoginForm, BrochureForm, FrenchBrochureForm, ReferForm, FrenchReferForm
from models import db, Infotable, Infolist, Categories, Brands, Products, Frenchinfotable, Frenchinfolist, Frenchcategories, Frenchproducts, Messages, Replies, Brochures
#import logging
#from logging.handlers import RotatingFileHandler

RECAPTCHA_PUBLIC_KEY = '6LfnzAMTAAAAAD9RAodwUlTy8ju-gB_kb7_reass'
RECAPTCHA_PRIVATE_KEY = '6LfnzAMTAAAAAHvSepf1FyNClFx78uoVK7FBAfW2'

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

MAIL_SERVER='mail.swingpaints.com'
MAIL_PORT=25
MAIL_USE_TLS = False
MAIL_USE_SSL= False
MAIL_USERNAME = 'bchaimberg@swingpaints.com'
MAIL_PASSWORD = 'webmaster'

app = Flask(__name__) #created app as instance of Flask
app.config.from_object(__name__)
mail = Mail(app)
app.secret_key = '3dc26edf9d4f51a973bfc4b92171aac'
app.url_map.converters['regex'] = RegexConverter
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://swingpaint305734:103569@sql.megasqlservers.com:3306/circa1850_swingpaints_com'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 28799
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 14
db.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@login_manager.unauthorized_handler
def unauthorized():
	abort(401)

def generic_page(page,request,**kwargs):
	if request.args.get('lang') == 'french':
		page = 'french'+ page
	page += '.html'
	return render_template(page,**kwargs)

@app.context_processor
def utility_processor(): #creates template context processor function
	def product_category(category,id): #creates specific category for product function, takes arguments of all products in all categories and product id
		for item in category: #for every category in categories
			for item2 in category[item]: #for every product in category
				if item2 == id: #if product is equal to productid
					return item #return category
				if (id == '1818' or id == '1819') and item2 == '1817': #if productid is 1818 or 1819, not in list, so uses 1817 instead
					return item #return category
	def string_convert(x):
		return str(x)
	return dict(string_convert=string_convert,product_category=product_category) #returns function result)

@app.errorhandler(404)
def notfound(e): #if HTTP returns 404 error
    return render_template('404.html'), 404 #render 404 template and return 404 error
    
@app.errorhandler(500)
def apperror(e): #if HTTP returns 500 error
    return render_template('500.html'), 500 #render 500 template and return 500 error
    
@app.errorhandler(403)
def forbidden(e): #if HTTP returns 403 error
    return render_template('403.html'), 403 #render 403 template and return 403 error
    
@app.errorhandler(401)
def forbidden(e): #if HTTP returns 401 error
    return render_template('401.html'), 401 #render 401 template and return 401 error

@app.route('/static/<regex("[a-z_.-]*.py[ocd]{0,1}"):uid>')
def error(uid):
	abort(404)

@app.route('/login', methods=["GET", "POST"])
def login():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		if login_form.username.data == 'administrator' and login_form.password.data == 'supersecurepassword':
			user = load_user(login_form.username.data)
			login_user(user)
			return redirect('/admin/')
	return render_template("login.html",login_form=login_form)

@app.route('/admin/')
@fresh_login_required
def adminroot():
	return render_template('admin.html')

@app.route('/admin/<page>')
@fresh_login_required
def adminpage(page):
	if page == 'brochure':
		with open('brochurelist', 'r') as file:
			data = json.load(file)
		return render_template('adminbrochure.html',data=data,len=len(data))
	elif page == 'newsletter':
		with open('mailinglist', 'r') as file:
			data = json.load(file)
		return render_template('adminnewsletter.html',data=data,len=len(data))
	else: abort(404)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/home')

@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@app.route('/start', methods=('GET', 'POST'))
def start():
	return generic_page('start',request)

@app.route('/main', methods=('GET', 'POST'))
def home():
	return generic_page('main',request,feed=feedparser.parse('http://www.facebook.com/feeds/page.php?format=rss20&id=46670450858')['entries'][0]['link'])

@app.route('/forumsearch/<search_string>', methods=('GET', 'POST'))
def forumsearch(search_string):
	while True:
		plus = search_string.find('+')
		if plus > 0:
			search_string = search_string[:plus]+' '+search_string[plus+1:]
		else: break
	if request.query_string == 'french': return render_template('forumsearch.html')
	else: return render_template('forumsearch.html',searchitems=forum_search(search_string))

@app.route('/search/<search_string>', methods=('GET', 'POST'))
def search(search_string):
	while True:
		plus = search_string.find('+')
		if plus > 0:
			search_string = search_string[:plus]+' '+search_string[plus+1:]
		else: break
	return render_template('search.html',searchitems=products_search(search_string))

@app.route('/locations', methods=('GET', 'POST'))
def locations():
	return generic_page('locations',request)

@app.route('/faq', methods=('GET', 'POST'))
def faq():
	return generic_page('faq',request)

@app.route('/contact')
def contact():
	return generic_page('contact',request)

@app.route('/marketing')
def marketing():
	return generic_page('marketing',request)

@app.route('/about')
def about():
	return generic_page('about',request)

@app.route('/colour')
def colour():
	return generic_page('colour',request)

@app.route('/aquacolour')
def aquacolour():
	return generic_page('aquacolour',request)

@app.route('/rightstripper')
def rightstripper():
	return generic_page('rightstripper',request)

@app.route('/rightfinish')
def rightfinish():
	return generic_page('rightfinish',request)

@app.route('/forum/', methods=('GET', 'POST'))
@app.route('/forum/<int:page>', methods=('GET', 'POST'))
def forum(page=1):
	message_form = MessageForm()
	if message_form.validate_on_submit():
		new_message = Messages(message_form.subject.data,message_form.name.data,message_form.email.data,message_form.notifyemail.data,time.strftime("%Y-%m-%d %H:%M:%S", localtime()),message_form.message.data,time.strftime("%Y-%m-%d %H:%M:%S", localtime()))
		db.session.add(new_message)
		db.session.commit()
		msg = Message()
		msg.recipients = ['mchaimberg@swingpaints.com']
		msg.sender = ('Swing Paints', 'info@swingpaints.com')
		msg.subject = 'Swing Paints Forum Reply'
		msg.html = 'Hello Mark,<br />%s has posted a new message.<br />Click <a href="http://127.0.0.1:5000/message/%s#%s">here</a> to view the message board.<br />Yours sincerely,<br />Swing Paints' % (new_message.name,new_message.IDmessage,new_message.mdate)
		mail.send(msg)
		return redirect('/message/'+str(new_message.IDmessage))
	messages = Messages.query.with_entities(Messages.IDmessage,Messages.name,Messages.email,Messages.last_rdate,Messages.subject).order_by(Messages.last_rdate.desc()).paginate(int(page),50)
	for message in messages.items:
		message.replies = Replies.query.filter_by(IDmessage=message.IDmessage).count()
		message.date = time.strftime('%H:%M %m/%d/%Y',time.strptime(str(message.last_rdate),'%Y-%m-%d %H:%M:%S'))
	return render_template('forum.html',messages=messages,message_form=message_form)

@app.route('/message/<int:message_id>', methods=('GET', 'POST'))
def message(message_id):
	message_form = MessageForm()
	if message_form.validate_on_submit():
		last_reply = Replies.query.filter_by(IDmessage=message_id).order_by(Replies.rdate.desc()).first()
		new_reply = Replies(message_id,message_form.subject.data,message_form.name.data,message_form.email.data,message_form.notifyemail.data,message_form.message.data,time.strftime("%Y-%m-%d %H:%M:%S", localtime()))
		db.session.add(new_reply)
		db.session.commit()
		db.session.query(Messages).filter_by(IDmessage=message_id).update({'last_rdate':time.strftime("%Y-%m-%d %H:%M:%S", gmtime())})
		msg = Message()
		if last_reply.notifyemail == 'True':
			msg.recipients = [last_reply.email]
		msg.bcc = ['mchaimberg@swingpaints.com']
		msg.sender = ('Swing Paints', 'info@swingpaints.com')
		msg.subject = 'Swing Paints Forum Reply'
		msg.html = 'Hello %s,<br />%s has posted a reply to your message.<br />Click <a href="http://127.0.0.1:5000/message/%s#%s">here</a> to view the message board.<br />Yours sincerely,<br />Swing Paints' % (last_reply.name,new_reply.name,new_reply.IDmessage,new_reply.rdate)
		mail.send(msg)
	message = Messages.query.filter_by(IDmessage=message_id).first_or_404()
	message.date = time.strftime('%b %d, %Y<br />%H:%M:%S',time.strptime(str(message.mdate),'%Y-%m-%d %H:%M:%S'))
	replies = Replies.query.filter_by(IDmessage=message_id).order_by(Replies.rdate.asc()).all()
	for reply in replies:
		reply.date = time.strftime('%b %d, %Y<br />%H:%M:%S',time.strptime(str(reply.rdate),'%Y-%m-%d %H:%M:%S'))
	return render_template('message.html',message=message,replies=replies,message_form=message_form)

@app.route('/refer', methods=('GET', 'POST'))
def refer():
	if request.args.get('lang') == 'french': #if URL ends with ?french
		refer_form = FrenchReferForm()
		if refer_form.validate_on_submit():
			visitorname = refer_form.visitorname.data
			visitoremail = refer_form.visitoremail.data
			friendname = refer_form.friendname.data
			friendemail = refer_form.friendemail.data
			msg = Message()
			msg.recipients = [friendemail]
			msg.bcc = ['echaimberg@swingpaints.com']
			msg.sender = (visitorname, visitoremail)
			msg.subject = "Re: Une recommandation d'un ami - Decouvrez Peintures Swing!"
			msg.html = "%s,<br />S'il vous pla&#xee;t pardonnez l'intrusion, mais je crois que j'ai trouv&#xe9; quelque chose que vous seriez int&#xe9;ress&#xe9;. Je regardais &#xe0; travers les pages du site Web de cette soci&#xe9;t&#xe9; assez cool de finition du bois, Peintures Swing, et la pens&#xe9;e de vous. Donc, c&#x27;est la raison de cette \"presque \" e-mail personnelle. Vous pouvez les trouver <a href='http://swingpaints.herokuapp.com/?french'>ici</a>." % (friendname)
			mail.send(msg)
			return render_template('frenchrefersuccess.html')
		return render_template('frenchrefer.html', refer_form=refer_form)
	else: #if URL does not end with ?french
		refer_form = ReferForm()
		if refer_form.validate_on_submit():
			visitorname = refer_form.visitorname.data
			visitoremail = refer_form.visitoremail.data
			friendname = refer_form.friendname.data
			friendemail = refer_form.friendemail.data
			msg = Message()
			msg.recipients = [friendemail]
			msg.bcc = ['echaimberg@swingpaints.com']
			msg.sender = (visitorname, visitoremail)
			msg.subject = "Re: A referral from a friend - Check out Swing Paints!"
			msg.html = "%s,<br />Please forgive the intrusion but I think I found something that you'd be interested in. I was browsing through the pages of the website of this pretty cool wood finishing company, Swing Paints, and thought of you. So, that is the reason for this \"almost\" personal email. You can find them <a href='http://swingpaints.herokuapp.com'>here</a>." % (friendname)
			mail.send(msg)
			return render_template('refersuccess.html')
		return render_template('refer.html', refer_form=refer_form)

@app.route('/brochure', methods=('GET', 'POST'))
def brochure():
	brochure_form = BrochureForm()
	brochure_frenchform = FrenchBrochureForm()
	if brochure_frenchform.validate_on_submit():
		brochure = Brochures(brochure_frenchform.name.data,brochure_frenchform.email.data,brochure_frenchform.address.data,brochure_frenchform.city.data,brochure_frenchform.stateprov.data,brochure_frenchform.zipcode.data,brochure_frenchform.country.data,time.strftime("%Y-%m-%d %H:%M:%S", localtime()),'False')
		db.session.add(brochure)
		db.session.commit()
		msg = Message()
		msg.recipients = ['echaimberg@swingpaints.com']
		msg.sender = ("Swing Paints", "swingpaints@swingpaints.com")
		msg.subject = "%s would like a free brochure!" % brochure_frenchform.name.data
		msg.html = "name:&nbsp;%s<br />email:&nbsp;%s<br />address:&nbsp;%s<br />city:&nbsp;%s<br />stateprov:&nbsp;%s<br />zipcode:&nbsp;%s<br />country:&nbsp;%s<br />lang:&nbsp;en" % (brochure_frenchform.name.data,brochure_frenchform.email.data,brochure_frenchform.address.data,brochure_frenchform.city.data,brochure_frenchform.stateprov.data,brochure_frenchform.zipcode.data,brochure_frenchform.country.data)
#		mail.send(msg)
		return render_template('frenchbrochuresuccess.html')
	if brochure_form.validate_on_submit():
		brochure = Brochures(brochure_form.name.data,brochure_form.email.data,brochure_form.address.data,brochure_form.city.data,brochure_form.stateprov.data,brochure_form.zipcode.data,brochure_form.country.data,time.strftime("%Y-%m-%d %H:%M:%S", localtime()),'True')
		db.session.add(brochure)
		db.session.commit()
		msg = Message()
		msg.recipients = ['echaimberg@swingpaints.com']
		msg.sender = ("Swing Paints", "swingpaints@swingpaints.com")
		msg.subject = "%s would like a free brochure!" % brochure_form.name.data
		msg.html = "name:&nbsp;%s<br />email:&nbsp;%s<br />address:&nbsp;%s<br />city:&nbsp;%s<br />stateprov:&nbsp;%s<br />zipcode:&nbsp;%s<br />country:&nbsp;%s<br />lang:&nbsp;en" % (brochure_form.name.data,brochure_form.email.data,brochure_form.address.data,brochure_form.city.data,brochure_form.stateprov.data,brochure_form.zipcode.data,brochure_form.country.data)
#		mail.send(msg)
		return render_template('brochuresuccess.html')
	if request.args.get('lang') == 'french': return render_template('frenchbrochure.html', brochure_form=brochure_frenchform)
	else: return render_template('brochure.html', brochure_form=brochure_form)

@app.route('/product/<productid>')
def product(productid): #if URL is at /product/####
	if request.args.get('lang') == 'french': #if URL ends with ?french
		product = Frenchproducts.query.filter_by(id=productid).first_or_404()
		product.infolist = Frenchinfolist.query.filter_by(productid=productid).all()
		product.infotable = Frenchinfotable.query.filter_by(productid=productid).all()
		category=Frenchcategories.query.filter_by(category=product.category).first().name
		return render_template('frenchproduct.html',product=product,category=category)
	else: #if URL does not end with ?french
		product = Products.query.filter_by(id=productid).first_or_404()
		product.infolist = Infolist.query.filter_by(productid=productid).all()
		product.infotable = Infotable.query.filter_by(productid=productid).all()
		category=Categories.query.filter_by(category=product.category).first().name
		return render_template('product.html',product=product,category=category)

@app.route('/category/<string:categoryid>')
def category(categoryid):
	if request.args.get('lang') == 'french': #if URL ends with ?french
		category = Frenchcategories.query.filter_by(category=categoryid).first_or_404()
		category.products = Frenchproducts.query.with_entities(Frenchproducts.id,Frenchproducts.title).filter_by(category=categoryid).order_by(Products.id.asc()).all()
		category.dictlen = len(category.products)
		return render_template('frenchcategory.html', category=category)
	else:
		category = Categories.query.filter_by(category=categoryid).first_or_404()
		category.products = Products.query.with_entities(Products.id,Products.title).filter_by(category=categoryid).order_by(Products.id.asc()).all()
		category.dictlen = len(category.products)
		return render_template('category.html', category=category)

@app.route('/brand/<string:brandid>')
def brand(brandid):
	if request.args.get('lang') == 'french': #if URL ends with ?french
		brand = Brands.query.filter_by(brand=brandyid).first_or_404()
		brand.products = Frenchproducts.query.with_entities(Frenchproducts.id,Frenchproducts.title).filter(Products.brand.like('%'+brandid+'%')).order_by(Products.id.asc()).all()
		brand.dictlen = len(brand.products)
		return render_template('frenchcategory.html', category=brand)
	else:
		brand = Brands.query.filter_by(brand=brandid).first_or_404()
		brand.products = Products.query.with_entities(Products.id,Products.title).filter(Products.brand.like('%'+brandid+'%')).order_by(Products.id.asc()).all()
		brand.dictlen = len(brand.products)
		return render_template('category.html', category=brand)

if __name__ == '__main__': #only run if executed directly from interpreter
    app.run(debug=True,host='0.0.0.0') #run server with application (debug on, must be turned off for deployment)
