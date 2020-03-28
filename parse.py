import csv
import json
import datetime

CONFIRMED_FILE = 'time_series_covid19_confirmed_global.csv'
DEATHS_FILE = 'time_series_covid19_deaths_global.csv'
RECOVERED_FILE = 'time_series_covid19_recovered_global.csv'

datesRow = None
confirmedData = None
deathsData = None
recoveredData = None

# A small hack to change South Korea name so the comma won't break the format
def southKoreaNameCheck(row):
	if row.split(',')[1] != '"Korea':
		return row.rstrip('\n').split(',')
	return row.replace('"Korea, South"', 'South Korea').rstrip('\n').split(',')

with open(CONFIRMED_FILE, 'r') as csv_file:
	data = csv_file.readlines()
	datesRow = data[0].rstrip('\n').split(',')[4:]
	confirmedData = list(map(southKoreaNameCheck, data[1:]))

with open(DEATHS_FILE, 'r') as csv_file:
	data = csv_file.readlines()
	deathsData = list(map(southKoreaNameCheck, data[1:]))

with open(RECOVERED_FILE, 'r') as csv_file:
	data = csv_file.readlines()
	recoveredData = list(map(southKoreaNameCheck, data[1:]))

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
		'timeline': []
	})

def makeMapOut(country):
	def mapOut(data):
		dataCountry = list(filter(lambda row: row[1] == country, data))
		dataCountry = list(map(lambda row: row[4:], dataCountry))
		dataCountry = list(zip(*dataCountry))
		dataCountry = list(map(lambda entry: sum(list(map(lambda val: int(val), entry))), dataCountry))
		return dataCountry
	return mapOut

for country in countries:
	mapOut = makeMapOut(country['name'])
	confirmedDataCountry = mapOut(confirmedData)
	deathsDataCountry = mapOut(deathsData)
	recoveredDataCountry = mapOut(recoveredData)

	timeline = country['timeline']

	for i, el in enumerate(confirmedDataCountry):
		date = datesRow[i].split('/')
		if i == 0:
			timeline.append({
				'date': datetime.date(2000 + int(date[2]), int(date[0]), int(date[1])).isoformat(),
				'confirmed': el,
				'newConfirmed': el,
				'deaths': deathsDataCountry[i],
				'newDeaths': deathsDataCountry[i],
				'recovered': recoveredDataCountry[i],
				'newRecovered': recoveredDataCountry[i]
			})
		else:
			timeline.append({
				'date': datetime.date(2000 + int(date[2]), int(date[0]), int(date[1])).isoformat(),
				'confirmed': el,
				'newConfirmed': el - confirmedDataCountry[i - 1],
				'deaths': deathsDataCountry[i],
				'newDeaths': deathsDataCountry[i] - deathsDataCountry[i - 1],
				'recovered': recoveredDataCountry[i],
				'newRecovered': recoveredDataCountry[i] - recoveredDataCountry[i - 1]
			})

with open('timelines.json', 'w') as file:
	json.dump(countries, file)
