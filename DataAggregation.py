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
import MySQLdb
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

	#TEST SERIES DESCRIPTION
	url = fred.series(**kwargs)
	xmlSeriesParser(url)


	#TEST OBSERVATIONS
	url = fred.observations(**kwargs)
	#jsonParser(url)
	
	#***xmlObservationsParser(url, kwargs['series'])

def jsonParser(url):

	response = urllib2.urlopen(url)
	data = json.load(response)
	print data

	observationArray = []

#https://docs.python.org/2/library/xml.dom.minidom.html
def xmlObservationsParser(url, series):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	observationList = xmldoc.getElementsByTagName('observation')
	print len(observationList)
	observationDict = {}
	for x in observationList:
		#print x.attributes['date'].value
		#print x.attributes['value'].value
		#print ''
		observationDict[x.attributes['date'].value] = x.attributes['value'].value

def xmlSeriesParser(url):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	seriesList = xmldoc.getElementsByTagName('series')
	seriesDict = {}
	for x in seriesList:
		seriesDict['id'] = x.attributes['id'].value
		seriesDict['title'] = x.attributes['title'].value
		#seriesDict['frequency'] = x.attributes['frequency'].value
		seriesDict['frequency_short'] = x.attributes['frequency_short'].value
		seriesDict['units'] = x.attributes['units'].value
		#seriesDict['seasonal_adjustment'] = x.attributes['seasonal_adjustment'].value
		#seriesDict['seasonal_adjustment_short'] = x.attributes['seasonal_adjustment_short'].value
		#seriesDict['last_updated'] = x.attributes['last_updated'].value
		#seriesDict['observation_start'] = x.attributes['observation_start'].value
	addSeriesToDatabase(seriesDict)

def addSeriesToDatabase(seriesDict):
	db = MySQLdb.connect(host="localhost", user="root", passwd="Optima1!", db="EconomicIndicators")
	
	cursor = db.cursor() 
	cursor.execute("SELECT 1 FROM fredindicators WHERE FREDID = \"%s\"" %(seriesDict['id']))
	if len(cursor.fetchall()) >= 1:
		print "yes"
	if len(cursor.fetchall()) <= 0:
		print "no"



	#cursor.execute("SELECT * FROM fredindicators")
	#for row in cursor.fetchall():
	#	print row[0]
		




#FREDIndicators
#FREDID  VarChar(16)
#IndicatorName  VarChar(45)
#Reporting Period  VarChar(1)
#Description  VarChar(45)
#Scale  VarChar(45)

#FredValues
#ValueID  int
#FREDID  VarChar(16)
#RealTimeStart  Date 
#RealTimeEnd  Date 
#Date   DATE 
#Value  Decimal(18,4)




if __name__ == "__main__":
	main()