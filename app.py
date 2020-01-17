import time
import re
import os
import ConfigParser
import werkzeug
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    abort,
    redirect,
    flash
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager,
    UserMixin
)
from flask_mail import Mail, Message
from flask_admin import Admin
from flask_sitemap import Sitemap
from flask_sslify import SSLify
from werkzeug.routing import BaseConverter, BuildError
from search_products import products_search
from search_forum import forum_search
from sqlalchemy import func
from locations import postal_dist, CodeException
from forms import (
    LocationsForm,
    MessageForm,
    FrenchMessageForm,
    LoginForm,
    BrochureForm,
    FrenchBrochureForm,
    ReferForm,
    FrenchReferForm
)
from models import (
    db,
    Brands,
    Brochures,
    Categories,
    Frenchcategories,
    Frenchinfolist,
    Frenchinfotable,
    Frenchproducts,
    Infolist,
    Infotable,
    Messages,
    Newsletter,
    Products,
    Replies
)
from admin import (
    MessageModelView,
    ReplyModelView,
    ProductModelView,
    CategoryModelView,
    BrandModelView,
    NewsletterModelView,
    InfoTableModelView,
    InfoListModelView,
    BrochureModelView,
    CustomFileAdmin,
    ProtectedAdminIndexView
)

config = ConfigParser.RawConfigParser()
config.read('swingflask.conf')

MAIL_SERVER = config.get('mail', 'server')
MAIL_PORT = config.getint('mail', 'port')
MAIL_USE_TLS = config.getboolean('mail', 'tls')
MAIL_USE_SSL = config.getboolean('mail', 'ssl')
MAIL_USERNAME = config.get('mail', 'username')
MAIL_PASSWORD = config.get('mail', 'password')
MAIL_DEFAULT_SENDER = config.get('mail', 'sender')

RECAPTCHA_PUBLIC_KEY = config.get('recaptcha', 'public_key')
RECAPTCHA_PRIVATE_KEY = config.get('recaptcha', 'private_key')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = config.getboolean('app', 'debug')
app.config['SECRET_KEY'] = config.get('app', 'secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = ''.join([
    config.get('mysql', 'dialect'),
    '+',
    config.get('mysql', 'driver'),
    '://',
    config.get('mysql', 'username'),
    ':',
    config.get('mysql', 'password'),
    '@',
    config.get('mysql', 'host'),
    ':',
    config.get('mysql', 'port'),
    '/',
    config.get('mysql', 'database')
])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

admin = Admin(
    index_view=ProtectedAdminIndexView()
)
admin.init_app(app)
admin.add_view(
    BrandModelView(Brands, db.session, category='Database')
)
admin.add_view(
    BrochureModelView(Brochures, db.session, category='Database')
)
admin.add_view(
    CategoryModelView(Categories, db.session, category='Database')
)
admin.add_view(
    CategoryModelView(Frenchcategories, db.session, category='Database')
)
admin.add_view(
    ProductModelView(Frenchproducts, db.session, category='Database')
)
admin.add_view(
    InfoListModelView(Infolist, db.session, category='Database')
)
admin.add_view(
    InfoTableModelView(Infotable, db.session, category='Database')
)
admin.add_view(
    MessageModelView(Messages, db.session, category='Database')
)
admin.add_view(
    NewsletterModelView(Newsletter, db.session, category='Database')
)
admin.add_view(
    ProductModelView(Products, db.session, category='Database')
)
admin.add_view(
    ReplyModelView(Replies, db.session, category='Database')
)
admin.add_view(
    CustomFileAdmin(
        os.path.join(os.path.dirname(__file__), 'static'),
        '/static/',
        name='Static Files',
        endpoint='static'
    )
)

sitemap = Sitemap(app)

sslify = SSLify(app)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


def regex_replace(value, find=r'', replace=r''):
    return re.sub(find, replace, value)


app.jinja_env.filters['regex_replace'] = regex_replace


