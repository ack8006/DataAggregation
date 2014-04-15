#http://api.stlouisfed.org/fred/series/observations?series_id=PAYEMS
#&observation_start=2013-03-01&observation_end=2013-03-01
#&realtime_start=2013-04-05&realtime_end=2013-04-05
#&units=chg&api_key=xxxxxxxxxxxxxxxxx

#**kwargs
#identifier
#series
#observation_start
#observation_end
#realtime_start
#realtime_end
#units
#fileType



class FredRequests:
	def __init__ (self):
		self.FredKey = "dbbac155dc1543184204ed045632071e"
		self.fredURLPrefix = "http://api.stlouisfed.org/fred/"
		self.jsonFileType = "&file_type=json"

	def fredRequestURL(self, **kwargs):
		url = self.fredURLPrefix+kwargs['identifier']+kwargs['series']
		if (kwargs['identifier'] == "series/observations?series_id="):
			if ('observation_start' in kwargs) and (observation_end in kwargs):
				url = url + "&observation_start=" + kwargs['observation_start'] +"&observation_end=" + kwargs['observation_end']
		if ('realtime_start' in kwargs) and ('realtime_end' in kwargs):
			url = url + "&realtime_start=" + kwargs['realtime_start'] + "&realtime_end=" + kwargs['realtime_end']
		url = url + "&api_key=" + self.FredKey
		if ('fileType' in kwargs and kwargs['fileType'] == 'JSON'):
			url = url + self.jsonFileType

		#print url
		return url

	def category(self, **kwargs):
		kwargs['identifier'] = "category?category_id="
		return self.fredRequestURL(**kwargs)

	def categorySeries(self, **kwargs):
		kwargs['identifier'] = "category/series?category_id="
		return self.fredRequestURL(**kwargs)
		
	def observations(self, **kwargs):
		kwargs['identifier'] = "series/observations?series_id="
		return self.fredRequestURL(**kwargs)

	def releases(self, **kwargs):
		#finds all releases, DOES NOT provide the data
		kwargs['identifier'] = "series/release?series_id="
		return self.fredRequestURL(**kwargs)

	def series(self, **kwargs):
		kwargs['identifier'] = "series?series_id="
		return self.fredRequestURL(**kwargs)
