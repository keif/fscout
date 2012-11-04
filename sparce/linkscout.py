from HTMLParser import HTMLParser
import re

#Just runs regular expressions against 'hrefs'
class LinkScout(HTMLParser):

	def __init__(self,listExp,moreExp):	
		
		HTMLParser.__init__(self)	
		
		self.listExp = listExp
		self.moreExp = moreExp
		
		self.rList = []
		self.rMore = None


	def handle_starttag(self, tag, attrs):
		for values in attrs:
			if values[0] == 'href':
				match = re.search(self.listExp,values[1])
				if match != None:
					self.rList.append(match.group(1))
				match = re.search(self.moreExp,values[1])
				if match != None:
					self.rMore = "http://m.facebook.com"+match.group()
					

