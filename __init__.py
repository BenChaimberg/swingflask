import json,time
from time import gmtime, strftime
from flask import Flask, render_template, url_for, request, abort, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required, fresh_login_required, LoginManager, UserMixin
from flask.ext.mail import Mail, Message
from flask_wtf import Form, validators
from wtforms.fields import TextField, PasswordField, SelectField
import wtforms
from werkzeug.routing import BaseConverter
from static import producttitle, producttext, productdir, productinfo, productdemo, productforms, frenchproducttitle, frenchproducttext, frenchproductdir, frenchproductinfo, frenchproductdemo, frenchproductforms, categoryimg, categorytitle, categoryproducts, frenchcategoryimg, frenchcategorytitle, frenchcategoryproducts #import data in .py dictionary form
#import logging
#from logging.handlers import RotatingFileHandler

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
app.secret_key = 'blahblahblah' #change later to random
app.url_map.converters['regex'] = RegexConverter
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@login_manager.unauthorized_handler
def unauthorized():
	abort(401)

class LoginForm(Form):
    username = TextField("Username:", [wtforms.validators.Required('Please enter your username')])
    password = PasswordField("Password:", [wtforms.validators.Required('Please enter your password')])

class BrochureForm(Form):
    name = TextField("Name", [wtforms.validators.Required('Please enter your name')])
    email = TextField("E-mail", [wtforms.validators.Required('Please enter your email'), wtforms.validators.Email()])
    address = TextField("Address", [wtforms.validators.Required('Please enter your address')])
    city = TextField("City", [wtforms.validators.Required('Please enter your city')])
    stateprov = SelectField("State/Prov", [wtforms.validators.Required('Please enter your state or province')], choices=[('',''),('Alberta','Alberta'),('British Columbia','British Columbia'),('Manitoba','Manitoba'),('New Brunswick','New Brunswick'),('Newfoundland and Labrador','Newfoundland and Labrador'),('Northwest Territories','Northwest Territories'),('Nova Scotia','Nova Scotia'),('Nunavut','Nunavut'),('Ontario','Ontario'),('Prince Edward Island','Prince Edward Island'),('Quebec','Quebec'),('Saskatchewan','Saskatchewan'),('Yukon Territory','Yukon Territory'),('_',''),('Alabama','Alabama'),('Alaska','Alaska'),('Arizona','Arizona'),('Arkansas','Arkansas'),('California','California'),('Colorado','Colorado'),('Connecticut','Connecticut'),('Delaware','Delaware'),('Florida','Florida'),('Georgia','Georgia'),('Hawaii','Hawaii'),('Idaho','Idaho'),('Illinois','Illinois'),('Indiana','Indiana'),('Iowa','Iowa'),('Kansas','Kansas'),('Kentucky','Kentucky'),('Louisiana','Louisiana'),('Maine','Maine'),('Maryland','Maryland'),('Massachusetts','Massachusetts'),('Michigan','Michigan'),('Minnesota','Minnesota'),('Mississippi','Mississippi'),('Missouri','Missouri'),('Montana','Montana'),('Nebraska','Nebraska'),('Nevada','Nevada'),('New Hampshire','New Hampshire'),('New Jersey','New Jersey'),('New Mexico','New Mexico'),('New York','New York'),('North Carolina','North Carolina'),('North Dakota','North Dakota'),('Ohio','Ohio'),('Oklahoma','Oklahoma'),('Oregon','Oregon'),('Pennsylvania','Pennsylvania'),('Rhode Island','Rhode Island'),('South Carolina','South Carolina'),('South Dakota','South Dakota'),('Tennessee','Tennessee'),('Texas','Texas'),('Utah','Utah'),('Vermont','Vermont'),('Virginia','Virginia'),('Washington','Washington'),('West Virginia','West Virginia'),('Wisconsin','Wisconsin'),('Wyoming','Wyoming')])
    zipcode = TextField("Zip/Postal Code", [wtforms.validators.Required('Please enter your zip or postal code')])
    country = SelectField("Country", [wtforms.validators.Required('Please enter your country')], choices=[('',''),('Afghanistan','Afghanistan'),('Aland Islands','Aland Islands'),('Albania','Albania'),('Algeria','Algeria'),('American Samoa','American Samoa'),('Andorra','Andorra'),('Angola','Angola'),('Anguilla','Anguilla'),('Antarctica','Antarctica'),('Antigua And Barbuda','Antigua And Barbuda'),('Argentina','Argentina'),('Armenia','Armenia'),('Aruba','Aruba'),('Australia','Australia'),('Austria','Austria'),('Azerbaijan','Azerbaijan'),('Bahamas','Bahamas'),('Bahrain','Bahrain'),('Bangladesh','Bangladesh'),('Barbados','Barbados'),('Belarus','Belarus'),('Belgium','Belgium'),('Belize','Belize'),('Benin','Benin'),('Bermuda','Bermuda'),('Bhutan','Bhutan'),('Bolivia','Bolivia'),('Bosnia And Herzegovina','Bosnia And Herzegovina'),('Botswana','Botswana'),('Bouvet Island','Bouvet Island'),('Brazil','Brazil'),('British Indian Ocean Territory','British Indian Ocean Territory'),('Brunei Darussalam','Brunei Darussalam'),('Bulgaria','Bulgaria'),('Burkina Faso','Burkina Faso'),('Burundi','Burundi'),('Cambodia','Cambodia'),('Cameroon','Cameroon'),('Canada','Canada'),('Cape Verde','Cape Verde'),('Cayman Islands','Cayman Islands'),('Central African Republic','Central African Republic'),('Chad','Chad'),('Chile','Chile'),('China','China'),('Christmas Island','Christmas Island'),('Cocos (Keeling) Islands','Cocos (Keeling) Islands'),('Colombia','Colombia'),('Comoros','Comoros'),('Congo','Congo'),('Congo, The Democratic Republic Of The','Congo, The Democratic Republic Of The'),('Cook Islands','Cook Islands'),('Costa Rica','Costa Rica'),('Cote D\'ivoire','Cote D\'ivoire'),('Croatia','Croatia'),('Cuba','Cuba'),('Cyprus','Cyprus'),('Czech Republic','Czech Republic'),('Denmark','Denmark'),('Djibouti','Djibouti'),('Dominica','Dominica'),('Dominican Republic','Dominican Republic'),('Ecuador','Ecuador'),('Egypt','Egypt'),('El Salvador','El Salvador'),('Equatorial Guinea','Equatorial Guinea'),('Eritrea','Eritrea'),('Estonia','Estonia'),('Ethiopia','Ethiopia'),('Falkland Islands (Malvinas)','Falkland Islands (Malvinas)'),('Faroe Islands','Faroe Islands'),('Fiji','Fiji'),('Finland','Finland'),('France','France'),('French Guiana','French Guiana'),('French Polynesia','French Polynesia'),('French Southern Territories','French Southern Territories'),('Gabon','Gabon'),('Gambia','Gambia'),('Georgia','Georgia'),('Germany','Germany'),('Ghana','Ghana'),('Gibraltar','Gibraltar'),('Greece','Greece'),('Greenland','Greenland'),('Grenada','Grenada'),('Guadeloupe','Guadeloupe'),('Guam','Guam'),('Guatemala','Guatemala'),('Guernsey','Guernsey'),('Guinea','Guinea'),('Guinea-bissau','Guinea-bissau'),('Guyana','Guyana'),('Haiti','Haiti'),('Heard Island And Mcdonald Islands','Heard Island And Mcdonald Islands'),('Holy See (Vatican City State)','Holy See (Vatican City State)'),('Honduras','Honduras'),('Hong Kong','Hong Kong'),('Hungary','Hungary'),('Iceland','Iceland'),('India','India'),('Indonesia','Indonesia'),('Iran, Islamic Republic Of','Iran, Islamic Republic Of'),('Iraq','Iraq'),('Ireland','Ireland'),('Isle Of Man','Isle Of Man'),('Israel','Israel'),('Italy','Italy'),('Jamaica','Jamaica'),('Japan','Japan'),('Jersey','Jersey'),('Jordan','Jordan'),('Kazakhstan','Kazakhstan'),('Kenya','Kenya'),('Kiribati','Kiribati'),('Korea, Democratic People\'s Republic Of','Korea, Democratic People\'s Republic Of'),('Korea, Republic Of','Korea, Republic Of'),('Kuwait','Kuwait'),('Kyrgyzstan','Kyrgyzstan'),('Lao People\'s Democratic Republic','Lao People\'s Democratic Republic'),('Latvia','Latvia'),('Lebanon','Lebanon'),('Lesotho','Lesotho'),('Liberia','Liberia'),('Libyan Arab Jamahiriya','Libyan Arab Jamahiriya'),('Liechtenstein','Liechtenstein'),('Lithuania','Lithuania'),('Luxembourg','Luxembourg'),('Macao','Macao'),('Macedonia, The Former Yugoslav Republic Of','Macedonia, The Former Yugoslav Republic Of'),('Madagascar','Madagascar'),('Malawi','Malawi'),('Malaysia','Malaysia'),('Maldives','Maldives'),('Mali','Mali'),('Malta','Malta'),('Marshall Islands','Marshall Islands'),('Martinique','Martinique'),('Mauritania','Mauritania'),('Mauritius','Mauritius'),('Mayotte','Mayotte'),('Mexico','Mexico'),('Micronesia, Federated States Of','Micronesia, Federated States Of'),('Moldova, Republic Of','Moldova, Republic Of'),('Monaco','Monaco'),('Mongolia','Mongolia'),('Montenegro','Montenegro'),('Montserrat','Montserrat'),('Morocco','Morocco'),('Mozambique','Mozambique'),('Myanmar','Myanmar'),('Namibia','Namibia'),('Nauru','Nauru'),('Nepal','Nepal'),('Netherlands','Netherlands'),('Netherlands Antilles','Netherlands Antilles'),('New Caledonia','New Caledonia'),('New Zealand','New Zealand'),('Nicaragua','Nicaragua'),('Niger','Niger'),('Nigeria','Nigeria'),('Niue','Niue'),('Norfolk Island','Norfolk Island'),('Northern Mariana Islands','Northern Mariana Islands'),('Norway','Norway'),('Oman','Oman'),('Pakistan','Pakistan'),('Palau','Palau'),('Palestinian Territory, Occupied','Palestinian Territory, Occupied'),('Panama','Panama'),('Papua New Guinea','Papua New Guinea'),('Paraguay','Paraguay'),('Peru','Peru'),('Philippines','Philippines'),('Pitcairn','Pitcairn'),('Poland','Poland'),('Portugal','Portugal'),('Puerto Rico','Puerto Rico'),('Qatar','Qatar'),('Reunion','Reunion'),('Romania','Romania'),('Russian Federation','Russian Federation'),('Rwanda','Rwanda'),('Saint Helena','Saint Helena'),('Saint Kitts And Nevis','Saint Kitts And Nevis'),('Saint Lucia','Saint Lucia'),('Saint Pierre And Miquelon','Saint Pierre And Miquelon'),('Saint Vincent And The Grenadines','Saint Vincent And The Grenadines'),('Samoa','Samoa'),('San Marino','San Marino'),('Sao Tome And Principe','Sao Tome And Principe'),('Saudi Arabia','Saudi Arabia'),('Senegal','Senegal'),('Serbia','Serbia'),('Seychelles','Seychelles'),('Sierra Leone','Sierra Leone'),('Singapore','Singapore'),('Slovakia','Slovakia'),('Slovenia','Slovenia'),('Solomon Islands','Solomon Islands'),('Somalia','Somalia'),('South Africa','South Africa'),('South Georgia And The South Sandwich Islands','South Georgia And The South Sandwich Islands'),('Spain','Spain'),('Sri Lanka','Sri Lanka'),('Sudan','Sudan'),('Suriname','Suriname'),('Svalbard And Jan Mayen','Svalbard And Jan Mayen'),('Swaziland','Swaziland'),('Sweden','Sweden'),('Switzerland','Switzerland'),('Syrian Arab Republic','Syrian Arab Republic'),('Taiwan, Province Of China','Taiwan, Province Of China'),('Tajikistan','Tajikistan'),('Tanzania, United Republic Of','Tanzania, United Republic Of'),('Thailand','Thailand'),('Timor-leste','Timor-leste'),('Togo','Togo'),('Tokelau','Tokelau'),('Tonga','Tonga'),('Trinidad And Tobago','Trinidad And Tobago'),('Tunisia','Tunisia'),('Turkey','Turkey'),('Turkmenistan','Turkmenistan'),('Turks And Caicos Islands','Turks And Caicos Islands'),('Tuvalu','Tuvalu'),('Uganda','Uganda'),('Ukraine','Ukraine'),('United Arab Emirates','United Arab Emirates'),('United Kingdom','United Kingdom'),('United States','United States'),('United States Minor Outlying Islands','United States Minor Outlying Islands'),('Uruguay','Uruguay'),('Uzbekistan','Uzbekistan'),('Vanuatu','Vanuatu'),('Venezuela','Venezuela'),('Viet Nam','Viet Nam'),('Virgin Islands, British','Virgin Islands, British'),('Virgin Islands, U.S.','Virgin Islands, U.S.'),('Wallis And Futuna','Wallis And Futuna'),('Western Sahara','Western Sahara'),('Yemen','Yemen'),('Zambia','Zambia'),('Zimbabwe','Zimbabwe')])