def sidebar_lang_render(page, request, **kwargs):
    page_html = ''.join([page, '.html'])
    if request.args.get('lang') == 'french':
        lang_page_html = ''.join(['french', page_html])
        categories = Frenchcategories.query.with_entities(
            Frenchcategories.category,
            Frenchcategories.name
        ).order_by(Frenchcategories.id.asc()).all()
    else:
        lang_page_html = page_html
        categories = Categories.query.with_entities(
            Categories.category,
            Categories.name
        ).order_by(Categories.id.asc()).all()
    brands = Brands.query.with_entities(
        Brands.brand,
        Brands.name
    ).order_by(Brands.id.asc()).all()
    return render_template(
        lang_page_html,
        categories=categories,
        brands=brands,
        **kwargs
    )


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('error', ''.join(['Form error: ', error]))


@app.context_processor
def utility_processor():
    def product_category(category, id):
        for item in category:
            for item2 in category[item]:
                if item2 == id:
                    return item
                if (id == '1818' or id == '1819') and item2 == '1817':
                    return item

    def string_convert(x):
        return str(x)
    return dict(
        string_convert=string_convert,
        product_category=product_category
    )


@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def apperror(e):
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


def product_title_sub(title):
    subbed_title = re.sub(r'(?:<br>|\s)', '-', title)
    m = re.search(r'&#x\d+;', subbed_title)
    while m is not None:
        subbed_title = subbed_title[:m.start()] + \
            unichr(int(subbed_title[m.start()+3:m.end()-1], 16)) + \
            subbed_title[m.end():]
        m = re.search(r'&#x\d+;', subbed_title)
    return subbed_title


@app.route('/product.php')
@app.route('/productMobile.php')
@app.route('/productIE.php')
def product_php_old_redirect():
    try:
        return redirect(url_for(
            'product',
            productid=request.args.get('id')
        ), code=301)
    except BuildError:
        abort(404)


@app.route('/<regex("[0-9_]+((us)|(can)|(us_can))?\.htm"):uid>')
def product_old_redirect(uid):
    uid = re.sub(r'(us|can)?(_.+)?\.htm', r'', uid)
    return redirect(url_for('product', productid=str(uid)), code=301)


@app.route('/<regex("french/[0-9_]+\.htm"):uid>')
def french_product_old_redirect(uid):
    uid = re.sub(r'french/', r'', re.sub(r'\.htm', r'', uid))
    return redirect(url_for(
        'product',
        productid=str(uid), lang='french'
    ), code=301)


@app.route('/<regex(".*more_info_[0-9_]*\.htm"):regid>')
def more_info_old_redirect(regid):
    try:
        uid = int(re.sub(r'_\d+', r'', str(regid)[10:-4]))
        return redirect(url_for('product', productid=str(uid)), code=301)
    except ValueError:
        uid = re.sub(r'_\d+', r'', str(regid)[17:-4])
        return redirect(url_for('product', productid=uid), code=301)


@app.route('/<regex(".*directions_[0-9_]*\.htm"):regid>')
def directions_old_redirect(regid):
    try:
        uid = int(re.sub(r'_\d+', r'', str(regid)[11:-4]))
        return redirect(url_for('product', productid=str(uid)), code=301)
    except ValueError:
        uid = re.sub(r'_\d+', r'', str(regid)[18:-4])
        return redirect(url_for('product', productid=uid), code=301)


@app.route('/category.php')
@app.route('/categoryMobile.php')
def category_php_old_redirect():
    category_hash = {
        'nontoxic': 'waxes',
        'oils': 'oils',
        'poly': 'poly',
        'remover': 'varnishremovers',
        'primer': 'primers',
        'special': 'epoxies',
        'waxes': 'waxes',
        'stain': 'stains',
        'accessories': 'accessories'
    }
    try:
        return redirect(url_for(
            'category',
            categoryid=category_hash[request.args.get('type')]
        ), code=301)
    except KeyError:
        abort(404)


@app.route('/<regex("((?!a_).)*\.htm"):regid>')
def category_old_redirect(regid):
    uid = str(regid)[:-4]
    category_hash = {
        'non_toxic': 'waxes',
        'oils_varnish_poly': 'poly',
        'paint_varnish_removers': 'varnishremovers',
        'paint_wallpaper_primers': 'primers',
        'specialty_paints_coating': 'epoxies',
        'waxes_polishes_cleaners': 'waxes',
        'wood_varnish_stains': 'stains',
        'accessories': 'accessories'
    }
    try:
        return redirect(url_for(
            'category',
            categoryid=category_hash[uid[0:]]
        ), code=301)
    except KeyError:
        try:
            return redirect(url_for(
                'category',
                categoryid=category_hash[uid[7:]],
                lang='french'
            ), code=301)
        except KeyError:
            abort(404)


