#!/usr/bin/python

#############################################################
#
#	FScout -- Facebook Data Parser				
#			                                                  
#	@Copyleft : All wrongs reserved.
#		Morgan Phillips					     
#		winter2718@gmail.com                                   
#                                                                      
#############################################################

import cookielib
import os
import sys
import urllib
import urllib2
import re

from sparce import parser

class LoginError(Exception):

    def __init__(self):
	
	print "Must log in before attempting to pull data."

class TimelineError(Exception):

    def __init__(self):	
	print "Login failed or the account you've logged into doesn't have mobile timeline enabled."	
	print "Make sure you escape special characters in your input (i.e. \!\@) and check to see that links like 'm.facebook.com/target?v=friends are working."

class FScout:
    

    def __init__(self):

	self.loggedIn = False

        self.cookie = cookielib.MozillaCookieJar('scoutcookie')
        if os.access('scoutcookie', os.F_OK):
            self.cookie.load()
            
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel = 0),
            urllib2.HTTPSHandler(debuglevel = 0),
            urllib2.HTTPCookieProcessor(self.cookie)
        )
        self.opener.addheaders = [('User-agent', ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'))]

    #Just a "do while" type loop for the LinkScout parser class which returns a list
    def scoutLoop(self,url,sObject):
        
	tempList = []	

	while url != None:
		response = self.opener.open(url)

		sObject.feed(response.read())
		tempList = tempList+sObject.rList
		
		if url == sObject.rMore:
			url = None
		else:
			url = sObject.rMore

	return tempList


    def login(self,login,password,target):

	self.target = target	

	#see if we have a url or an id and react accordingly
	match = re.search('.*\?.*',self.target)
	if match != None:
		self.target = self.target+'&'
	else:
		self.target = self.target+'?'
	
	loginPage = self.opener.open("http://m.facebook.com/login.php")
	
	LoginBuilder = parser.FormCapture()
	LoginBuilder.feed(loginPage.read())
	
	LoginBuilder.hiddenFields['email']=login
	LoginBuilder.hiddenFields['pass']=password
	self.opener.open("https://m.facebook.com/login.php",urllib.urlencode(LoginBuilder.hiddenFields))
	
	response = self.opener.open("http://m.facebook.com/"+self.target)
	self.profile = parser.ProfileScout()
	self.profile.feed(response.read())

	self.locationData = self.profile.locationData
	
	self.loggedIn = True

	if self.profile.timelineProfile == False:
		raise TimelineError
	
    def friends(self):

        if self.loggedIn:
            friends = []
            if(self.profile.publicFriends):
                    friends = self.scoutLoop('http://m.facebook.com/'+self.target+'v=friends',parser.LinkScout('/(.*)\?fref=.*','.*\?.*&startindex=.*'))
		    return friends
        else:
            raise LoginError

    def likes(self):

        if self.loggedIn:
            likes = []
            if(self.profile.publicLikes):
                likes = self.scoutLoop('http://m.facebook.com/'+self.target+'v=likes',parser.LikeScout('/(.*)\?fref=.*','.*\?.*&startindex=.*'))
                return likes
        else:
            raise LoginError

    def timeline(self):

        timeline = []
        for link in self.profile.timelineLinks:
                response = self.opener.open('http://m.facebook.com/'+self.target+link)
                sScout = parser.StoryScout()
                sScout.feed(response.read())
                timeline = timeline+sScout.rStories
        timeline = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in timeline)]
        return timeline

    def info(self):

	info = []
        if(self.profile.publicAbout):
                response = self.opener.open('http://m.facebook.com/'+self.target+'v=info')
                about = parser.InfoScout()
                #this rhymes :p
                about.feed(response.read())
		return about.infoData
        else:
                raise LoginError

