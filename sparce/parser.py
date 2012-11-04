from HTMLParser import HTMLParser
import re

from profilescout import *
from storyscout import *
from infoscout import *
from linkscout import *
from likescout import *


#This gives us our randomly generated 'hidden' values in the login form
class FormCapture(HTMLParser):

	tDict = {}
	hiddenFields = {}

	def handle_starttag(self, tag, attrs):
		if tag=="input":
			for values in attrs:
				try:
					self.tDict[values[0]] = values[1]
				except(LookupError):
					raise
				
		try:
			if self.tDict['type']=='hidden':
				self.hiddenFields[self.tDict['name']]=self.tDict['value']

		except:
			pass


	
