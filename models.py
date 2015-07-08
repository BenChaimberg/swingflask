from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Infotable(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Text(convert_unicode=True), nullable=False)
    quantity = db.Column(db.Text(convert_unicode=True), nullable=False)

    def __init__(self, productid, size, quantity):
        self.productid = productid
        self.size = size
        self.quantity = quantity


class Infolist(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    infolist = db.Column(db.Text(convert_unicode=True), nullable=True)

    def __init__(self, productid, infolist):
        self.productid = productid
        self.infolist = infolist


class Categories(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    category = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, category, name):
        self.category = category
        self.name = name


class Brands(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    brand = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, brand, name):
        self.brand = brand
        self.name = name


class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    demo = db.Column(db.String(250), nullable=True)
    text = db.Column(db.Text(), nullable=False)
    directions = db.Column(db.Text(), nullable=True)
    forms_us = db.Column(db.Text(), nullable=True)
    forms_can = db.Column(db.Text(), nullable=True)
    category = db.Column(db.Text(), nullable=False)
    brand = db.Column(db.Text(), nullable=True)

    def __init__(
        self,
        id,
        title,
        demo,
        text,
        directions,
        forms_us,
        forms_can,
        category,
        brand
    ):
        self.id = id
        self.title = title
        self.demo = demo
        self.text = text
        self.directions = directions
        self.forms_us = forms_us
        self.forms_can = forms_can
        self.category = category
        self.brand = brand


class Frenchinfotable(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Text(convert_unicode=True), nullable=False)
    quantity = db.Column(db.Text(convert_unicode=True), nullable=False)

    def __init__(self, productid, size, quantity):
        self.productid = productid
        self.size = size
        self.quantity = quantity


class Frenchinfolist(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    productid = db.Column(db.Integer(), nullable=False)
    infolist = db.Column(db.Text(convert_unicode=True), nullable=True)

    def __init__(self, productid, infolist):
        self.productid = productid
        self.infolist = infolist


class Frenchcategories(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    category = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, category, name):
        self.category = category
        self.name = name


class Frenchproducts(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    demo = db.Column(db.String(250), nullable=True)
    text = db.Column(db.Text(), nullable=False)
    directions = db.Column(db.Text(), nullable=True)
    forms_us = db.Column(db.Text(), nullable=True)
    forms_can = db.Column(db.Text(), nullable=True)
    category = db.Column(db.Text(), nullable=False)
    brand = db.Column(db.Text(), nullable=False)

    def __init__(
        self,
        id,
        title,
        demo,
        text,
        directions,
        forms_us,
        forms_can,
        category,
        brand
    ):
        self.id = id
        self.title = title
        self.demo = demo
        self.text = text
        self.directions = directions
        self.forms_us = forms_us
        self.forms_can = forms_can
        self.category = category
        self.brand = brand


class Messages(db.Model):
    IDmessage = db.Column(db.Integer(), primary_key=True, nullable=False)
    subject = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    notifyemail = db.Column(db.Enum('True', 'False'), nullable=True)
    mdate = db.Column(db.DateTime(), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    last_rdate = db.Column(db.DateTime(), nullable=True)

    def __init__(
        self,
        subject,
        name,
        email,
        notifyemail,
        mdate,
        message,
        last_rdate
    ):
        self.subject = subject
        self.name = name
        self.email = email
        self.notifyemail = notifyemail
        self.mdate = mdate
        self.message = message
        self.last_rdate = last_rdate


class Replies(db.Model):
    IDreply = db.Column(db.Integer(), primary_key=True, nullable=False)
    IDmessage = db.Column(db.Integer(), nullable=True)
    subject = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    notifyemail = db.Column(db.Enum('True', 'False'), nullable=True)
    message = db.Column(db.Text(), nullable=True)
    rdate = db.Column(db.DateTime(), nullable=True)

    def __init__(
        self,
        IDmessage,
        subject,
        name,
        email,
        notifyemail,
        message,
        rdate
    ):
        self.IDmessage = IDmessage
        self.subject = subject
        self.name = name
        self.email = email
        self.notifyemail = notifyemail
        self.message = message
        self.rdate = rdate


class Brochures(db.Model):
    idbrochure = db.Column(db.Integer(), primary_key=True, nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    province = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    xdate = db.Column(db.DateTime(), nullable=True)
    language = db.Column(db.Enum('True', 'False'), nullable=True)

    def __init__(
        self,
        contact,
        email,
        address,
        city,
        province,
        postal_code,
        country,
        xdate,
        language
    ):
        self.contact = contact
        self.email = email
        self.address = address
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.country = country
        self.xdate = xdate
        self.language = language
