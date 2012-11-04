from HTMLParser import HTMLParser
import re

#This is skipping image links for the moment....
class StoryScout(HTMLParser):

	rStories = []
	rStory = {}
	currentTag = ''

	collectData = False

	def handle_starttag(self,tag,attrs):
		
		if tag == 'div':
			for values in attrs:
				if values[0] == 'class':
					match = re.search('.*tlUnit.*',values[1])
					if match != None:
						if self.rStory:
							self.rStories.append(self.rStory)
							self.rStory = {}
							self.currentTag = ''
		if tag == 'abbr':
			self.collectData=True
			self.currentTag = 'date'
		if tag == 'span':
			for values in attrs:
				if values[0] == 'class':
					match = re.search('.*tlActorText.*',values[1])
					if match != None:
						self.collectData = True
						self.currentTag = 'tlActorText'
					match = re.search('.*tlName.tlActor.*',values[1])
					if match != None:
						self.collectData = True
						self.currentTag = 'tlActor'
					match = re.search('.*word_break.*',values[1])
					if match != None:
						self.collectData = True
						self.currentTag = 'tlActorText'

	def handle_data(self, data):
		tDict = {}
		if self.collectData:
			try:
				if self.currentTag == 'tlActorText' and self.rStory['tlActorText']:
					self.rStory['tlActorText'] = self.rStory['tlActorText']+self.unescape(data)
				else:
					tDict = {self.currentTag:self.unescape(data)}
					self.rStory.update(tDict)
					self.collectData = False
			except:

				tDict = {self.currentTag:self.unescape(data)}
				self.rStory.update(tDict)
				self.collectData = False

		if data == 'near':
			self.collectData = True
			self.currentTag = 'near'
		
	def handle_endtag(self,tag):
		if tag=='html':
			if self.rStory:
				self.rStories.append(self.rStory)



