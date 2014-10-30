'''Read a CSV file containing delivery information, extract zipcode frequencies and bucket delivery values into 0-60/60-120/120+'''


import csv

global FILE_PATH , WRITE_FILE_PATH

FILE_PATH = 'delivery_data.csv' ##Set this to point to the deliveries CSV file
WRITE_FILE_PATH = 'delivery_values.csv'


"""Writes the first line (headers) of the resulting csv file"""
def writeCSVHeaders():
	file = open(WRITE_FILE_PATH, 'w')
	file.write("Zipcode,Less_Than_$60,Btw_$60_$120,Above_$120\n")
	file.close()

"""Given a table of price buckets for zipcodes, produces the desired table"""
def writeToCSV(priceTable):
	writeCSVHeaders()
	file = open(WRITE_FILE_PATH, 'a')
	for key in priceTable.keys():
		string = str(key) + ',' + str(priceTable[key]).strip('[]') + '\n'
		file.write(string)

	file.close()

'''
Returns a table (dictionary) representing how many deliveries were made in each zipcode
'''
def createZipFrequencyTable():
	zipFrequency = {}
	with open(FILE_PATH, 'rU') as csvfile:
		deliveryArray = csv.reader(csvfile)
		for entry in deliveryArray: #[zip, price, customerid, pickupid, avg_courier,status]
			if entry[0]:
				if zipFrequency.has_key(entry[0]):
					zipFrequency[entry[0]] += 1
				else: 
					zipFrequency[entry[0]] = 1

	return zipFrequency

'''
Returns a table (dictionary) representing, for each zipcode, how many deliveries were made in the 0-$60 / $60-$120 / $120+ ranges
Parameter: countDictionary - a dictionary representing how many deliveries happened in each zipcode

'''
def bucketDeliveryValues(countDictionary):
	zipcodeValues = {}
	with open(FILE_PATH, 'rU') as csvfile:
		deliveryArray = csv.reader(csvfile)
		for entry in deliveryArray:
			if entry[0] in countDictionary: #If the value is defined and the zipcode has 200+ deliveries
				#decide on the bucket
				bucket = -1

				if (float(entry[1]) < 60.0):
					bucket = 1
				elif (float(entry[1]) < 120.0):
					bucket = 2
				elif (120 < entry [1]): 
					bucket = 3
				else:
					continue

				# print bucket
				if (entry[0] in zipcodeValues): 
					zipcodeValues[entry[0]][bucket - 1] += 1
				else:
					zipcodeValues[entry[0]] = [0,0,0]
					zipcodeValues[entry[0]][bucket - 1] += 1
	
	return zipcodeValues

"""
Removes from a dictionary any keys whose values are <= n
Parameter: dictionary - the dictionary upon which the function acts
Parameter: n - the lower bound filter for the values
"""
def removeValuesFromDict(dictionary, n):
	for key in dictionary.keys():
		if dictionary.get(key) <= n:
			del dictionary[key]

"""Main Driver function"""
def main():
	
	table = createZipFrequencyTable()
	removeValuesFromDict(table, 200)

	priceTable = bucketDeliveryValues(table)
	writeToCSV(priceTable)
	
if __name__ == "__main__":
	main()