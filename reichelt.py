#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup


class Reichelt:
	def __init__(self):
		pass
	

	def get_search_results(self, keyword):
		# download search results as raw html
		link = "https://www.reichelt.de/index.html?ACTION=446&LA=0&nbc=1&q=%s" % keyword.lower().replace(" ", "%20")
		website = urllib.request.urlopen(link).read().decode('utf-8')
		parser = BeautifulSoup(website, 'html.parser')
		# get every part in the search result list. Each part is in a div named "al_gallery_article".
		parts=[]
		for part_html in parser.find_all("div", "al_gallery_article"):
			# create json object for each part
			part={"part":"", "name":"", "link":"", "1":None, "10":None, "100":None, "1000":None}
			# get link html tag to part
			part_link = part_html.find("a", "al_artinfo_link")
			# extract data
			part["part"] = part_link.contents[0].strip().replace("Artikel-Nr.: ","") # part number
			part["name"] = part_link.contents[2].strip() # part name
			part["link"] = part_link.get("href") # href
			# find price if there is one
			if(part_html.find("span", "itemprop")):
				part["1"] = float(part_html.find("span", "itemprop").next_element.replace(",",".")) # price
			# find discounts. Price for 10, 100, 1000 peaces are added to the array
			if(part_html.find("ul", "discounts") ):
				# get every price from discount table
				discounts = part_html.find("ul", "discounts").find_all("li")
				for i in range(len(discounts)):
					part[str(10**(i+1))] = float(discounts[i].find_all("span")[0].contents[0].replace("€","").replace(",","."))
			# add part to list
			parts.append(part)
		# return part list
		return parts
	

	def get_part_information(self, link):
		# download website
		website = urllib.request.urlopen(link).read().decode()
		parser = BeautifulSoup(website, "html.parser")
		# technical information json
		information = {}
		# datasheet
		information["datasheet"] = None
		if parser.find("div", "av_datasheet"):
			information["datasheet"] = "https://www.reichelt.de"+parser.find("div", "av_datasheet").a.get("href")
		# parse information from html
		information_html = parser.find("div", "av_props_inline")
		for section_html in information_html.find_all("ul", "av_propview"):
			section_name = section_html.find("li", "av_propview_headline").contents[0].strip()
			sections = {}
			for info in section_html.find_all("ul", "clearfix"):
				sections[ info.find("li", "av_propname").contents[0].strip() ] =  info.find("li", "av_propvalue").contents[0].strip()
			information[section_name] = sections
		# parse categories
		categories = []
		category_html = parser.find("ol", "breadcrumb")
		for category in category_html.find_all("span", itemprop="name"):
			categories.append( category.contents[0].strip() )
		information["categories"] = categories
		# return technical information
		return information
	

	def get_datasheet(self, link, filename):
		data = urllib.request.urlopen(link).read()
		f = open(filename, "wb")
		f.write(data)
		f.close()
	

	def search_part(self, part):
		results = self.get_search_results(part)
		for result in results:
			if result["part"] == part:
				# found right entry
				result.update( self.get_part_information(result["link"]) )
				return result
				

