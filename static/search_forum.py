from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import update, or_
import inspect

def line_no():
    return inspect.currentframe().f_back.f_lineno

app = Flask(__name__) #created app as instance of Flask
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://swingpaint305734:103569@sql.megasqlservers.com:3306/circa1850_swingpaints_com?charset=latin1'
db = SQLAlchemy(app)

class Messages(db.Model):
    IDmessage = db.Column(db.Integer(), primary_key=True, nullable=False)
    subject = db.Column(db.String(250),nullable=True)
    name = db.Column(db.String(250),nullable=True)
    email = db.Column(db.String(250),nullable=True)
    notifyemail = db.Column(db.Enum('True','False'),nullable=True)
    mdate = db.Column(db.DateTime(),nullable=True)
    message = db.Column(db.Text(),nullable=True)
    last_rdate = db.Column(db.DateTime(),nullable=True)

    def __init__(self, subject, name, email, notifyemail, mdate, message, last_rdate):
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
    subject = db.Column(db.String(250),nullable=True)
    name = db.Column(db.String(250),nullable=True)
    email = db.Column(db.String(250),nullable=True)
    notifyemail = db.Column(db.Enum('True','False'),nullable=True)
    message = db.Column(db.Text(),nullable=True)
    rdate = db.Column(db.DateTime(),nullable=True)

    def __init__(self, IDmessage, subject, name, email, notifyemail, message, rdate):
        self.IDmessage = IDmessage
        self.subject = subject
        self.name = name
        self.email = email
        self.notifyemail = notifyemail
        self.message = message
        self.rdate = rdate

class SearchError(Exception):
	def __init__(self):
		pass

def forum_search(search_string):
	try:
		search_string = search_string.lower()
		search_items = []
		found_index = -1
		html_index = 0
		html = ''
		found_titles = []
		found_sites = []
		messages = []
		replies = []
		while True:
			try_index = found_index+1
			found_index = search_string.find(' ',try_index)
			if not found_index < 0:
				search_items.append(search_string[:found_index])
				search_string = search_string[found_index:]
			else:
				search_items.append(search_string)
				break
		for search_item in search_items:
			for reply in Replies.query.filter(Replies.message.like('%'+search_item+'%')).all():
				if not Messages.query.filter(Messages.IDmessage == reply.IDmessage).first() in messages:
					message = Messages.query.filter(Messages.IDmessage == reply.IDmessage).first()
					messages.append(message)
			messages_temp = Messages.query.filter(Messages.message.like('%'+search_item+'%')).all()
			for message in messages_temp:
				if not message in messages:
					messages.append(message)
			for message in messages:
				replies_temp = Replies.query.filter(Replies.message.like('%'+search_item+'%')).filter(Replies.IDmessage == message.IDmessage).all()
				for reply in replies_temp:
 					replies.append(reply)
		for message in messages:
			found_site = [message,[]]
			found_sites.append(found_site)
			for search_item in search_items:
				found_index = -1
				while True:
					try_index = found_index+1
					found_index = message.message.lower().find(search_string,try_index)
					if not found_index < 0:
						space_index = len(message.message)-found_index
						space_index2 = found_index
						for i in range(0,3):
							space_index = message.message[::-1].find(' ',space_index+1)
						if space_index < 0:
							space_index = len(message.message)
						for i in range(0,4):
							if message.message.find(' ',space_index2+1) > 0:
								space_index2 = message.message.find(' ',space_index2+1)
						found_sites[-1][1].append(message.message[len(message.message)-space_index:found_index]+'<b>'+message.message[found_index:found_index+len(search_item)]+'</b>'+message.message[found_index+len(search_item):space_index2])
					else:
						for reply in replies:
							if not reply.IDmessage == message.IDmessage:
								continue
							found_index = -1
							while True:
								try_index = found_index+1
								found_index = reply.message.lower().find(search_string,try_index)
								if not found_index < 0:
									space_index = len(reply.message)-found_index
									space_index2 = found_index
									for i in range(0,3):
										space_index = reply.message[::-1].find(' ',space_index+1)
									if space_index < 0:
										space_index = len(reply.message)
									for i in range(0,4):
										if reply.message.find(' ',space_index2+1) > 0:
											space_index2 = reply.message.find(' ',space_index2+1)
									found_sites[-1][1].append(reply.message[len(reply.message)-space_index:found_index]+'<b>'+reply.message[found_index:found_index+len(search_item)]+'</b>'+reply.message[found_index+len(search_item):space_index2])
								else:
									break
						break
				found_index = -1
			found_sites[-1][1].sort()
			if found_sites[-1][1] == []:
				found_sites.pop()
		if not found_sites == []:
			found_sorted = [found_sites.pop()]
		else: raise SearchError
		for found_site in found_sites:
			for sorted in found_sorted:
				if len(sorted[1]) < len(found_site[1]):
					found_sorted.insert(found_sorted.index(sorted),found_site)
					break
				if found_sorted.index(sorted) == len(found_sorted) - 1:
					found_sorted.append(found_site)
					break
		html += '<ul>'
		for final in found_sorted:
			html += '<li><h2><a href="/message/' + str(final[0].IDmessage) + '">' + final[0].subject + '</a></h2>'
			for text in final[1]:
				html += text + '&hellip;'
			html += '</li>'
		html += '</ul>'
	except SearchError:
		html = 'There were no pages that matched your search.'
	return html
