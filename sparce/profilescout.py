from HTMLParser import HTMLParser
import re

#collects all the links we'll want to parse from the profil's home page
class ProfileScout(HTMLParser):
	
	timelineLinks = []
	locationData = []

	publicFriends = False
	publicLikes = False
	publicAbout = False
	publicPhotos = False
	publicFeed = False
	timelineProfile = False

	profileType = 0
	urls = {}

	lSwitch=False
	
	def handle_starttag(self, tag, attrs):
		for values in attrs:
				if values[0] == 'href':
					match = re.search('.*\?(tm=.*)',values[1])
					if match != None:
						self.timelineProfile = True
						self.timelineLinks.append(match.group(1))

					match = re.search('.*(v=friends).*',values[1])
					if match != None:
						self.publicFriends = True
						self.urls['friends']=match.group(1)

					match = re.search('.*v=likes.*',values[1])
					if match != None:

						self.publicLikes = True
					match = re.search('.*v=photos.*',values[1])
					if match != None:

						self.publicPhotos = True

					match = re.search('.*v=info.*',values[1])
					if match != None:
						self.publicAbout = True

	
	def handle_data(self, data):
		
		if self.lSwitch == True:
			self.locationData.append(data)
			self.lSwitch = False
		
		match = re.search('.*Lives in.*',data)
		if match != None:
    			self.lSwitch = True
		match = re.search('.*From.*',data)
		if match != None:
			self.lSwitch = True


