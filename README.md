# Web scraping module for Reichelt Elektronik

Copyright 2021 Jannik Kreucher

**NOTE: This Project is still work in progress!**


## Table of Contents
- [Web scraping module for Reichelt Elektronik](#web-scraping-module-for-reichelt-elektronik)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
	- [Quick Start](#quick-start)
	- [Creating the object](#creating-the-object)
	- [Searching with a string](#searching-with-a-string)
	- [Getting more data](#getting-more-data)
	- [But I want it in one line](#but-i-want-it-in-one-line)
	- [Downloading Datasheets](#downloading-datasheets)

## Introduction

ReicheltAPI is a very simple Python libaray for pulling data from the rather popular german distributor Reichelt Elektronik. This is achived by scraping the Reichelt website with [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/). The goal of this project is to build a python module for generating BOMs and price estimates within KiCad.

## Quick Start

A very simple script to get started: [`api_test.py`](api_test.py)
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

Here the variable *result* contains the following:
```json
{
    "part": "74HC 00",
    "name": "4-fach, 2 Eingangs-NAND-Gatter,  2 ... 6 V, DIL-14",
    "link": "https://www.reichelt.de/de/de/4-fach-[...]",
    "1": 0.26,
    "10": null,
    "100": null,
    "1000": null,
    "datasheet": "https://www.reichelt.de/index.html?[...].pdf",
    "Allgemeines": {
        "Familie": "74HC",
        "Modell": "NAND-Gate",
        "Typ": "2 Eingänge",
        "Ausführung": "4-Elemente",
        "Bauform": "DIP-14"
    },
    "Sonstiges": {
        "Temperaturbereich": "-40 ... +85 °C"
    },
    "Elektrische Werte": {
        "Versorgungsspannung": "2,0 ... 6,0 VDC",
        "Eingangsspannung Vi": "0 ... 6,0 VDC",
        "Leistung": "500 mW",
        "Eingangsspannung ViH": "4,2 VDC",
        "Eingangsspannung ViL": "0,5 VDC"
    },
    "Herstellerangaben": {
        "Verpackungsgewicht": "0.001 kg",
        "RoHS": "konform",
        "EAN / GTIN": "9900000031190"
    },
    "categories": [
        "Startseite",
        "Bauelemente",
        "Bauelemente, aktiv",
        "ICs & Controller",
        "ICs digital",
        "Logik-ICs"
    ]
}
```


## Creating the object

To start scraping data, the object needs to be constructed:
```python
import reichelt
foo = reichelt.Reichelt()
```
Note that the file [`reichelt.py`](reichelt.py) needs to be in the same directory


## Searching with a string

The function [`get_search_results(keyword)`](reichelt.py) starts a search on the Reichelt homepage like you would in your browser. But it returns a dict with the most important information.
```python
result = foo.get_search_results("Z80")
```

```json
[
	{
        "part": "Z84C00-10MHZ",
        "name": "Z80 Microprozessor, 10 MHz, DIP40",
        "link": "https://www.reichelt.de/de/de/z80-microprozessor-10-mhz-dip40-z84c00-10mhz-p31823.html[...]",
        "1": 7.12,
        "10": null,
        "100": null,
        "1000": null
    },
    {
        "part": "Z84C30-06MHZ",
        "name": "Z80 MICRPROZESSOR DIL-28",
        "link": "https://www.reichelt.de/de/de/z80-micrprozessor-dil-28-z84c30-06mhz-p23034.html[...]",
        "1": 6.67,
        "10": null,
        "100": null,
        "1000": null
    }
...
```
The function returns a array of the items found by the keyword or string. Note that only items on the first page are parsed. The key 1 is the price for this specific item. The keys 10, 100 and 1000 show the discounted price for the respective order volume. Null means there is no discount obviously.


## Getting more data

To get even more information about a item the function [`get_search_results(keyword)`](reichelt.py) can be utilized. It requires a link to a specific item and returns more information about the product.
```python
product = foo.get_part_information("https://www.reichelt.de/z80-microprozessor-10-mhz-dip40-z84c00-10mhz-p31823.html?&trstct=pos_2&nbc=1")
```
Or if you want to use the link provided by *get_search_results* above directly:
```python
product = foo.get_part_information(result[0]["link"])
```

```json
{
    "datasheet": "https://www.reichelt.de/index.html?ACTION=7&LA=3&OPEN=0&INDEX=0&FILENAME=A300%2FZ84C00%23ZIL.pdf",
    "Allgemeines": {
        "Modell": "Microprozessor",
        "Typ": "CPU",
        "Ausführung": "4 Kanäle",
        "Bauform": "PDIP-40"
    },
    "Besonderheiten": {
        "CPU Takt": "10 MHz"
    },
    "Herstellerangaben": {
        "Hersteller": "ZILOG",
        "Artikelnummer des Herstellers": "Z84C0010PEG",
        "Verpackungsgewicht": "0.007 kg",
        "EAN / GTIN": "9900000318239"
    },
    "categories": [
        "Startseite",
        "Bauelemente",
        "Bauelemente, aktiv",
        "ICs & Controller",
        "ICs digital",
        "8-Bit Microcontroller"
    ]
}
```


## But I want it in one line

[`search_part(part)`](reichelt.py) combines the two and is meant for getting data about an item when the Reichelt part number is known. The part number is passed as a string. Note that the part number must be exact!
```python
product = reichelt.Reichelt().search_part("74HC 00")
```


## Downloading Datasheets

This module allows you to download the datasheet from Reichelt as well. Since the link to the datasheet is parsed by *get_part_information* it is very easy to implement:
```python
foo.get_datasheet(product["datasheet"], "foo.pdf")
```
Now the datasheet for the product above is saved in "foo.pdf".


