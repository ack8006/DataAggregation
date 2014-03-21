#downloads data from APIs
#Organizes data 
#stores data into a database
#this is a one time use to download and fully populate the database
#there will be a separate cron job to consistently update the database

import json
import urllib2
#not currently using
import fred

def main():
	fredAPI()



def fredAPI():
	fredAPIKey = "dbbac155dc1543184204ed045632071e"
	jsonFileType = "&file_type=json"
	fredURLPrefix = "http://api.stlouisfed.org/fred/"

	for i in range(0,10):
		url = fredURLPrefix + "category?category_id=" + str(i) + "&api_key=" + fredAPIKey + jsonFileType
		jsonParser(url)

def jsonParser(url):
	#r = urllib2.urlopen(url)
	#data = json.loads(r)
	#print data
	print url




if __name__ == "__main__":
	main()