class FrenchBrochureForm(Form):
    name = TextField("Nom", [wtforms.validators.Required('Veuillez entrer votre nom')])
    email = TextField("Couriel", [wtforms.validators.Required('Veuillez entrer votre couriel'), wtforms.validators.Email()])
    address = TextField("Adresse", [wtforms.validators.Required('Veuillez entrer votre adresse')])
    city = TextField("Ville", [wtforms.validators.Required('Veuillez entrer votre ville')])
    stateprov = SelectField("&#xc9;tat/Province", [wtforms.validators.Required('Veuillez entrer votre &#xe9;tat ou province')], choices=[('',''),('Alberta','Alberta'),('British Columbia','British Columbia'),('Manitoba','Manitoba'),('New Brunswick','New Brunswick'),('Newfoundland and Labrador','Newfoundland and Labrador'),('Northwest Territories','Northwest Territories'),('Nova Scotia','Nova Scotia'),('Nunavut','Nunavut'),('Ontario','Ontario'),('Prince Edward Island','Prince Edward Island'),('Quebec','Quebec'),('Saskatchewan','Saskatchewan'),('Yukon Territory','Yukon Territory'),('_',''),('Alabama','Alabama'),('Alaska','Alaska'),('Arizona','Arizona'),('Arkansas','Arkansas'),('California','California'),('Colorado','Colorado'),('Connecticut','Connecticut'),('Delaware','Delaware'),('Florida','Florida'),('Georgia','Georgia'),('Hawaii','Hawaii'),('Idaho','Idaho'),('Illinois','Illinois'),('Indiana','Indiana'),('Iowa','Iowa'),('Kansas','Kansas'),('Kentucky','Kentucky'),('Louisiana','Louisiana'),('Maine','Maine'),('Maryland','Maryland'),('Massachusetts','Massachusetts'),('Michigan','Michigan'),('Minnesota','Minnesota'),('Mississippi','Mississippi'),('Missouri','Missouri'),('Montana','Montana'),('Nebraska','Nebraska'),('Nevada','Nevada'),('New Hampshire','New Hampshire'),('New Jersey','New Jersey'),('New Mexico','New Mexico'),('New York','New York'),('North Carolina','North Carolina'),('North Dakota','North Dakota'),('Ohio','Ohio'),('Oklahoma','Oklahoma'),('Oregon','Oregon'),('Pennsylvania','Pennsylvania'),('Rhode Island','Rhode Island'),('South Carolina','South Carolina'),('South Dakota','South Dakota'),('Tennessee','Tennessee'),('Texas','Texas'),('Utah','Utah'),('Vermont','Vermont'),('Virginia','Virginia'),('Washington','Washington'),('West Virginia','West Virginia'),('Wisconsin','Wisconsin'),('Wyoming','Wyoming')])
    zipcode = TextField("Zip/Code Postal", [wtforms.validators.Required('Veuillez entrer votre code postal')])
    country = SelectField("Pays", [wtforms.validators.Required('Veuillez entrer votre pays')], choices=[('',''),('Afghanistan','Afghanistan'),('Aland Islands','Aland Islands'),('Albania','Albania'),('Algeria','Algeria'),('American Samoa','American Samoa'),('Andorra','Andorra'),('Angola','Angola'),('Anguilla','Anguilla'),('Antarctica','Antarctica'),('Antigua And Barbuda','Antigua And Barbuda'),('Argentina','Argentina'),('Armenia','Armenia'),('Aruba','Aruba'),('Australia','Australia'),('Austria','Austria'),('Azerbaijan','Azerbaijan'),('Bahamas','Bahamas'),('Bahrain','Bahrain'),('Bangladesh','Bangladesh'),('Barbados','Barbados'),('Belarus','Belarus'),('Belgium','Belgium'),('Belize','Belize'),('Benin','Benin'),('Bermuda','Bermuda'),('Bhutan','Bhutan'),('Bolivia','Bolivia'),('Bosnia And Herzegovina','Bosnia And Herzegovina'),('Botswana','Botswana'),('Bouvet Island','Bouvet Island'),('Brazil','Brazil'),('British Indian Ocean Territory','British Indian Ocean Territory'),('Brunei Darussalam','Brunei Darussalam'),('Bulgaria','Bulgaria'),('Burkina Faso','Burkina Faso'),('Burundi','Burundi'),('Cambodia','Cambodia'),('Cameroon','Cameroon'),('Canada','Canada'),('Cape Verde','Cape Verde'),('Cayman Islands','Cayman Islands'),('Central African Republic','Central African Republic'),('Chad','Chad'),('Chile','Chile'),('China','China'),('Christmas Island','Christmas Island'),('Cocos (Keeling) Islands','Cocos (Keeling) Islands'),('Colombia','Colombia'),('Comoros','Comoros'),('Congo','Congo'),('Congo, The Democratic Republic Of The','Congo, The Democratic Republic Of The'),('Cook Islands','Cook Islands'),('Costa Rica','Costa Rica'),('Cote D\'ivoire','Cote D\'ivoire'),('Croatia','Croatia'),('Cuba','Cuba'),('Cyprus','Cyprus'),('Czech Republic','Czech Republic'),('Denmark','Denmark'),('Djibouti','Djibouti'),('Dominica','Dominica'),('Dominican Republic','Dominican Republic'),('Ecuador','Ecuador'),('Egypt','Egypt'),('El Salvador','El Salvador'),('Equatorial Guinea','Equatorial Guinea'),('Eritrea','Eritrea'),('Estonia','Estonia'),('Ethiopia','Ethiopia'),('Falkland Islands (Malvinas)','Falkland Islands (Malvinas)'),('Faroe Islands','Faroe Islands'),('Fiji','Fiji'),('Finland','Finland'),('France','France'),('French Guiana','French Guiana'),('French Polynesia','French Polynesia'),('French Southern Territories','French Southern Territories'),('Gabon','Gabon'),('Gambia','Gambia'),('Georgia','Georgia'),('Germany','Germany'),('Ghana','Ghana'),('Gibraltar','Gibraltar'),('Greece','Greece'),('Greenland','Greenland'),('Grenada','Grenada'),('Guadeloupe','Guadeloupe'),('Guam','Guam'),('Guatemala','Guatemala'),('Guernsey','Guernsey'),('Guinea','Guinea'),('Guinea-bissau','Guinea-bissau'),('Guyana','Guyana'),('Haiti','Haiti'),('Heard Island And Mcdonald Islands','Heard Island And Mcdonald Islands'),('Holy See (Vatican City State)','Holy See (Vatican City State)'),('Honduras','Honduras'),('Hong Kong','Hong Kong'),('Hungary','Hungary'),('Iceland','Iceland'),('India','India'),('Indonesia','Indonesia'),('Iran, Islamic Republic Of','Iran, Islamic Republic Of'),('Iraq','Iraq'),('Ireland','Ireland'),('Isle Of Man','Isle Of Man'),('Israel','Israel'),('Italy','Italy'),('Jamaica','Jamaica'),('Japan','Japan'),('Jersey','Jersey'),('Jordan','Jordan'),('Kazakhstan','Kazakhstan'),('Kenya','Kenya'),('Kiribati','Kiribati'),('Korea, Democratic People\'s Republic Of','Korea, Democratic People\'s Republic Of'),('Korea, Republic Of','Korea, Republic Of'),('Kuwait','Kuwait'),('Kyrgyzstan','Kyrgyzstan'),('Lao People\'s Democratic Republic','Lao People\'s Democratic Republic'),('Latvia','Latvia'),('Lebanon','Lebanon'),('Lesotho','Lesotho'),('Liberia','Liberia'),('Libyan Arab Jamahiriya','Libyan Arab Jamahiriya'),('Liechtenstein','Liechtenstein'),('Lithuania','Lithuania'),('Luxembourg','Luxembourg'),('Macao','Macao'),('Macedonia, The Former Yugoslav Republic Of','Macedonia, The Former Yugoslav Republic Of'),('Madagascar','Madagascar'),('Malawi','Malawi'),('Malaysia','Malaysia'),('Maldives','Maldives'),('Mali','Mali'),('Malta','Malta'),('Marshall Islands','Marshall Islands'),('Martinique','Martinique'),('Mauritania','Mauritania'),('Mauritius','Mauritius'),('Mayotte','Mayotte'),('Mexico','Mexico'),('Micronesia, Federated States Of','Micronesia, Federated States Of'),('Moldova, Republic Of','Moldova, Republic Of'),('Monaco','Monaco'),('Mongolia','Mongolia'),('Montenegro','Montenegro'),('Montserrat','Montserrat'),('Morocco','Morocco'),('Mozambique','Mozambique'),('Myanmar','Myanmar'),('Namibia','Namibia'),('Nauru','Nauru'),('Nepal','Nepal'),('Netherlands','Netherlands'),('Netherlands Antilles','Netherlands Antilles'),('New Caledonia','New Caledonia'),('New Zealand','New Zealand'),('Nicaragua','Nicaragua'),('Niger','Niger'),('Nigeria','Nigeria'),('Niue','Niue'),('Norfolk Island','Norfolk Island'),('Northern Mariana Islands','Northern Mariana Islands'),('Norway','Norway'),('Oman','Oman'),('Pakistan','Pakistan'),('Palau','Palau'),('Palestinian Territory, Occupied','Palestinian Territory, Occupied'),('Panama','Panama'),('Papua New Guinea','Papua New Guinea'),('Paraguay','Paraguay'),('Peru','Peru'),('Philippines','Philippines'),('Pitcairn','Pitcairn'),('Poland','Poland'),('Portugal','Portugal'),('Puerto Rico','Puerto Rico'),('Qatar','Qatar'),('Reunion','Reunion'),('Romania','Romania'),('Russian Federation','Russian Federation'),('Rwanda','Rwanda'),('Saint Helena','Saint Helena'),('Saint Kitts And Nevis','Saint Kitts And Nevis'),('Saint Lucia','Saint Lucia'),('Saint Pierre And Miquelon','Saint Pierre And Miquelon'),('Saint Vincent And The Grenadines','Saint Vincent And The Grenadines'),('Samoa','Samoa'),('San Marino','San Marino'),('Sao Tome And Principe','Sao Tome And Principe'),('Saudi Arabia','Saudi Arabia'),('Senegal','Senegal'),('Serbia','Serbia'),('Seychelles','Seychelles'),('Sierra Leone','Sierra Leone'),('Singapore','Singapore'),('Slovakia','Slovakia'),('Slovenia','Slovenia'),('Solomon Islands','Solomon Islands'),('Somalia','Somalia'),('South Africa','South Africa'),('South Georgia And The South Sandwich Islands','South Georgia And The South Sandwich Islands'),('Spain','Spain'),('Sri Lanka','Sri Lanka'),('Sudan','Sudan'),('Suriname','Suriname'),('Svalbard And Jan Mayen','Svalbard And Jan Mayen'),('Swaziland','Swaziland'),('Sweden','Sweden'),('Switzerland','Switzerland'),('Syrian Arab Republic','Syrian Arab Republic'),('Taiwan, Province Of China','Taiwan, Province Of China'),('Tajikistan','Tajikistan'),('Tanzania, United Republic Of','Tanzania, United Republic Of'),('Thailand','Thailand'),('Timor-leste','Timor-leste'),('Togo','Togo'),('Tokelau','Tokelau'),('Tonga','Tonga'),('Trinidad And Tobago','Trinidad And Tobago'),('Tunisia','Tunisia'),('Turkey','Turkey'),('Turkmenistan','Turkmenistan'),('Turks And Caicos Islands','Turks And Caicos Islands'),('Tuvalu','Tuvalu'),('Uganda','Uganda'),('Ukraine','Ukraine'),('United Arab Emirates','United Arab Emirates'),('United Kingdom','United Kingdom'),('United States','United States'),('United States Minor Outlying Islands','United States Minor Outlying Islands'),('Uruguay','Uruguay'),('Uzbekistan','Uzbekistan'),('Vanuatu','Vanuatu'),('Venezuela','Venezuela'),('Viet Nam','Viet Nam'),('Virgin Islands, British','Virgin Islands, British'),('Virgin Islands, U.S.','Virgin Islands, U.S.'),('Wallis And Futuna','Wallis And Futuna'),('Western Sahara','Western Sahara'),('Yemen','Yemen'),('Zambia','Zambia'),('Zimbabwe','Zimbabwe')])

