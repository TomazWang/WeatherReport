# coding=UTF-8
# weather.py 
import urllib2
import xml.etree.ElementTree as ET
import datetime

# api from CWB, Central Weather Bureau
# 一週縣市天氣預報
wApiUrl = 'http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-005.xml' 

# Tags
NAMESPACE = '{urn:cwb:gov:tw:cwbcommon:0.1}'
TAG_dataset = NAMESPACE+'dataset'
TAG_location = NAMESPACE+'location'
TAG_locationName = NAMESPACE+'locationName'
TAG_weatherElement = NAMESPACE+'weatherElement'
TAG_elementName = NAMESPACE+'elementName'
TAG_time = NAMESPACE+'time'
TAG_startTime = NAMESPACE+'startTime'
TAG_endTime = NAMESPACE+'endTime'
TAG_parameter = NAMESPACE+'parameter'
TAG_parameterName = NAMESPACE+'parameterName'
TAG_parameterValue = NAMESPACE+'parameterValue'
TAG_parameterUnit = NAMESPACE+'parameterUnit'

E_TYPE_Wx = 'Wx'
E_TYPE_MaxT = 'MaxT'
E_TYPE_MinT = 'MinT'


# get data from CWB's api, return a dict for datas
def getWeatherData():
	response = urllib2.urlopen(wApiUrl)
	xml = response.read()

	# testFile = open('./res/data.xml','rU')  #testing data
	# xml = testFile.read()	# xml is a big string of xml data
	# testFile.close()

	return xml

# parsing xml date to a list of dict
def parsingData(xml):
	# parsing xml string into a element tree
	root = ET.fromstring(xml)
	dataset = root.find('.//'+TAG_dataset)
	# print 'dateset = ',dataset
	mainWeatherDB = []


	allLocation = dataset.findall(TAG_location)
	# print 'allloction = ',allLocation

	for locDataElement in allLocation: # parsing every location
		loc = locDataElement.find(TAG_locationName)
		# print 'loc -> ', loc
		locName = loc.text
		# print 'locName ->',locName

		# create a empty location into db

		# datas = [
		# 			{
		# 				'st':start time,
		# 				'et':end time,
		# 				'wx':weather,
		# 				'maxT':max temp,
		# 				'minT':min temp
		# 			},
		#	 			...
		#				...
		# 		]
		locData = {'location':locName, 'datas':[]}
		wes = locDataElement.findall(TAG_weatherElement)
		# print 'wes = ',wes

		for we in wes:
			timeElements = we.findall(TAG_time) # <time>
			eType = we.find(TAG_elementName)	# get element type

			for timeElement in timeElements:

				startTimeStr = timeElement.find(TAG_startTime)
				endTimeStr = timeElement.find(TAG_endTime)

				startDateTime = stringToDateTime(startTimeStr.text)
				endDateTime = stringToDateTime(endTimeStr.text)

				# check if there's a data in locData/datas 
				timeData = {}
				for existTimeData in locData.get('datas') :
					if existTimeData.get('st') == startDateTime :
						timeData = existTimeData
				
				if timeData == {} :
					timeData = {'st':startDateTime,'et':endDateTime}
					locData.get('datas').append(timeData)


				if eType.text == E_TYPE_Wx:
					wxParam = timeElement.find('.//'+TAG_parameter+'/'+TAG_parameterName)
					timeData['wx'] = wxParam.text

				elif eType.text == E_TYPE_MaxT:
					maxTemp = timeElement.find('.//'+TAG_parameter+'/'+TAG_parameterName)
					timeData['maxT'] = maxTemp.text

				elif eType.text == E_TYPE_MinT:
					minTemp = timeElement.find('.//'+TAG_parameter+'/'+TAG_parameterName)
					timeData['minT'] = minTemp.text

		# add locdata into main db	
		mainWeatherDB.append(locData)

	return mainWeatherDB

# parsing string to date and time tuple
def stringToDateTime(timeStr):
	# time formate from CWB : 2015-03-09T17:00:00+08:00
	# print 'sting to date and time func parsing : ',timeStr
	dateAndTimeStr = timeStr.split('T')
	dateStr = dateAndTimeStr[0]
	timeStr = dateAndTimeStr[1]
	# print 'dateStr = ',dateStr
	# print 'timeStr = ',timeStr
	date = datetime.datetime.strptime(dateStr,'%Y-%m-%d').date()
	# print 'date = ',date

	time = datetime.datetime.strptime(((timeStr.split('+'))[0]),'%X').time()
	# print 'time = ',time

	return (date,time)
		
def showData(data):
	'''
	data = list of locDatas
	locData = {'location':locName, 'datas':[]}	
	datas = [
					{
						'st':start time,
						'et':end time,
						'wx':weather,
						'maxT':max temp,
						'minT':min temp
					},
			 			...
						...
				]
	'''


	i = 1
	index = ''
	for locData in data :

		if i < 10 :
			index = '0'+str(i)
		else :
			index = str(i)
		
		print index,locData['location']
		i += 1

	print 'Hey there! Where are you?'
	usr_input = raw_input()

	loc_index = int(usr_input)

	if loc_index <= i and loc_index > 0:
		loc_index -= 1
		locData = data[loc_index]
		print '\n\n'
		print 'location:',locData['location']
		print '=================================='
		print '| Date | weather | max temp | min temp |'
		for timedata in locData['datas']:
			print '----------------------------------'
			print '|',timedata['st'][0],timedata['wx'],timedata['maxT'],timedata['minT'],'|'

def main():
	xml = getWeatherData()
	data = parsingData(xml)
	showData(data)


if __name__ == '__main__':
	main()
