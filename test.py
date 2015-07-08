from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from urllib2 import Request, urlopen, URLError
from models import db, Products

for x in Products.query.all():
    req = Request('http://www.swingpaints.com/' + str(x.id) + 'can.htm')
    try:
        response = urlopen(req)
    except URLError:
        pass
    else:
        html = response.read()
        html = html.decode('latin-1')

        class MyHTMLParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.recording = False
                self.datalist = []
                self.start = 0
                self.end = 0

            def handle_starttag(self, tag, attrs):
                if tag == 'select':
                    self.recording = True
                if tag == 'option':
                    self.datalist.append('<option ')
                    for attr in attrs:
                        self.datalist.append(
                            str(attr[0])+'="'+str(attr[1])+'"'
                        )
                    self.datalist.append('>')

            def handle_endtag(self, tag):
                if tag == 'select':
                    self.recording = False
                if tag == 'option':
                    self.datalist.append('</option>')

            def handle_data(self, data):
                if self.recording is True:
                    self.datalist.append(data)

            def handle_entityref(self, name):
                c = unichr(name2codepoint[name])
                if self.recording is True:
                    self.datalist.append('&'+c+';')

            def handle_charref(self, name):
                if name.startswith('x'):
                    c = int(name[1:], 16)
                else:
                    c = int(name)
                if self.recording is True:
                    self.datalist.append(c)
        parser = MyHTMLParser()
        parser.feed(html)
        wholedata = ''
        for datum in parser.datalist:
            wholedata += datum
        if x.forms_can == '':
            print 'blank'
            print wholedata
db.session.commit()
