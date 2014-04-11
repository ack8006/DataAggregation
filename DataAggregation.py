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



def main(**kwargs):
	#fred.key("dbbac155dc1543184204ed045632071e")
	#print fred.api_key
	
	#seriesUpload()


def seriesUpload(**kwargs):
	#print fred.observations('PAYEMS')
	fred = FredRequests()
	
	#tagList = ['VIXCLS','VXVCLS','VXNCLS','GVZCLS','OVXCLS','VXEEMCLS','RVXCLS','VXDCLS','VXSLVCLS','VXXLECLS']

	for x in tagList:
		kwargs['series'] = x		
		#kwargs['fileType'] = 'JSON'
		#TEST SERIES DESCRIPTION
		url = fred.series(**kwargs)
		xmlSeriesParseAndLoad(url)

def xmlCategoryParser(url, a):
	try:
		xmldoc = minidom.parse(urllib2.urlopen(url))
		categoryList = xmldoc.getElementsByTagName('category')
		for x in categoryList:
			print 
			print str(a) + x.attributes['name'].value
	except urllib2.HTTPError, err:
		if err.code == 400:
			pass
		else:
			raise

def xmlObservationsParser(url, series):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	observationList = xmldoc.getElementsByTagName('observation')
	print len(observationList)
	observationDict = {}
	
		#print x.attributes['date'].value
		#print x.attributes['value'].value
		#print ''
	observationDict[x.attributes['date'].value] = x.attributes['value'].value

def xmlSeriesParseAndLoad(url):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	seriesList = xmldoc.getElementsByTagName('series')

	db = MySQLdb.connect(host="localhost", user="root", passwd="Optima1!", db="EconomicIndicators")

		#seriesDict['id'] = x.attributes['id'].value
		#seriesDict['title'] = x.attributes['title'].value
		#seriesDict['frequency'] = x.attributes['frequency'].value
		#seriesDict['frequency_short'] = x.attributes['frequency_short'].value
		#seriesDict['units'] = x.attributes['units'].value
		#seriesDict['seasonal_adjustment'] = x.attributes['seasonal_adjustment'].value
		#seriesDict['seasonal_adjustment_short'] = x.attributes['seasonal_adjustment_short'].value
		#seriesDict['last_updated'] = x.attributes['last_updated'].value
		#seriesDict['observation_start'] = x.attributes['observation_start'].value
	
	cursor = db.cursor() 
	for x in seriesList:
		cursor.execute("SELECT 1 FROM fredindicators WHERE FREDID = \"%s\"" %(x.attributes['id'].value))
		if len(cursor.fetchall()) <= 0:
			print x.attributes['id'].value
			cursor.execute("INSERT INTO fredindicators (FREDID, Title, Frequency, SeasonalAdjustment, Units, Region, Category) VALUES ('%s', '%s', '%s', '%s','%s','%s','%s')" % (x.attributes['id'].value.replace("'","''"), x.attributes['title'].value.replace("'","''"), x.attributes['frequency_short'].value, x.attributes['seasonal_adjustment_short'].value, x.attributes['units'].value.replace("'","''"), "Global", "Volatility"))
			db.commit()
			print "uploaded: " + x.attributes['id'].value

	db.close()










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