@app.route('/<regex("(french/)?a_.+\.(htm|php)"):regid>')
def menu_old_redirect(regid):
    uid = re.sub(r'^a_', r'', str(regid)[0:-4])
    menu_hash = {
        'about_swing': 'about',
        'where_to_buy': 'locations',
        'faq': 'faq',
        'faq1': 'faq',
        'faq2': 'faq',
        'faq3': 'faq',
        'faq4': 'faq',
        'faq5': 'faq',
        'faq6': 'faq',
        'faq7': 'faq',
        'faq8': 'faq',
        'contact_swing': 'contact',
        'free_brochure': 'brochure'
    }
    try:
        return redirect(url_for(menu_hash[uid]), code=301)
    except KeyError:
        try:
            return redirect(url_for(
                menu_hash[uid[9:]],
                lang='french'
            ), code=301)
        except KeyError:
            abort(404)


@app.route('/refer_a_friend.htm')
@app.route('/refer.php')
def refer_old_redirect():
    return redirect(url_for('refer'), code=301)


@app.route('/french/refer_a_friend.htm')
def french_refer_old_redirect():
    return redirect(url_for('refer', lang='french'), code=301)


@app.route('/marketing.htm')
@app.route('/marketing.php')
def marketing_old_redirect():
    return redirect(url_for('refer'), code=301)


@app.route('/french/marketing.htm')
def french_marketing_old_redirect():
    return redirect(url_for('refer', lang='french'), code=301)


@app.route('/main.html')
def main_old_redirect():
    return redirect(url_for('home'), code=301)


@app.route('/french/main.html')
def french_main_old_redirect():
    return redirect(url_for('home', lang='french'), code=301)


@app.route('/right_stripper.htm')
def right_stripper_old_redirect():
    return redirect(url_for('right_stripper'), code=301)


@app.route('/french/right_stripper.htm')
def french_right_stripper_old_redirect():
    return redirect(url_for('right_stripper', lang='french'), code=301)


@app.route('/forum.asp')
def forum_old_redirect():
    try:
        return redirect(url_for(
            'forum',
            page=request.args.get('pg')
        ), code=301)
    except ValueError:
        abort(404)


@app.route('/viewmessage.asp')
def message_old_redirect():
    try:
        return redirect(url_for(
            'message',
            message_id=request.args.get('id')
        ), code=301)
    except ValueError:
        abort(404)
    except werkzeug.routing.BuildError:
        abort(404)


@app.route('/401')
def e401():
    abort(401)


@app.route('/403')
def e403():
    abort(403)


@app.route('/404')
def e404():
    abort(404)


@app.route('/500')
def e500():
    abort(500)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@login_manager.unauthorized_handler
