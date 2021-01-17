import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	tab_body = soup.findAll(text='Eligibility Criteria')
	found = None
	for i in tab_body:
		classes = i.parent.attrs.get('class')
		if classes and classes[0] == 'ct-header2':
			found = i.parent
			break
	if not found: return None
	container = found.parent.parent.find(text="Criteria")
	container = container.parent.parent.findAll(class_="tr-indent2")[-1]
	titles = [t.text for t in container.findAll('p')]
	titleDsc = [t.text for t in container.findAll('ul')]
	lDsc, lTitle = len(titleDsc), len(titles)
	if lDsc < lTitle:
		titles = titles[lTitle - lDsc:]
	elif lTitle < lDsc:
		print("Uncaught Issue")
	return list(zip(titles, titleDsc))
	
def updateCSV(csv):
	df = pd.read_csv(csv)
	failures = []
	for i, row in df.iterrows():
		try:
			scrapedCriteria = scrape(row['URL'])
			inclusionCrit, exclusionCrit = "", ""
			for key, value in scrapedCriteria:
				if "inclusion criteria" in key.lower():
					inclusionCrit += value
				elif "exclusion criteria" in key.lower():
					exclusionCrit += value
				else:
					print(key.lower())
			df.at[i, "InclusionCrit"] = inclusionCrit
			df.at[i, "ExclusionCrit"] = exclusionCrit
		except:
			failures.append(row["URL"])
			print(f'failure for {row["URL"]}')
	df.to_csv('demo.csv')
	print(failures)
	
# updateCSV("./combinedStudies.csv")
