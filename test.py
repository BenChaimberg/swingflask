from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import urllib2
from urllib2 import Request, urlopen, URLError
from static import frenchproducttitle

for x in frenchproducttitle.title:
    req = Request('http://www.swingpaints.com/french/'  + str(x) + '.htm')
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server. Reason: ', e.reason
        elif hasattr(e, 'code'):
            print '\''+x+'\':\'\'\'404\'\'\','
    else:
        html = response.read()
        html = html.decode('latin-1')
    
        class MyHTMLParser(HTMLParser):
        	def __init__(self):
        		HTMLParser.__init__(self)
        		self.recording = False
        		self.datalist = []
        	def handle_starttag(self, tag, attrs):
        		if tag == 'p':
        			self.recording = True
        	def handle_endtag(self, tag):
        		if tag == 'p':
        			self.recording = False
        	def handle_data(self, data):
        		if self.recording == True:
        			self.datalist.append(data)
        	def handle_entityref(self, name):
        		c = unichr(name2codepoint[name])
        		if self.recording == True:
        			self.datalist.append('&'+name+';')
        	
    		def handle_charref(self, name):
        		if name.startswith('x'):
        		    c = int(name[1:], 16)
        		else:
        		    c = int(name)
        		if self.recording == True:
        			self.datalist.append(c)
        
        parser = MyHTMLParser()
        parser.feed(html)
        wholedata = ''
        for datum in parser.datalist:
        	wholedata += datum
        print '\''+x+'\':\'\'\''+wholedata+'\'\'\','