class ReferForm(Form):
    visitorname = TextField("Your name", [wtforms.validators.Required('Please enter your name')])
    visitoremail = TextField("Your email", [wtforms.validators.Required('Please enter your email'), wtforms.validators.Email()])
    friendname = TextField("Your friend's name", [wtforms.validators.Required('Please enter your friend&apos;s name')])
    friendemail = TextField("Your friend's email", [wtforms.validators.Required('Please enter your friend&apos;s email'), wtforms.validators.Email()])

class FrenchReferForm(Form):
    visitorname = TextField("Votre nom", [wtforms.validators.Required('Veuillez entrer votre nom')])
    visitoremail = TextField("Votre adresse de courriel", [wtforms.validators.Required('Veuillez entrer votre adresse de courriel'), wtforms.validators.Email()])
    friendname = TextField("Le nom de votre amie", [wtforms.validators.Required('Veuillez entrer le nom de votre amie')])
    friendemail = TextField("Son adresse de courriel", [wtforms.validators.Required('Veuillez entrer son adresse de courriel'), wtforms.validators.Email()])

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
    form = LoginForm()
    if form.validate_on_submit():
    	if form.username.data == 'administrator' and form.password.data == 'supersecurepassword':
    		user = load_user(form.username.data)
        	login_user(user)
        	return redirect('/admin/')
    return render_template("login.html", form=form)

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

