"""Demo to read in json file"""
import json
import re

with open('all_events.json','r',encoding='utf-8') as myjsonfile:
  json_list = json.load(myjsonfile)

#print(json_hash)

def get_all_date(thisdate):
  for thisevent in json_list:
    thisfulldatetime = thisevent['fulldatetime']
    event_date_match = re.search(thisdate,thisfulldatetime)
    if event_date_match:
      print(thisevent)

def get_all_location(thislocation):
  for thisevent in json_list:
    thiscanonloc = thisevent['canonical_location']
    event_loc_match = re.search(thislocation,thiscanonloc)
    if event_loc_match:
      print(thisevent)

#thislocation = r"Ottobar"
thislocation = r"Peabody Heights|No Land Beyond"
thislocation = r""

get_all_location(thislocation)


#thisdate = r"2025-07-05"
#get_all_date(thisdate)
