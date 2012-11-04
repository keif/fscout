from HTMLParser import HTMLParser
import re

from linkscout import *

#'like' links don't always have regular text in the link attributes
class LikeScout(LinkScout):

	def __init__(self,listExp,moreExp):
		
		LinkScout.__init__(self,listExp,moreExp)
		self.rListLength = len(self.rList)

	def handle_data(self, data):
		if self.rListLength < len(self.rList):
			dL = {self.rList[len(self.rList)-1]:data}
			self.rList.pop()
			self.rList.append(dL)
			self.rListLength = len(self.rList)