@app.route('/colour')
def colour(): #if URL is at about
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchcolour.html') #render french about page
	else: #if URL does not end with ?french
		return render_template('colour.html') #return english about page

@app.route('/aquacolour')
def aquacolour(): #if URL is at about
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchaquacolour.html') #render french about page
	else: #if URL does not end with ?french
		return render_template('aquacolour.html') #return english about page

@app.route('/rightstripper')
def rightstripper(): #if URL is at about
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchrightstripper.html') #render french about page
	else: #if URL does not end with ?french
		return render_template('rightstripper.html') #return english about page

@app.route('/rightfinish')
def rightfinish(): #if URL is at about
	if request.query_string == 'french': #if URL ends with ?french
		return render_template('frenchrightfinish.html') #render french about page
	else: #if URL does not end with ?french
		return render_template('rightfinish.html') #return english about page

@app.route('/refer', methods=('GET', 'POST'))
def refer():
	if request.query_string == 'french': #if URL ends with ?french
		form = FrenchReferForm()
		if form.validate_on_submit():
			visitorname = form.visitorname.data
			visitoremail = form.visitoremail.data
			friendname = form.friendname.data
			friendemail = form.friendemail.data
			msg = Message()
			msg.recipients = [friendemail]
			msg.bcc = ['echaimberg@swingpaints.com']
			msg.sender = (visitorname, visitoremail)
			msg.subject = "Re: Une recommandation d'un ami - Decouvrez Peintures Swing!"
			msg.html = "%s,<br />S'il vous pla&#xee;t pardonnez l'intrusion, mais je crois que j'ai trouv&#xe9; quelque chose que vous seriez int&#xe9;ress&#xe9;. Je regardais &#xe0; travers les pages du site Web de cette soci&#xe9;t&#xe9; assez cool de finition du bois, Peintures Swing, et la pens&#xe9;e de vous. Donc, c&#x27;est la raison de cette \"presque \" e-mail personnelle. Vous pouvez les trouver <a href='http://swingpaints.herokuapp.com/?french'>ici</a>." % (friendname)
			mail.send(msg)
			return render_template('frenchrefersuccess.html')
		return render_template('frenchrefer.html', form=form)
	else: #if URL does not end with ?french
		form = ReferForm()
		if form.validate_on_submit():
			visitorname = form.visitorname.data
			visitoremail = form.visitoremail.data
			friendname = form.friendname.data
			friendemail = form.friendemail.data
			msg = Message()
			msg.recipients = [friendemail]
			msg.bcc = ['echaimberg@swingpaints.com']
			msg.sender = (visitorname, visitoremail)
			msg.subject = "Re: A referral from a friend - Check out Swing Paints!"
			msg.html = "%s,<br />Please forgive the intrusion but I think I found something that you'd be interested in. I was browsing through the pages of the website of this pretty cool wood finishing company, Swing Paints, and thought of you. So, that is the reason for this \"almost\" personal email. You can find them <a href='http://swingpaints.herokuapp.com'>here</a>." % (friendname)
			mail.send(msg)
			return render_template('refersuccess.html')
		return render_template('refer.html', form=form)

