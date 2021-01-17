import pandas as pd
import googlemaps

API_KEY = 'AIzaSyCO9FSJNcibybFZ42dCroyS_SA1EYxWsqI'

df = pd.read_csv('final.csv')

gmaps = googlemaps.Client(key=API_KEY)

for index, row in df.iterrows():
	if index%10 == 0:
		print('{pos} are done.'.format(pos = index))
	if index%100 == 0:
		df.to_csv('final1.csv', index=False)
	result = gmaps.geocode(row['Location'])[0]['geometry']['location']
	df.loc[index, 'Latitude'] = result['lat']
	df.loc[index, 'Longitude'] = result['lng']

df.to_csv('final1.csv', index=False)