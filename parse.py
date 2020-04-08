import csv
import json
import datetime

CONFIRMED_FILE = 'time_series_covid19_confirmed_global.csv'
DEATHS_FILE = 'time_series_covid19_deaths_global.csv'
RECOVERED_FILE = 'time_series_covid19_recovered_global.csv'

datesRow = []
confirmedData = []
deathsData = []
recoveredData = []

# A small hack to change South Korea name so the comma won't break the format
# def southKoreaNameCheck(row):
# 	if row.split(',')[1] != '"Korea':
# 		return row.rstrip('\n').split(',')
# 	return row.replace('"Korea, South"', 'South Korea').rstrip('\n').split(',')

with open(CONFIRMED_FILE, 'r') as csv_file:
	reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	readDates = True
	for row in reader:
		if readDates:
			datesRow = row[4:]
			readDates = False
		else:
			confirmedData.append(row)

with open(DEATHS_FILE, 'r') as csv_file:
	reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	readDates = True
	for row in reader:
		if readDates: readDates = False
		else:
			deathsData.append(row)

with open(RECOVERED_FILE, 'r') as csv_file:
	reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	readDates = True
	for row in reader:
		if readDates: readDates = False
		else:
			recoveredData.append(row)

countries = []

def unique(array):
	newArray = []
	for el in array:
		if el not in newArray:
			newArray.append(el)
	return newArray

for country in unique(list(map(lambda row: row[1], confirmedData))):
	countries.append({
		'name': country,
		'timeline': [],
		'states': []
	})

def arrayToIntArray(arr):
	return list(map(lambda val: int(val), arr))

def makeMapOut(country):
	def mapOut(data):
		dataCountry = list(filter(lambda row: row[1] == country, data))
		dataStates = list(map(lambda row: arrayToIntArray(row[4:]), dataCountry))
		dataCountry = list(zip(*dataStates))
		dataCountry = list(map(lambda entry: sum(entry), dataCountry))
		return (dataCountry, dataStates)
	return mapOut

def mapIntoTimeline(datesRow, confirmedTuple, deathsTuple, recoveredTuple):
	useConfirmed, confirmedData = confirmedTuple
	useDeaths, deathsData = deathsTuple
	useRecovered, recoveredData = recoveredTuple
	def addConfirmed(dictionary, confirmed, confirmedPrev):
		dictionary['confirmed'] = confirmed
		dictionary['newConfirmed'] = confirmed - confirmedPrev
		return dictionary
	def addDeaths(dictionary, deaths, deathsPrev):
		dictionary['deaths'] = deaths
		dictionary['newDeaths'] = deaths - deathsPrev
		return dictionary
	def addRecovered(dictionary, recovered, recoveredPrev):
		dictionary['recovered'] = recovered
		dictionary['newRecovered'] = recovered - recoveredPrev
		return dictionary

	timeline = []

	for i, el in enumerate(confirmedData):
		date = datesRow[i].split('/')
		if i == 0:
			dictionary = {
				'date': datetime.date(2000 + int(date[2]), int(date[0]), int(date[1])).isoformat()
			}
			if (useConfirmed):
				dictionary = addConfirmed(dictionary, el, 0)
			if (useDeaths):
				dictionary = addDeaths(dictionary, deathsData[i], 0)
			if (useRecovered):
				dictionary = addRecovered(dictionary, recoveredData[i], 0)
			timeline.append(dictionary)
		else:
			dictionary = {
				'date': datetime.date(2000 + int(date[2]), int(date[0]), int(date[1])).isoformat()
			}
			if (useConfirmed):
				dictionary = addConfirmed(dictionary, el, confirmedData[i - 1])
			if (useDeaths):
				dictionary = addDeaths(dictionary, deathsData[i], deathsData[i - 1])
			if (useRecovered):
				dictionary = addRecovered(dictionary, recoveredData[i], recoveredData[i - 1])
			timeline.append(dictionary)

	return timeline

for country in countries:
	mapOut = makeMapOut(country['name'])
	statesList = list(map(lambda row: row[0], list(filter(lambda row: row[1] == country['name'], confirmedData))))
	confirmedDataCountry, confirmedDataState = mapOut(confirmedData)
	deathsDataCountry, deathsDataState = mapOut(deathsData)
	recoveredDataCountry, recoveredDataState = mapOut(recoveredData)

	country['timeline'] = mapIntoTimeline(datesRow, (True, confirmedDataCountry), (True, deathsDataCountry), (True, recoveredDataCountry))

	states = country['states']
	# Are there any states? If not, remove sates key.
	if statesList[0] != '':
		# Check if number of states is equal to number of different data sets.
		# If it's not, that means that some data set doesn't have data for each
		# state and we are going to assume that data sets for each state is not
		# specifed. There are some examples of this like Canada.
		useConfirmed = len(confirmedDataState) == len(statesList)
		useDeaths = len(deathsDataState) == len(statesList)
		useRecovered = len(recoveredDataState) == len(statesList)

		for i, state in enumerate(statesList):
			states.append({
				'name': state,
				'timeline': mapIntoTimeline(datesRow, (useConfirmed, confirmedDataState[i] if useConfirmed else None), (useDeaths, deathsDataState[i] if useDeaths else None), (useRecovered, recoveredDataState[i] if useRecovered else None))
			})
	else:
		states = []

with open('timelines.json', 'w') as file:
	json.dump(countries, file)
