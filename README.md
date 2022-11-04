A simple Python Script to generate CHIP-0007 compatible json files from CSV files.

## Installation

The app's dependencies are managed using composer. Make sure that the latest versions of [php](http://php.net) and [composer](https://getcomposer.org) are installed then run:

```bash
composer install
```

## Usage
Run shell script, pass in one argument (path to csv file)

```bash
./csvtojson.sh pathtocsv
```

	### example

	```bash
	./csvtojson.sh "HNGi9 CSV FILE - Sheet1.csv"
	```

Here is the json file with the default values:

```jsonc
{
    "format": "CHIP-0007",
    "name": "Pikachu",
    "description": "Electric-type Pokémon with stretchy cheeks",
    "minting_tool": "SuperMinter/2.5.2",
    "sensitive_content": false,
    "series_number": 0,
    "series_total": 0,
    "attributes": [],
    "collection": {
        "name": "Example Pokémon Collection",
        "id": "e43fcfe6-1d5c-4d6e-82da-5de3aa8b3b57",
        "attributes": [
            {
                "type": "description",
                "value": "Example Pokémon Collection is the best Pokémon collection. Get yours today!"
            },
            {
                "type": "icon",
                "value": "https://examplepokemoncollection.com/image/icon.png"
            },
            {
                "type": "banner",
                "value": "https://examplepokemoncollection.com/image/banner.png"
            },
            {
                "type": "twitter",
                "value": "ExamplePokemonCollection"
            },
            {
                "type": "website",
                "value": "https://examplepokemoncollection.com/"
            }
        ]
    },
    "data": {}
}
```

**Below is a sample csv file**

| TEAM NAMES | Series Number | Filename          | Name              | Description                                 | Gender | Attributes                                                                                                                        | UUID                                 |
| ---------- | ------------- | ----------------- | ----------------- | ------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| TEAM BEVEL | 1             | adewale-the-amebo | adewale the amebo | Adewale likes to be in everyone's business. | Male   | hair: bald; eyes: black; teeth: none; clothing: red; accessories: mask; expression: none; strength: powerful; weakness: curiosity | cad316c3-37f8-4b27-9f53-9d803bfcfee7 |

The generated files and their sha256 has would located in the `./output` directory. A new file `filename.output.csv` (where filename is the name of the source file) is created in the output directory. This file contains the contents of the source csv file and a new column `hash` with the hash of the json corresponding json file.
