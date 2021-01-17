import pandas as pd
import googlemaps

API_KEY = 'AIzaSyCO9FSJNcibybFZ42dCroyS_SA1EYxWsqI'

df = pd.read_csv('locationAppended.csv')

gmaps = googlemaps.Client(key=API_KEY)

for index, row in df.iterrows():

	if index%10 == 0:
		print("{index} are completed.".format(index = index))

	try:
		hosLoc = gmaps.geocode(row['Location'])[0]['geometry']['location']
		df.loc[index, 'Latitude'] = hosLoc['lat']
		df.loc[index, 'Latitude'] = hosLoc['lng']
	except:
		print(index)

df.to_csv('locationAppended.csv', index=False)