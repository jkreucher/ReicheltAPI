#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Reichelt:
    """
    Class for interacting with Reichelt Elektronik's product catalog.

    Provides methods to search for products, extract detailed product data,
    and download datasheets.
    """

    def __init__(self):
        """
        Initialize the Reichelt object with default HTTP headers.
        """
        self.req_headers = {
            'Accept-Language': 'en-US;q=0.7,en;q=0.3'
        }
    

    def get_search_results(self, keyword: str) -> list[dict]:
        """
        Search Reichelt for a keyword and return a list of product summaries.

        Args:
            keyword (str): Search term for querying products.

        Returns:
            list[dict]: A list of dictionaries, each containing data about a product (part number, name, price tiers, URL, etc).
        """
        # download search results as raw html
        url = "https://www.reichelt.com/index.html?ACTION=446&LA=0&nbc=1&q=%s" % keyword.lower().replace(" ", "%20")
        website = requests.get(url, headers=self.req_headers).content.decode('utf-8')
        parser = BeautifulSoup(website, 'html.parser')
        # get every part in the search result list. Each part is in a div named "al_gallery_article".
        parts=[]
        for part_html in parser.find_all("div", "al_gallery_article"):
            # create json object for each part
            part={"part":"", "name":"", "url":"", "price":None}
            # extract data
            part["part"] = part_html.find("meta", itemprop="productID").get("content") # part number
            part["name"] = part_html.find("meta", itemprop="name").get("content") # part name
            part["url"] = part_html.find("a", "al_artinfo_link").get("href") # href
            # find price if there is one
            part["price"] = {}
            part["price"]["1"] = float(part_html.find("meta", itemprop="price").get("content"))
            part["price"]["10"] = None
            part["price"]["100"] = None
            part["price"]["1000"] = None
            part["price"]["currency"] = part_html.find("meta", itemprop="priceCurrency").get("content")
            # find discounts. Price for 10, 100, 1000 peaces are added to the array
            if(part_html.find("ul", "discounts") ):
                # get every price from discount table
                for discount_lis in part_html.find("ul", "discounts").find_all("li"):
                    span_quant = discount_lis.find("span", attrs={"data-discquant": True})
                    span_price = discount_lis.find("span", attrs={"data-discprice": True})
                    quant = span_quant.get("data-discquant") if span_quant else None
                    price = span_price.get("data-discprice") if span_price else None
                    if quant:
                        part["price"][quant] = float(price)
            # add part to list
            parts.append(part)
        # return part list
        return parts
    

    def get_part_information(self, url: str) -> dict:
        """
        Retrieve detailed information for a specific part from its product page.

        Args:
            url (str): URL of the product page.

        Returns:
            dict: A dictionary containing detailed information including name, pricing, availability, datasheets, technical specs, and categories.
        """
        # download website
        website = requests.get(url, headers=self.req_headers).content.decode('utf-8')
        parser = BeautifulSoup(website, "html.parser")
        # technical information json
        information = {}
        # part number
        information["part"] = parser.find("span", attrs={"itemprop":"sku"}).find("b").text.strip()
        information["name"] = parser.find("h1", attrs={"itemprop":"name"}).text.strip()
        information["url"] = parser.find("meta", attrs={"itemprop":"url"}).get("content").strip()
        # parse availability
        information["availability"] = parser.find("link", attrs={"itemprop":"availability"}).get("href").split("/")[-1].strip()
        # parse price
        information["price"] = {}
        information["price"]["currency"] = parser.find("meta", itemprop="priceCurrency").get("content").strip()
        information["price"]["1"] = float(parser.find("meta", itemprop="price").get("content").strip())
        information["price"]["10"] = None
        information["price"]["100"] = None
        information["price"]["1000"] = None
        # check if there are discounts
        price_elements = parser.find_all('p', class_='productPrice right')
        prices = [float(elem.get_text(strip=True).replace('€', '')) for elem in price_elements]
        for i, price in enumerate(prices):
            information["price"][str(10**i)] = price
        # datasheets
        information["datasheets"] = []
        for datasheet_div in parser.find_all("div", attrs={"class": "articleDatasheet"}):
            information["datasheets"].append(datasheet_div.find("a").get("href"))
        # part information
        information["data"] = {}
        data_html = parser.find_all("ul", attrs={"class":"articleTechnicalData"})
        for data_category_html in data_html:
            headline = data_category_html.find("li", "articleTechnicalHeadline").text.strip()
            information["data"][headline] = {}
            for data_attribute_html in data_category_html.find_all("ul", "articleAttribute"):
                data_lis = data_attribute_html.find_all("li")
                for i in range(0, len(data_lis), 2):
                    # get attribute name and value
                    name = data_lis[i].text.strip()
                    value = data_lis[i+1].text.strip()
                    information["data"][headline][name] = value
        # categories
        information["categories"] = []
        for category_html in parser.find_all("ol", "breadcrumb"):
            for category in category_html.find_all("span", itemprop="name"):
                information["categories"].append(category.contents[0].strip())
        # return technical information
        return information
    

    def get_datasheet(self, url: str, filename: str) -> None:
        """
        Download and save a datasheet from a given URL.

        Args:
            url (str): URL of the datasheet.
            filename (str): Local filename to save the datasheet.
        """
        data = requests.get(url, headers=self.req_headers).content
        f = open(filename, "wb")
        f.write(data)
        f.close()
    

    def search_part(self, part: str) -> dict:
        """
        Search for a specific part number and retrieve full information if found.

        Args:
            part (str): The part number to search for.

        Returns:
            dict: A dictionary with full product details if the part is found, else None.
        """
        results = self.get_search_results(part)
        for result in results:
            if part.upper() == result["part"].upper():
                # found right entry
                result.update( self.get_part_information(result["url"]) )
                return result
        return None
                

# stand alone
if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: ./reichelt.py \"Part Name\" optional_attribute")
        print("The optional attribute can be any key of the jobject returned by the search_part function. Otherwise the whole object is returned.")
        exit(1)
    
    def find_key_recursively(d, target_key):
        if isinstance(d, dict):
            for key, value in d.items():
                if key == target_key:
                    return value
                result = find_key_recursively(value, target_key)
                if result is not None:
                    return result
        elif isinstance(d, list):
            for item in d:
                result = find_key_recursively(item, target_key)
                if result is not None:
                    return result
        return None
    
    app = Reichelt()
    # search for part
    result = app.search_part(sys.argv[1])
    if result is None:
        print("Part not found")
        exit(1)
    # check if there is an optional attribute
    if len(sys.argv) == 2:
        print(json.dumps(result, indent=2))
    else:
        value = find_key_recursively(result, sys.argv[2])
        # check type
        if value is None:
            print(f"Key \"{sys.argv[2]}\" not found.")
            exit(1)
        elif isinstance(value, list):
            for item in value:
                print(item)
        elif isinstance(value, dict):
            for key, item in value.items():
                print(f"{key}:{item}")
        else:
            print(value)
    exit(0)
