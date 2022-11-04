#!/usr/bin/env python3
"""
This module converts a CSV to a CHIP_0007 representation

How to run;
    ./csvtojson.py `csvfilepath`
"""
import csv
import json
import hashlib
from sys import argv


team_list = [
        "TEAM AXE", "TEAM AXLE", "TEAM BEVEL", "TEAM BOOT",
        "TEAM BRAINBOX", "TEAM CHISEL", "TEAM CLUTCH", "TEAM CRANKSHAFT",
        "TEAM ENGINE", "TEAM GEAR", "TEAM GRIT", "TEAM HEADLIGHT",
        "TEAM HYDRAULICS", "TEAM PLUG", "TEAM POWERDRILL", "TEAM PRYBAR",
        "TEAM RULER", "TEAM SANDPAPER", "TEAM SCALE", "TEAM TAPE", "TEAM VBELT"
    ]


def parse_attributes(attributes):
    """
    Parse the attributes from CSV
    """
    result = []

    attributes = attributes.split()
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
                    value = value.strip(";").strip()
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

    # remove empty key value pairs
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
    result_list = []

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            data.append(rows)

        i = 0
        team = data[0]["TEAM NAMES"]
        nft = {}
        jsonFilePath = f"output/{team}.json"
        attributes = "Attributes"
        saved = True
        for index, row in enumerate(data):
            if len(result_list) == 20:
                # Save team csv
                # Open a json writer, and use the json.dumps()
                # Dump data to json file
                with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                    for result in result_list:
                        jsonf.write(json.dumps(result, indent=4))
                    result_list = []

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
            result_list.append(nft)
            if row['TEAM NAMES'] != "" and row['TEAM NAMES'] != team:
                team = row["TEAM NAMES"]
                jsonFilePath = f"output/{team}.json"

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            for result in result_list:
                jsonf.write(json.dumps(result, indent=4))


def hash_jsonfile():
    # hash team json files
    team_dict = {}

    hasher = hashlib.sha256()
    for team in team_list:
        with open(f"output/{team}.json", 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            team_dict[team] = hasher.hexdigest()

    return team_dict


def add_hash_to_csv():
    # Map hash of team json files with to a csv file

    result_list = []
    with open(argv[1], 'r') as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["TEAM NAMES"] in team_list:
                new_team = team_dict[row["TEAM NAMES"]]
                row["HASH"] = team_dict[row["TEAM NAMES"]]
            else:
                row["HASH"] = new_team
            new_dict = row
            result_list.append(new_dict)

    with open("output/filename.output.csv", 'w', newline='') as file:
        fieldlist = [
            'TEAM NAMES', 'Series Number',
            'Filename', 'Name', 'Description',
            'Gender', 'Attributes', 'UUID', 'HASH'
        ]
        writer = csv.writer(file)
        writer.writerow(fieldlist)
        for dicts in result_list:
            values = []
            for k, v in dicts.items():
                values.append(v)
            writer.writerow(values)


# Driver Code
# csvFilePath = first argument to script
# Call the functions
if __name__ == "__main__":
    make_json(argv[1])
    team_dict = hash_jsonfile()
    add_hash_to_csv()
