from HTMLParser import HTMLParser
import re

#Throw back fields from the about page
class InfoScout(HTMLParser):

	collectData = False
	linkData = False
	divData = False

	dataBuffer = ""

	infoData = []	

	def handle_starttag(self,tag,attrs):
		if tag=='div':
			for values in attrs:
				if values[0] == 'class' and values[1] =='mfsm':
						self.collectData = True
						self.divData = True

		if tag=='a':
			self.linkData = True

	def handle_endtag(self,tag):
		if tag=='div':
			self.collectData = False
			self.divData = False
			self.dataBuffer = ""

		if tag=='a':
			self.linkData = False

	def handle_data(self, data):
	
		if self.collectData and data != 'Search':
			self.infoData.append(data)
