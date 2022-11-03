#!/usr/bin/env python3
"""
This module converts a CSV to a CHIP_0007 representation
"""
import csv
import json
from sys import argv

def parse_attributes(attributes):
	"""
	Parse the attributes from CSV
	"""
	result = []

	attributes = attributes.split()
	i = 0
	key = ""
	value = ""
	pair = [0, 0]
	for i, word in enumerate(attributes):
		if word.endswith(":"):
			if pair[0] != 0:
				# new key value pair
				if value == "":
					pair[1] = None
				else:
					value = value.strip(",").strip()
					if value == 'none' or value == 'None':
						value = None
					pair[1] = value
				# reset value and pair
				value = ""
				pair = [0, 0]
			key = word.strip(",").strip(":")
			pair[0] = key
		else:
			value = value + " " + word
			continue
		result.append(pair)
	
	for i, pair in enumerate(result):
		if pair[0] == 'none':
			result.pop(i)
	return result
		

def make_json(csvFilePath):
	"""
	Function to convert a CSV to JSON
    Takes the file paths as arguments
	"""
	
	# create dictionary of data and result list
	data = []
	result = []
	
	# Open a csv reader called DictReader
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		
		# Convert each row into a dictionary
		# and add it to data
		for rows in csvReader:

			# print(rows)
			# print("\n\n")
			data.append(rows)

		i = 0
		team = ""
		nft = {}
		jsonFilePath = ""
		attributes = "Attributes- Hair. Eyes. Teeth. Clothing. Accessories. Expression. Strength. Weakness"
		for index, row in enumerate(data):
			if row["Filename"] == "":
				# Save team csv
				# Open a json writer, and use the json.dumps()
				# function to dump data
				if jsonFilePath != "":
					with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
						jsonf.write(json.dumps(nft, indent=4))
				team = row["Series Number"]
				jsonFilePath = f"{team}.json"
				continue
			# create nft dictionary
			nft = {}
			nft["format"] = "CHIP-0007"
			nft["name"] = row["Name"]
			nft["description"] = row["Description"]
			nft["minting_tool"] = team
			nft["sensitive_content"] = False
			nft["series_number"] = row["Series Number"]
			nft["series_total"] = 420
			nft["attributes"] = []
			for attr in parse_attributes(row[attributes]):
				result = {}
				result["trait_type"] = attr[0]
				result["value"] = attr[1]
				nft["attributes"].append(result)
			nft["collection"] = {}
			nft["collection"]["name"] = "Zuri NFT Tickets for Free Lunch"
			nft["collection"]["id"] = row["UUID"]
		
# # Driver Code

# # Decide the two file paths according to your
# # computer system
# csvFilePath = r'Names.csv'
# jsonFilePath = r'Names.json'

# # Call the make_json function
# make_json(csvFilePath, jsonFilePath)
make_json(argv[1])

