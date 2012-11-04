#!/usr/bin/python

import sys
from fscout import *

scout = FScout()

if len(sys.argv) < 3:
	print "Usage: <username> <password> <target>"
else:

	scout.login(sys.argv[1],sys.argv[2],sys.argv[3])

	print "~LOCATION~"
	print scout.profile.locationData
	print "~FRIENDS~"
	print scout.friends()
	print "~LIKES~"
	print scout.likes()
	print "~INFO~"
	print scout.info()
	print "~TIMELINE~"
	print scout.timeline()
