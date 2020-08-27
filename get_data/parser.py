###################################
# Parser autovit.ro
# requirements: 
# pip install beautifulsoup4
# pip install requests
# 
# request limit  ???
# 
#

from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import json
import re
from multiprocessing import Pool

carUrls = []
cars = []

root = "photos/"

def parseCarPage(url):
	dict = url

	try:
		response = requests.get(url['link'])

		soup = BeautifulSoup(response.content, 'html.parser')
		res = soup.find_all("li", "offer-params__item")

		### get photos
		photoLinks = soup.find_all("li", "offer-photos-thumbs__item")

		counter = 0
		
		for link in photoLinks:
			link = link.find("img")['src'].split(';')[0]

			try:
				img = requests.get(link)
				fileName = root + dict['id'] + '_' + str(counter) + '.jpg'

				file = open(fileName, "wb")
				file.write(img.content)

				counter += 1
				img.raise_for_status()
			except HTTPError as http_err:
				print(f'HTTP error occurred: {http_err}')  # Python 3.6
			except Exception as err:
				print(f'Other error occurred: {err}')  # Python 3.6
		
	
		### get values
		for entry in res:
			category = entry.find("span", "offer-params__label").text
			value = entry.find("div", "offer-params__value")
			value2 = value.find("a", "offer-params__link")

			if value2 == None:
				value = value.text.strip().rstrip()
			else:
				value = value2.text.strip().rstrip()

			dict[category] = value

		
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')  # Python 3.6
	except Exception as err:
		print(f'Other error occurred: {err}')  # Python 3.6

	cars.append(dict)
	return 


def parseListPage(url):

	try:

		response = requests.get(url)

		soup = BeautifulSoup(response.content, 'html.parser')
		res = soup.find_all("a", "offer-title__link")

		for entry in res:
			dict = { 'id' : entry['data-ad-id'],
					'title': entry['title'],
					'link': entry['href']}
			carUrls.append(dict)


		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')  # Python 3.6
	except Exception as err:
		print(f'Other error occurred: {err}')  # Python 3.6

	return	


def main():
	### pool mechanism 
	#with Pool(5) as p:
		#print(p.map(parseOne, urls))

	#manually define number of pages
	pageString = 'https://www.autovit.ro/autoturisme/?search%5Border%5D=created_at%3Adesc&page='
	numPagesStart = 31
	numPagesEnd = 35

	for idx in range(numPagesStart,numPagesEnd+1):
		parseListPage(pageString + str(idx))

	### save data
	with open('data'  + str(numPagesStart) + '-' + str(numPagesEnd) +  '.json', 'w') as fp:
		json.dump(carUrls, fp)


	#shared list ???? python done fucked up again 
	#with Pool(8) as p:
	#	p.map(parseCarPage, carUrls)

	for idx in range(len(carUrls)):
		parseCarPage(carUrls[idx])

	with open('carData' + str(numPagesStart) + '-' + str(numPagesEnd) + '.json', 'w') as fp:
		json.dump(cars, fp)

if __name__ == '__main__':

	main()
