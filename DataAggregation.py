#downloads data from APIs
#Organizes data 
#stores data into a database
#this is a one time use to download and fully populate the database
#there will be a separate cron job to consistently update the database

#must be careful on how returned data is interpreted.  PAYEMS for example returns
# in the total number of jobs in the US, not the change which is what is commonly
# seen

#http://api.stlouisfed.org/fred/series/observations?series_id=PAYEMS
#&observation_start=2013-03-01&observation_end=2013-03-01
#&realtime_start=2013-04-05&realtime_end=2013-04-05
#&units=chg&api_key=xxxxxxxxxxxxxxxxx

import json
import urllib2
#not currently using
#import fred
from FREDRequests import *


def main():
	#fred.key("dbbac155dc1543184204ed045632071e")
	#print fred.api_key
	test()

def test(**kwargs):
	#print fred.observations('PAYEMS')
	fred = FredRequests()
	kwargs['series'] = "PAYEMS"
	fred.observations(**kwargs)


def jsonParser(url):
	#r = urllib2.urlopen(url)
	#data = json.loads(r)
	#print data
	print url




if __name__ == "__main__":
	main()