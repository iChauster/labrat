import requests
from bs4 import BeautifulSoup

def scrape(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	tab_body = soup.find(text='Inclusion Criteria:')
	container = tab_body.parent.parent
	inc, exc = container.findAll('ul')
	print(inc.text, exc.text)

scrape("https://ClinicalTrials.gov/show/NCT04076280")
scrape("https://ClinicalTrials.gov/show/NCT04101630")