@app.route('/brochure', methods=('GET', 'POST'))
def brochure():
	form = BrochureForm()
	frenchform = FrenchBrochureForm()
	if form.validate_on_submit():
		with open('brochurelist', 'r') as file:
			data = json.load(file)
		i=0
		for item in data:
			i+=1
		if request.query_string == 'french': lang = 'fr'
		else: lang = 'en'
		writedata = {i:{'name':form.name.data,'email':form.email.data,'address':form.address.data,'city':form.city.data,'stateprov':form.stateprov.data,'zipcode':form.zipcode.data,'country':form.country.data,'time':time.strftime("%m/%d/%Y %I:%M:%S %p", gmtime()),'lang':lang}}
		data.update(writedata)
		with open('brochurelist', 'w') as file:
			json.dump(data,file,sort_keys=True,indent=4)
		msg = Message()
		msg.recipients = ['echaimberg@swingpaints.com']
		msg.sender = ("Swing Paints", "swingpaints@swingpaints.com")
		msg.subject = "%s would like a free brochure!" % form.name.data
		msg.html = "name:&nbsp;%s<br />email:&nbsp;%s<br />address:&nbsp;%s<br />city:&nbsp;%s<br />stateprov:&nbsp;%s<br />zipcode:&nbsp;%s<br />country:&nbsp;%s<br />lang:&nbsp;en" % (form.name.data,form.email.data,form.address.data,form.city.data,form.stateprov.data,form.zipcode.data,form.country.data)
		mail.send(msg)
		if request.query_string == 'french': return render_template('frenchbrochuresuccess.html')
		else: return render_template('brochuresuccess.html')
	if request.query_string == 'french': return render_template('frenchbrochure.html', form=frenchform)
	else: return render_template('brochure.html', form=form)

@app.route('/product/<productid>')
def product(productid): #if URL is at /product/####
	if request.query_string == 'french': #if URL ends with ?french
		if frenchproducttitle.title.get(productid): #if product exists in list of product titles (should contain all products)
			return render_template('frenchproduct.html', product={ #renders french product page with the following parameters
																'id':productid, #product.id = productid
																'title':frenchproducttitle.title[productid], #product.title = string with product name
																'text':frenchproducttext.text[productid], #product.text = string with product text
																'dir':frenchproductdir.dir[productid], #product.dir = string with product directions
																'info':frenchproductinfo.info[productid], #product.info = string with product info (table)
																'info2':frenchproductinfo.info2[productid],
																'demo':frenchproductdemo.demo[productid],
																'canforms':frenchproductforms.forms[productid + 'can'],
																'usforms':frenchproductforms.forms[productid + 'us'],
																'category':frenchcategoryproducts.products,
																'categoryimg':frenchcategoryimg.img,
																'categorytitle':frenchcategorytitle.title
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
    app.run(debug=False,host= '0.0.0.0') #run server with application (debug on, must be turned off for deployment)
