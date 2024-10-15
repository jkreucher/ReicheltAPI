# Reichelt Elektronik Web Scraping Module

Copyright 2024 Jannik Kreucher

A Python module for extracting data from Reichelt Elektronik, a popular German electronics distributor.


## Table of Contents
- [Web scraping module for Reichelt Elektronik](#web-scraping-module-for-reichelt-elektronik)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
	- [Standalone Usage](#standalone-usage)
	- [Python Quick Start](#python-quick-start)
	- [Creating the object](#creating-the-object)
	- [Searching with a string](#searching-with-a-string)
	- [Retrieving Detailed Information](#retrieving-detailed-information)
	- [But I want it in one line](#but-i-want-it-in-one-line)
	- [Downloading Datasheets](#downloading-datasheets)

## Introduction

**ReicheltAPI** is a lightweight Python library for scraping data from Reichelt Elektronik using [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/). This module aims to assist in generating Bills of Materials (BOMs) and price estimates within KiCad by retrieving information directly from the Reichelt website.

## Standalone Usage
If you just want to query information about a Reichelt part, you can use the module in standalone mode. The command syntax is simple:
```bash
python3 reichelt.py "<ReicheltPartNo>" <attribute>
```
Make sure to enclose the part number in quotes if it contains spaces. The `<attribute>` can be one of the following:
| Attribute   | Function                                                   |
| ----------- | ---------------------------------------------------------- |
| `all`       | everything as json for you to mess around                  |
| `part`      | shows parsed part number, should be the same as "PartName" |
| `name`      | Reichelt product name                                      |
| `link`      | link to the item                                           |
| `datasheet` | link to the pdf datasheet                                  |
| `1`         | price of one item                                          |
| `10`        | price per item when buying 10                              |
| `100`       | price when ordering 100                                    |
| `1000`      | price when ordering 1000                                   |

Examples:
```bash
~$ python3 reichelt.py "Z84C00-06MHZ" name  # returns name of item
Z80 Microprozessor, 6 MHz, DIP40
~$ python3 reichelt.py "Z84C00-06MHZ" 1  # return unit price in Euro
7.25
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
print(json.dumps(result, indent=4))

# download datasheet
api.get_datasheet(result["datasheet"], part+".pdf")
```

### Example Output:
```json
{
    "part": "74HC 00",
    "name": "4-fold, 2 input NAND gates, 2 ... 6 V, DIL-14",
    "link": "https://www.reichelt.com/de/en/4-fold-2-input-nand-gates-2--6-v-dil-14-74hc-00-p3119.html?&trstct=pos_1&nbc=1&SID=9433fcf4a460e776488c64328e79f537447333d0260dc8fc87708",
    "1": 0.24,
    "10": null,
    "100": null,
    "1000": null,
    "datasheet": "https://www.reichelt.com/index.html?ACTION=7&LA=3&OPEN=0&INDEX=0&FILENAME=A200%2FDS_NXP_74HC00.pdf",
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
        "Package weight": "0.001 kg",
        "RoHS": "conform"
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

You can search for a part using the [`get_search_results(keyword)`](reichelt.py) function, which mimics a browser search on the Reichelt homepage but returns the results as a dictionary.

```python
result = foo.get_search_results("Z80 CPU")
```

### Example Output
```json
[
    {
        "part": "EZ80F91AZA50EK",
        "name": "8-bit microcontroller, eZ80AcclaimPlus!, LQFP-144",
        "link": "https://www.reichelt.com/de/en/8-bit-microcontroller-ez80acclaimplus-lqfp-144-ez80f91aza50ek-p376411.html?&trstct=pos_0&nbc=1&SID=968601949b80683845a58c8f12e7374d7421209b4623f36305e19",
        "1": 17.7,
        "10": null,
        "100": null,
        "1000": null
    },
    {
        "part": "EZ80F92AZ020EG",
        "name": "8-bit microcontroller, eZ80AcclaimPlus!, LQFP-144",
        "link": "https://www.reichelt.com/de/en/8-bit-microcontroller-ez80acclaimplus-lqfp-144-ez80f92az020eg-p376413.html?&trstct=pos_1&nbc=1&SID=968601949b80683845a58c8f12e7374d7421209b4623f36305e19",
        "1": 13.95,
        "10": null,
        "100": null,
        "1000": null
    },
...
```


## Retrieving Detailed Information

To retrieve detailed information about a specific item, use the [`get_search_results(keyword)`](reichelt.py) function. Pass the URL of the product page to this function.

```python
product = foo.get_part_information("https://www.reichelt.de/z80-microprozessor-10-mhz-dip40-z84c00-10mhz-p31823.html?&trstct=pos_2&nbc=1")
```
Or, you can directly use the link obtained from [`get_search_results`](reichelt.py):
```python
product = foo.get_part_information(result[0]["link"])
```

```json
{
    "datasheet": "https://www.reichelt.com/index.html?ACTION=7&LA=3&OPEN=0&INDEX=0&FILENAME=A200%2FPS0270.pdf",
    "General": {
        "Type": "8-Bit Mikrocontroller",
        "Technology": "eZ80",
        "Mounting form": "LQFP-144",
        "family": "EZ80F91"
    },
    "Specials": {
        "CPU clock": "50 MHz"
    },
    "Implementation": {
        "Memory": "256",
        "RAM": "8 kByte",
        "I/O-Pins": "32",
        "16-bit Timer": "4"
    },
    "Interfaces": {
        "I²C": "1",
        "UART": "2"
    },
    "Electrical values": {
        "Supply voltage": "3..3.6 VDC"
    },
    "Other": {
        "Temperature range": "-40..+105"
    },
    "Manufacturer specifications": {
        "Manufacturer": "ZILOG",
        "Factory number": "EZ80F91AZA50EK",
        "Package weight": "0.014 kg",
        "RoHS": "conform"
    },
    "categories": [
        "Home",
        "Components",
        "Active components",
        "ICs and controllers",
        "Digital ICs",
        "8-bit microcontrollers"
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
foo.get_datasheet(product["datasheet"], "foo.pdf")
```
This will save the datasheet as `foo.pdf` in your current directory.
