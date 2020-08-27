import json
import glob

csvFileName = 'finalData.csv'

### some have missing header columns => causes shifts 
header = ['id', 'title', 'link', 'Oferit de', 'Categorie', 'Marca', 'Model', 'Versiune',\
		'Anul fabricatiei', 'Kilometraj', 'Capacitate cilindrica', 'VIN', \
		'Combustibil', 'Putere', 'Cutie de viteze', 'Transmisie', 'Norma de poluare', \
		'Filtru de particule', 'Caroserie', 'Culoare', 'Primul proprietar', \
		'Fara accident in istoric', 'Carte de service', 'Stare']

headerBool = 0

if __name__ == '__main__':
	fileNames = glob.glob('carData*')

	with open(csvFileName, 'w') as f:
		
		###Header
		headerString = ''
		for h in header:
			headerString += h + ','
		f.write(headerString[:-1] + '\n')

		###Data
		for fileName in fileNames:
			with open(fileName, 'r') as jsonFile:
				res = json.loads(jsonFile.read())
				for entry in res:
					dataString = ''

					keys = entry.keys()
					for head in header:
						if head in keys:
							dataString += str(entry[head]) + ','
						else:
							dataString += 'NODATA,'

					f.write(dataString[:-1] + '\n')


