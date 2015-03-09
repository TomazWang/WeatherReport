# coding=UTF-8
# weather.py 
import urllib2
import xml.etree.ElementTree as ET

# api from CWB, Central Weather Bureau
# 一週縣市天氣預報
# wApiUrl = 'http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-005.xml' 


# get data from CWB's api, return a dict for datas
def getWeatherData():
	# response = urllib2.urlopen(wApiUrl)
	# xml = response.read()

	testFile = open('./res/data.xml','rU')  #testing data
	xml = testFile.read()	
	testFile.close()
	# tree = ET.parse(xml)
	root = ET.fromstring(xml)
	data = root.find("./dataset")
	
	print 'data -> ',data
	return data


def main():
	data = getWeatherData()
	for loc in data.iter('location'):
		print loc


if __name__ == '__main__':
	main()
