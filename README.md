# Reichelt Elektronik Web Scraping Module

Copyright 2024 Jannik Kreucher

A Python module for extracting data from Reichelt Elektronik, a popular German electronics distributor.


## Table of Contents
- [Web scraping module for Reichelt Elektronik](#web-scraping-module-for-reichelt-elektronik)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
    - [Setup and Dependencies](#setup-and-dependencies)
	- [Standalone Usage](#standalone-usage)
	- [Python Quick Start](#python-quick-start)
	- [Creating the object](#creating-the-object)
	- [Searching with a string](#searching-with-a-string)
	- [Retrieving Detailed Information](#retrieving-detailed-information)
	- [But I want it in one line](#but-i-want-it-in-one-line)
	- [Downloading Datasheets](#downloading-datasheets)

## Introduction

**ReicheltAPI** is a lightweight Python library for scraping data from Reichelt Elektronik using [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/). This module aims to assist in generating Bills of Materials (BOMs) and price estimates within KiCad by retrieving information directly from the Reichelt website.

## Setup and Dependencies

Before running the script, create a virtual environment and install the required Python packages:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Standalone Usage
If you just want to query information about a Reichelt part, you can use the module in standalone mode. The command syntax is simple:
```bash
python3 reichelt.py "<ReicheltPartNo>" <attribute>
```
Make sure to enclose the part number in quotes if it contains spaces. The `<attribute>` is optional and can be any of the keys in the json object. When no attribute is specified the part information will be returned as json string. Here are some useful example attributes:
| Attribute    | Function                                                   |
| ------------ | ---------------------------------------------------------- |
| `part`       | shows parsed part number, should be the same as "PartName" |
| `name`       | Reichelt product name                                      |
| `url`        | url to the item                                            |
| `datasheets` | links to the pdf datasheet                                 |
| `1`          | price of one item                                          |
| `10`         | price per item when buying 10                              |
| `100`        | price when ordering 100                                    |
| `1000`       | price when ordering 1000                                   |

Examples:
```bash
~$ python3 reichelt.py "74HC 00" name  # returns name of item
4-fold, 2 input NAND gates, 2 ... 6 V, DIL-14
~$ python3 reichelt.py "74HC 00" 1  # return unit price
0.24
```


## Python Quick Start

Here's a simple script to get you started:
```python
import reichelt
import json

part = "74HC 00"

# create API object
api = reichelt.Reichelt()
result = api.search_part(part)

# print info
print(json.dumps(result, indent=2))

# download datasheet
api.get_datasheet(result["datasheets"][0], part+".pdf")
```

### Example Output:
```json
{
  "part": "74HC 00",
  "name": "4-fold, 2 input NAND gates, 2 ... 6 V, DIL-14",
  "url": "https://www.reichelt.com/de/en/shop/product/4-fold_2_input_nand_gates_2_6_v_dil-14-3119",
  "price": {
    "currency": "EUR",
    "1": 0.24,
    "10": null,
    "100": null,
    "1000": null
  },
  "availability": "InStock",
  "datasheets": [
    "https://cdn-reichelt.de/documents/datenblatt/A200/DS_NXP_74HC00.pdf",
    "https://cdn-reichelt.de/documents/datenblatt/A200/DS_STM_M74HC00.pdf",
    "https://cdn-reichelt.de/documents/datenblatt/A200/U74HC00_UTC.pdf"
  ],
  "data": {
    "General": {
      "family": "74HC",
      "Model": "NAND-Gate",
      "Type": "4 inputs",
      "Design": "4-Elemente",
      "Mounting form": "DIP-14"
    },
    "Other": {
      "Temperature range": "-40 ... +85"
    },
    "Electrical values": {
      "Supply voltage": "2.0 ... 6.0 VDC",
      "Input voltage": "0 ... 6.0 VDC",
      "Performance": "500 mW",
      "Input voltage ViH": "4.2 VDC",
      "Input voltage ViL": "0.5 VDC"
    },
    "Manufacturer specifications": {
      "Manufacturer": "FREI",
      "Manufacturer ID": "",
      "Weight": "0.001 kg",
      "RoHS": "conform",
      "EAN/GTIN": "9900000031190"
    }
  },
  "categories": [
    "Home",
    "Components",
    "Active components",
    "ICs and controllers",
    "Digital ICs",
    "Logic ICs"
  ]
}
```


## Creating the object

To begin scraping, you need to create an instance of the `Reichelt` object:
```python
import reichelt
foo = reichelt.Reichelt()
```
Ensure that the [`reichelt.py`](reichelt.py) file is in the same directory as your script.


## Searching with a string

You can search for a part using the [`get_search_results(keyword)`](reichelt.py) function, which mimics a browser search on the Reichelt homepage and returns the results as a dictionary.

```python
results = foo.get_search_results("Z80 CPU")
```

### Example Output
```json
[
  {
    "part": "EZ80F92AZ020EG",
    "name": "8-bit microcontroller, eZ80AcclaimPlus!, LQFP-144",
    "url": "https://www.reichelt.com/de/en/shop/product/8-bit_microcontroller_ez80acclaimplus_lqfp-144-376413",
    "price": {
      "1": 13.95,
      "10": null,
      "100": null,
      "1000": null,
      "currency": "EUR"
    }
  },
  {
    "part": "EZ80F91AZA50EK",
    "name": "8-bit microcontroller, eZ80AcclaimPlus!, LQFP-144",
    "url": "https://www.reichelt.com/de/en/shop/product/8-bit_microcontroller_ez80acclaimplus_lqfp-144-376411",
    "price": {
      "1": 17.7,
      "10": null,
      "100": null,
      "1000": null,
      "currency": "EUR"
    }
  },
  ...
]
```


## Retrieving Detailed Information

To retrieve detailed information about a specific item, use the [`get_search_results(keyword)`](reichelt.py) function. Pass the URL of the product page to this function.

```python
product = foo.get_part_information("https://www.reichelt.com/de/en/shop/product/4-fold_2_input_nand_gates_2_6_v_dil-14-3119")
```
Or, you can directly use the link obtained from [`get_search_results`](reichelt.py):
```python
product = foo.get_part_information(result[0]["url"])
```

```json
{
  "part": "74HC 00",
  "name": "4-fold, 2 input NAND gates, 2 ... 6 V, DIL-14",
  "url": "https://www.reichelt.com/de/en/shop/product/4-fold_2_input_nand_gates_2_6_v_dil-14-3119",
  "availability": "InStock",
  "price": {
    "currency": "EUR",
    "1": 0.24,
    "10": null,
    "100": null,
    "1000": null
  },
  "datasheets": [
    "https://cdn-reichelt.de/documents/datenblatt/A200/DS_NXP_74HC00.pdf",
    "https://cdn-reichelt.de/documents/datenblatt/A200/DS_STM_M74HC00.pdf",
    "https://cdn-reichelt.de/documents/datenblatt/A200/U74HC00_UTC.pdf"
  ],
  "data": {
    "General": {
      "family": "74HC",
      "Model": "NAND-Gate",
      "Type": "4 inputs",
      "Design": "4-Elemente",
      "Mounting form": "DIP-14"
    },
    "Other": {
      "Temperature range": "-40 ... +85"
    },
    "Electrical values": {
      "Supply voltage": "2.0 ... 6.0 VDC",
      "Input voltage": "0 ... 6.0 VDC",
      "Performance": "500 mW",
      "Input voltage ViH": "4.2 VDC",
      "Input voltage ViL": "0.5 VDC"
    },
    "Manufacturer specifications": {
      "Manufacturer": "FREI",
      "Manufacturer ID": "",
      "Weight": "0.001 kg",
      "RoHS": "conform",
      "EAN/GTIN": "9900000031190"
    }
  },
  "categories": [
    "Home",
    "Components",
    "Active components",
    "ICs and controllers",
    "Digital ICs",
    "Logic ICs"
  ]
}
```


## But I want it in one line

If you already know the exact part number, you can combine both search and detail retrieval using the [`search_part(part)`](reichelt.py) function:

```python
product = reichelt.Reichelt().search_part("74HC 00")
```


## Downloading Datasheets

The module also allows you to download the product's datasheet directly from Reichelt. The URL is extracted by the [`get_part_information`](reichelt.py) function, and downloading is as simple as:
```python
foo.get_datasheet(product["datasheets"][0], "foo.pdf")
```
This will save the first datasheet as `foo.pdf` in your current directory.
