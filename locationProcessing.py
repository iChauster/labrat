import pandas as pd
import requests, json
import googlemaps, traceback

API_KEY = 'AIzaSyCO9FSJNcibybFZ42dCroyS_SA1EYxWsqI'

df = pd.read_csv('combinedStudies.csv')
df['Locations'] = df['Locations'].apply(lambda x: x.split('|'))
df['Location Distances'] = None
df['Location Times'] = None

gmaps = googlemaps.Client(key='AIzaSyC7LO5SjC-6phou3MfA1VHEOsZbIMi-RwE')
permAddress = '4238 Pine Street, Philadelphia, PA'
permLoc = gmaps.geocode(permAddress)[0]['geometry']['location']
permLoc = (permLoc['lat'], permLoc['lng'])

def pullDistanceTime(matrix):
	dis = int(float(matrix['distance']['text'].split()[0].replace(',','')))
	return (dis,matrix['duration']['text'])

for index, row in df.iterrows():
	result = None
	startingRow = row['Locations']
	try:
		if index % 50 == 0:
			print("{index} are done.".format(index = index))
		if index % 100 == 0:
			df.to_csv('locationAppended.csv', index=False)
			print(df)
		startingRow = list(filter(lambda x: "Hawaii" not in x and "Alaska" not in x, startingRow))
		if len(startingRow) == 0:
			continue
		hosCo = []
		for index2, hospital in enumerate(startingRow):
			if index2 > 15:
				startingRow = startingRow[0:10]
				break
			hosLoc = gmaps.geocode(hospital)
			hosLoc = hosLoc[0]['geometry']['location']
			hosLoc = (hosLoc['lat'], hosLoc['lng'])
			hosCo.append(hosLoc)
		result = gmaps.distance_matrix(hosCo, permLoc, mode='driving', units = 'imperial')
		numLocations = len(startingRow)
		unsortedDis, unsortedTimes = [], []
		for i in range(numLocations):
			matrix = result['rows']
			matrix = matrix[i]
			matrix = matrix['elements']
			matrix = matrix[0]
			if matrix['status'] != 'OK':
				unsortedDis.append(1e9)
				unsortedTimes.append((1e9,59))
			else:
				dis, time = pullDistanceTime(matrix)
				unsortedDis.append(dis)
				unsortedTimes.append(time)
		if len(row['Locations']) > 1:
			resultant = sorted(zip(startingRow, unsortedDis, unsortedTimes), key = lambda x: x[1])
			endingRow, sortedDis, sortedTimes = zip(*list(resultant))
			df.loc[index,'Locations'] = endingRow[0]
			df.loc[index,'Location Distances'] = sortedDis[0]
			df.loc[index,'Location Times'] = sortedTimes[0]
		else:
			df.loc[index,'Locations'] = startingRow[0]
			df.loc[index,'Location Distances'] = unsortedDis[0]
			df.loc[index,'Location Times'] = unsortedTimes[0]
	except:
		print(index)
		traceback.print_exc() 

print(df)

df.to_csv('locationAppended.csv', index=False)  


#Patient Home Address: 4238 Pine Street, Philadelphia, PA

#inclusion/exclusion criteria

#splitting locations string into array
#remove NaN