def login_unauthorized():
    abort(401)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if current_user.is_authenticated():
        return redirect('/admin/')
    if login_form.validate_on_submit():
        user = load_user(login_form.username.data)
        login_user(user)
        return redirect('/admin/')
    else:
        flash_errors(login_form)
    return sidebar_lang_render("login", request, login_form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/home')


@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@app.route('/start', methods=('GET', 'POST'))
@app.route('/main', methods=('GET', 'POST'))
def home():
    return sidebar_lang_render('main', request, fbToken=config.get('facebook', 'token'))


@sitemap.register_generator
def sitemap_generator():
    endpoints = ['home', 'locations', 'faq', 'contact', 'marketing', 'about', 'gallery', 'colour', 'aquacolour', 'rightstripper', 'rightfinish', 'refer', 'brochure']
    for endpoint in endpoints:
        yield (endpoint, {})
        yield (endpoint, {'lang': 'french'})
    last_reply = db.session.query(db.func.max(Messages.last_rdate)).scalar().isoformat() + "-05:00"
    for page in range(Messages.query.paginate(1, 50).pages):
        yield ('forum', {'page': page+1}, last_reply)
    for category in Categories.query.with_entities(Categories.category).all():
        yield ('category', {'categoryid': category[0]})
    for brand in Brands.query.with_entities(Brands.brand).all():
        yield ('brand', {'brandid': brand[0]})
    for product in Products.query.with_entities(Products.id, Products.title).all():
        yield ('product_string', {'regid': str(product[0]) + '/' + product_title_sub(product[1])})
    for frenchproduct in Frenchproducts.query.with_entities(Frenchproducts.id, Frenchproducts.title).all():
        yield ('product_string', {'regid': str(frenchproduct[0]) + '/' + product_title_sub(frenchproduct[1]), 'lang': 'french'})
    for message in Messages.query.with_entities(Messages.IDmessage, Messages.last_rdate).all():
        yield ('message', {'message_id': message[0]}, message[1].isoformat() + "-05:00")


@app.route('/forumsearch/<search_string>', methods=('GET', 'POST'))
def forumsearch(search_string):
    unplus_search_string = re.sub(r'\+', ' ', search_string)
    if request.query_string == 'french':
        return sidebar_lang_render('forumsearch', request)
    else:
        return sidebar_lang_render(
            'forumsearch',
            request,
            searchitems=forum_search(unplus_search_string)
        )


@app.route('/search/<search_string>', methods=('GET', 'POST'))
def search(search_string):
    unplus_search_string = re.sub(r'\+', ' ', search_string)
    return sidebar_lang_render(
        'search',
        request,
        searchitems=products_search(unplus_search_string)
    )


@app.route('/locations', methods=('GET', 'POST'))
def locations():
    locations_form = LocationsForm()
    if request.method == 'POST':
        if locations_form.validate():
            try:
                distances = postal_dist(
                    locations_form.postalcode.data,
                    locations_form.measure.data,
                    locations_form.results.data
                )
            except CodeException:
                flash('error', 'Invalid postal code')
                return sidebar_lang_render(
                    'locations',
                    request,
                    locations_form=locations_form
                )
            else:
                us = False
                if len(locations_form.postalcode.data) <= 5:
                    us = True
                if len(distances) is 0:
                    return sidebar_lang_render(
                        'locations',
                        request,
                        locations_form=locations_form,
                        too_far=True,
                        us=us
                    )
                return sidebar_lang_render(
                    'locations',
                    request,
                    locations_form=locations_form,
                    distances=distances,
                    us=us
                )
        else:
            flash_errors(locations_form)
    return sidebar_lang_render(
        'locations',
        request,
        locations_form=locations_form
    )


@app.route('/faq', methods=('GET', 'POST'))
def faq():
    return sidebar_lang_render('faq', request)


@app.route('/contact')
def contact():
    return sidebar_lang_render('contact', request)


@app.route('/marketing')
def marketing():
    return sidebar_lang_render('marketing', request)


@app.route('/about')
def about():
    return sidebar_lang_render('about', request)


@app.route('/gallery')
def gallery():
    return sidebar_lang_render('gallery', request)


@app.route('/color')
@app.route('/colour')
def colour():
    return sidebar_lang_render('colour', request)


@app.route('/aquacolor')
@app.route('/aquacolour')
def aquacolour():
    return sidebar_lang_render('aquacolour', request)


@app.route('/rightstripper')
def rightstripper():
    return sidebar_lang_render('rightstripper', request)


@app.route('/rightfinish')
def rightfinish():
    return sidebar_lang_render('rightfinish', request)


@app.route('/forum/', methods=('GET', 'POST'))
@app.route('/forum/<int:page>', methods=('GET', 'POST'))
def forum(page=1):
    if request.args.get('lang') == 'french':
        message_form = FrenchMessageForm()
    else:
        message_form = MessageForm()
    if message_form.validate_on_submit():
        new_message = Messages(
            message_form.subject.data,
            message_form.name.data,
            message_form.email.data,
            message_form.notifyemail.data,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            message_form.message.data,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        db.session.add(new_message)
        db.session.commit()
        msg = Message()
        msg.sender = "forum@swingpaints.com"
        msg.recipients = ['mchaimberg@swingpaints.com']
        msg.subject = 'Swing Paints Forum Message'
        msg.html = 'Hello Mark,<br />' + \
            message_form.name.data + \
            ' has posted a new message.<br />Click <a href="' + \
            url_for(
                'message',
                message_id=new_message.IDmessage,
                _external=True
            ) + \
            '">here</a> to view the message board.<br />Yours sincerely,\
            <br />Swing Paints'
        mail.send(msg)
        flash('success', 'Success! Your message has been posted to the forum.')
        if request.args.get('lang') == 'french':
            return redirect(url_for(
                'message',
                message_id=new_message.IDmessage,
                lang='french'
            ))
        else:
            return redirect(url_for(
                'message',
                message_id=new_message.IDmessage
            ))
    messages = Messages.query.order_by(
        Messages.last_rdate.desc()
    ).paginate(int(page), 50)
    for message in messages.items:
        message.replies = Replies.query.filter_by(
            IDmessage=message.IDmessage
        ).count()
        message.date = time.strftime(
            '%H:%M %m/%d/%Y',
            time.strptime(str(message.last_rdate), '%Y-%m-%d %H:%M:%S')
        )
    flash_errors(message_form)
    return sidebar_lang_render(
        'forum',
        request,
        messages=messages,
        message_form=message_form
    )


@app.route('/message/<int:message_id>', methods=('GET', 'POST'))
def message(message_id):
    if request.args.get('lang') == 'french':
        message_form = FrenchMessageForm()
    else:
        message_form = MessageForm()
    message = Messages.query.filter_by(IDmessage=message_id).first_or_404()
    if message_form.validate_on_submit():
        last_reply = Replies.query.with_entities(
            Replies.name,
            Replies.email,
            Replies.notifyemail
        ).filter_by(
            IDmessage=message_id
        ).order_by(Replies.rdate.desc()).first()
        if not last_reply:
            last_reply = message
        new_reply = Replies(
            message_id,
            message_form.subject.data,
            message_form.name.data,
            message_form.email.data,
            message_form.notifyemail.data,
            message_form.message.data,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        db.session.add(new_reply)
        db.session.commit()
        db.session.query(Messages).filter_by(
            IDmessage=message_id
        ).update({
            'last_rdate': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })
        msg = Message()
        if last_reply.notifyemail == 'True':
            msg.recipients = [last_reply.email]
        msg.sender = "forum@swingpaints.com"
        msg.bcc = ['mchaimberg@swingpaints.com']
        msg.subject = 'Swing Paints Forum Reply'
        msg.html = 'Hello ' + \
            last_reply.name + \
            ',<br />' + \
            new_reply.name +\
            ' has posted a reply to your message.<br />Click <a href="' + \
            url_for(
                'message',
                message_id=message_id,
                _external=True
            ) + \
            '">here</a> to view the message board.<br />Yours sincerely,<br />\
            Swing Paints'
        mail.send(msg)
        flash('success', 'Success! Your reply has been posted to the forum.')
        return redirect(url_for(
            'message',
            message_id=message_id,
            _anchor=str(
                time.strftime(
                    '%b %d, %Y<br />%H:%M:%S',
                    time.strptime(str(new_reply.rdate), '%Y-%m-%d %H:%M:%S')
                )
            )
        ))
    message.date = time.strftime(
        '%b %d, %Y<br />%H:%M:%S',
        time.strptime(str(message.mdate), '%Y-%m-%d %H:%M:%S')
    )
    replies = Replies.query.filter_by(
        IDmessage=message_id
    ).order_by(Replies.rdate.asc()).all()
    for reply in replies:
        reply.date = time.strftime(
            '%b %d, %Y<br />%H:%M:%S',
            time.strptime(str(reply.rdate), '%Y-%m-%d %H:%M:%S')
        )
    flash_errors(message_form)
    return sidebar_lang_render(
        'message',
        request,
        message=message,
        replies=replies,
        message_form=message_form
    )


@app.route('/refer', methods=('GET', 'POST'))
def refer():
    if request.args.get('lang') == 'french':
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
            msg.subject = "Re: Une recommandation d'un ami - Decouvrez \
                Peintures Swing!"
            msg.html = "%s,<br />S'il vous pla&#xee;t pardonnez l'intrusion, \
                mais je crois que j'ai trouv&#xe9; quelque chose que vous \
                seriez int&#xe9;ress&#xe9;. Je regardais &#xe0; travers les \
                pages du site Web de cette soci&#xe9;t&#xe9; assez cool de \
                finition du bois, Peintures Swing, et la pens&#xe9;e de vous. \
                Donc, c&#x27;est la raison de cette \"presque \" e-mail \
                personnelle. Vous pouvez les trouver \
                <a href='http://www.swingpaints.com/?french'>ici</a>.\
                " % (friendname)
            mail.send(msg)
            return sidebar_lang_render('refersuccess', request)
    else:
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
            msg.subject = "Re: A referral from a friend - Check out Swing \
                Paints!"
            msg.html = "%s,<br />Please forgive the intrusion but I think I \
                found something that you'd be interested in. I was browsing \
                through the pages of the website of this pretty cool wood \
                finishing company, Swing Paints, and thought of you. So, that \
                is the reason for this \"almost\" personal email. You can \
                find them <a href='http://www.swingpaints.com'>here</a>.\
                " % friendname
            mail.send(msg)
            return sidebar_lang_render('refersuccess', request)
    return sidebar_lang_render('refer', request, refer_form=refer_form)


@app.route('/brochure', methods=('GET', 'POST'))
def brochure():
    if request.args.get('lang') == 'french':
        brochure_form = FrenchBrochureForm()
        if brochure_form.validate_on_submit():
            brochure = Brochures(
                brochure_form.name.data,
                brochure_form.email.data,
                brochure_form.address.data,
                brochure_form.city.data,
                brochure_form.stateprov.data,
                brochure_form.zipcode.data,
                brochure_form.country.data,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'False'
            )
            db.session.add(brochure)
            db.session.commit()
            msg = Message()
            msg.recipients = ['echaimberg@swingpaints.com']
            msg.subject = "%s would like a free brochure!" % (
                brochure_form.name.data
            )
            msg.html = "name:&nbsp;%s<br />email:&nbsp;%s<br />address:&nbsp;\
                %s<br />city:&nbsp;%s<br />stateprov:&nbsp;%s<br />zipcode:\
                &nbsp;%s<br />country:&nbsp;%s<br />lang:&nbsp;en" % (
                brochure_form.name.data,
                brochure_form.email.data,
                brochure_form.address.data,
                brochure_form.city.data,
                brochure_form.stateprov.data,
                brochure_form.zipcode.data,
                brochure_form.country.data
            )
            mail.send(msg)
            return sidebar_lang_render('brochuresuccess', request)
    else:
        brochure_form = BrochureForm()
        if brochure_form.validate_on_submit():
            brochure = Brochures(
                brochure_form.name.data,
                brochure_form.email.data,
                brochure_form.address.data,
                brochure_form.city.data,
                brochure_form.stateprov.data,
                brochure_form.zipcode.data,
                brochure_form.country.data,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'True'
            )
            db.session.add(brochure)
            db.session.commit()
            msg = Message()
            msg.recipients = ['echaimberg@swingpaints.com']
            msg.subject = "%s would like a free brochure!" % (
                brochure_form.name.data
            )
            msg.html = "name:&nbsp;%s<br />email:&nbsp;%s<br />address:&nbsp;\
                %s<br />city:&nbsp;%s<br />stateprov:&nbsp;%s<br />zipcode:\
                &nbsp;%s<br />country:&nbsp;%s<br />lang:&nbsp;en" % (
                brochure_form.name.data,
                brochure_form.email.data,
                brochure_form.address.data,
                brochure_form.city.data,
                brochure_form.stateprov.data,
                brochure_form.zipcode.data,
                brochure_form.country.data
            )
            mail.send(msg)
            return sidebar_lang_render('brochuresuccess', request)
    return sidebar_lang_render(
        'brochure',
        request,
        brochure_form=brochure_form
    )


@app.route('/product/<regex("\d+\/.*"):regid>')
def product_string(regid):
    productid = int(re.sub(r'(\d+)\/.*', r'\1', regid))
    stringid = re.sub(r'\d+\/(\w+)', r'\1', regid)
    if request.args.get('lang') == 'french':
        product = Frenchproducts.query.filter_by(id=productid).first_or_404()
        subbed_title = product_title_sub(product.title)
        if not stringid == subbed_title:
            return redirect(url_for(
                'product_string',
                regid=''.join([
                    str(productid),
                    '/',
                    subbed_title
                ]),
                lang='french'
            ), code=301)
        product.infolist = Infolist.query.with_entities(
            Infolist.infolistfr
        ).filter_by(
            productid=productid
        ).order_by(Infolist.id.asc()).all()
        product.infotable = Infotable.query.with_entities(
            Infotable.sizefr,
            Infotable.quantityfr
        ).filter_by(
            productid=productid
        ).order_by(Infotable.id.asc()).all()
        try:
            category = Frenchcategories.query.filter_by(
                category=product.category
            ).first().name
        except AttributeError:
            category = ''
    else:
        product = Products.query.filter_by(id=productid).first_or_404()
        subbed_title = re.sub(r'(?:<br>|\s)', '-', product.title)
        m = re.search(r'&#x\d+;', subbed_title)
        while m is not None:
            subbed_title = subbed_title[:m.start()] + \
                unichr(int(subbed_title[m.start()+3:m.end()-1], 16)) + \
                subbed_title[m.end():]
            m = re.search(r'&#x\d+;', subbed_title)
        if not stringid == subbed_title:
            return redirect(url_for(
                'product_string',
                regid=''.join([
                    str(productid),
                    '/',
                    subbed_title
                ])
            ), code=301)
        product.infolist = Infolist.query.with_entities(
            Infolist.infolist
        ).filter_by(
            productid=productid
        ).order_by(Infolist.id.asc()).all()
        product.infotable = Infotable.query.with_entities(
            Infotable.size,
            Infotable.quantity
        ).filter_by(
            productid=productid
        ).order_by(Infotable.id.asc()).all()
        try:
            category = Categories.query.filter_by(
                category=product.category
            ).first().name
        except AttributeError:
            category = ''
    return sidebar_lang_render(
        'product',
        request,
        product=product,
        category=category
    )


@app.route('/product/<productid>')
def product(productid):
    if request.args.get('lang') == 'french':
        return redirect(url_for(
            'product_string',
            regid=''.join([productid, '/']),
            lang='french'
        ), code=301)
    return redirect(url_for(
        'product_string',
        regid=''.join([productid, '/'])
    ), code=301)


@app.route('/category/<string:categoryid>')
def category(categoryid):
    if request.args.get('lang') == 'french':
        category = Frenchcategories.query.filter_by(
            category=categoryid
        ).first_or_404()
        category.products = Frenchproducts.query.with_entities(
            Frenchproducts.id,
            Frenchproducts.title,
            Frenchproducts.text
        ).filter(
            Frenchproducts.category.like('%'+categoryid+'%')
        ).order_by(Frenchproducts.id.asc()).all()
        category.dictlen = len(category.products)
    else:
        category = Categories.query.filter_by(
            category=categoryid
        ).first_or_404()
        category.products = Products.query.with_entities(
            Products.id,
            Products.title,
            Products.text
        ).filter(
            Products.category.like('%'+categoryid+'%')
        ).order_by(Products.id.asc()).all()
        category.dictlen = len(category.products)
    return sidebar_lang_render('category', request, category=category)


@app.route('/brand/<string:brandid>')
def brand(brandid):
    if request.args.get('lang') == 'french':
        brand = Brands.query.filter_by(brand=brandid).first_or_404()
        brand.products = Frenchproducts.query.with_entities(
            Frenchproducts.id,
            Frenchproducts.title,
            Frenchproducts.text
        ).filter(
            Frenchproducts.brand.like('%'+brandid+'%')
        ).order_by(Frenchproducts.id.asc()).all()
        brand.dictlen = len(brand.products)
    else:
        brand = Brands.query.filter_by(brand=brandid).first_or_404()
        brand.products = Products.query.with_entities(
            Products.id,
            Products.title,
            Products.text
        ).filter(
            Products.brand.like('%'+brandid+'%')
        ).order_by(Products.id.asc()).all()
        brand.dictlen = len(brand.products)
    return sidebar_lang_render('category', request, category=brand)


if __name__ == '__main__':
    app.run()
