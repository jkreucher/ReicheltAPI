#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import reichelt
import json

part = "74HC 00"

# create API object
api = reichelt.Reichelt()
result = api.search_part(part)

# print info
print(json.dumps(result, indent=2, ensure_ascii=False))

# download datasheet
api.get_datasheet(result["datasheets"][0], part+".pdf")
