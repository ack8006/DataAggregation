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
	
	#initialSeriesUpload()
	initialCategorySeriesUpload()

def initialSeriesUpload(**kwargs):
	#print fred.observations('PAYEMS')
	fred = FredRequests()
	
	#tagList = ['VIXCLS','VXVCLS','VXNCLS','GVZCLS','OVXCLS','VXEEMCLS','RVXCLS','VXDCLS','VXSLVCLS','VXXLECLS']

	for x in tagList:
		kwargs['id'] = x		
		#kwargs['fileType'] = 'JSON'
		#TEST SERIES DESCRIPTION
		url = fred.series(**kwargs)
		xmlSeriesParseAndLoad(url)

def initialCategorySeriesUpload(**kwargs):
	fred = FredRequests()
	categoryList = [1]
	#gets name of category then adds all series within that category
	for x in categoryList:
		#sets category id
		kwargs['id'] = str(x)
		#gets the url with fred.category then calls categoryparser which returns the cat name
		categoryName = xmlCategoryParser(fred.category(**kwargs))
		if categoryName:
			xmlSeriesParseAndLoad(fred.categorySeries(**kwargs), categoryName)

#parses category information and returns the category name
def xmlCategoryParser(url):
	try:
		xmldoc = minidom.parse(urllib2.urlopen(url))
		categoryList = xmldoc.getElementsByTagName('category')
		#there will only be one category
		for x in categoryList:
			#***************************get cat name then call category series and load them
			return = x.attributes['name'].value 
	except urllib2.HTTPError, err:
		if err.code == 400:
			#**** deal with this better
			print "error 400"
			return None	
		else:
			raise

#parses series for economic series information, this parses and puts into a database
def xmlSeriesParseAndLoad(url, categoryName = ""):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	seriesList = xmldoc.getElementsByTagName('series')

	db = MySQLdb.connect(host="localhost", user="root", passwd="Optima1!", db="EconomicIndicators")

	cursor = db.cursor() 
	for x in seriesList:
		cursor.execute("SELECT 1 FROM fredindicators WHERE FREDID = \"%s\"" %(x.attributes['id'].value))
		if len(cursor.fetchall()) <= 0:
			print x.attributes['id'].value

			#****************************may have to figure out how to do date and datetime
			#cursor.execute("INSERT INTO fredindicators (FREDID, IndicatorName, ReportingPeriod, \
			#	SeasonalAdjustment, Units, Category, Popularity, ObservationEnd, LastUpdated) \
			#	VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" 
			#	% (x.attributes['id'].value.replace("'","''"), x.attributes['title'].value.replace("'","''"), 
			#	x.attributes['frequency_short'].value, x.attributes['seasonal_adjustment_short'].value, 
			#	x.attributes['units'].value.replace("'","''"), categoryName, x.attributes['popularity'].value,
			#	x.attributes['observation_end'].value, x.attributes['last_updated'].value))

			#db.commit()
			#print "uploaded: " + x.attributes['id'].value

	db.close()

#parses a series information for the date and value of that information
def xmlObservationsParser(url, series):
	xmldoc = minidom.parse(urllib2.urlopen(url))
	observationList = xmldoc.getElementsByTagName('observation')
	print len(observationList)
	observationDict = {}
	
		#print x.attributes['date'].value
		#print x.attributes['value'].value
		#print ''
	observationDict[x.attributes['date'].value] = x.attributes['value'].value








#FREDIndicators
#FREDID  VarChar(16)
#IndicatorName  VarChar(120)
#Reporting Period  VarChar(4)
#SeasonalAdjustment VARCHAR(8)
#Units VARCHAR(45)
#Category VARCHAR(16)
#Popularity INT
#ObservationEnd DATE
#LastUpdated DATETIME

#FredValues
#ValueID  int
#FREDID  VarChar(16)
#RealTimeStart  Date 
#RealTimeEnd  Date 
#Date   DATE 
#Value  Decimal(18,4)




if __name__ == "__main__":
	main()