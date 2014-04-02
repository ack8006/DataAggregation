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
from xml.dom import minidom
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
	#kwargs['fileType'] = 'JSON'
	url = fred.observations(**kwargs)
	#jsonParser(url)
	xmlObservationsParser(url)

def jsonParser(url):

	response = urllib2.urlopen(url)
	data = json.load(response)
	print data

	observationArray = []

#https://docs.python.org/2/library/xml.dom.minidom.html
def xmlObservationsParser(url):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	observationList = xmldoc.getElementsByTagName('observation')
	print len(observationList)
	observationDict = {}
	for x in observationList:
		print x.attributes['date'].value
		print x.attributes['value'].value
		print ''
		observationDict[x.attributes['date']] = x.attributes['value'].value


def addToDatabase()
	pass



if __name__ == "__main__":
	main()