import requests
from bs4 import BeautifulSoup
import pandas as pd

def getContacts(soup):
	name = soup.find('td', {"headers": "contactName"})
	name = name.text if name else None
	contactPhone = soup.find('td', {"headers":"contactPhone"})
	contactPhone = contactPhone.text if contactPhone else None
	contactEmail = soup.find('td', {"headers":"contactEmail"})
	contactEmail = contactEmail.text if contactEmail else None
	contactAddress = soup.find('td', {"headers":"contactAddress"})
	contactAddress = contactAddress.text if contactAddress else None
	return (name, contactPhone, contactEmail, contactAddress)

def getCriteria(soup):
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

def scrape(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	gc = getCriteria(soup)
	contact = getContacts(soup)
	return gc, contact

def updateCSV(csv):
	df = pd.read_csv(csv)
	failures = []
	for i, row in df.iterrows():
			try:
				scrapedCriteria, contactInfo = scrape(row['URL'])
				name, contactPhone, contactEmail, contactAddress = contactInfo
				inclusionCrit, exclusionCrit = "", ""
				for key, value in scrapedCriteria:
					if "inclusion" in key.lower():
						inclusionCrit += value
					elif "exclusion" in key.lower():
						exclusionCrit += value
					else:
						print(key.lower())
				df.at[i, "InclusionCrit"] = inclusionCrit
				df.at[i, "ExclusionCrit"] = exclusionCrit
				df.at[i, "contactName"] = name if name else ""
				df.at[i, "contactPhone"] = contactPhone if contactPhone else ""
				df.at[i, "contactEmail"] = contactEmail if contactEmail else ""
				df.at[i, "contactAddress"] = contactAddress if contactAddress else ""
			except Exception as e:
				print(e)
				failures.append(row["URL"])
				print(f'failure for {row["URL"]}')
	df.to_csv('final.csv')
	print(failures)
	
updateCSV("./locationAppended.csv")
