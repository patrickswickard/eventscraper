"""Simple requests demo"""
import requests
import re
from datetime import datetime

request_url1 = 'https://peabody.jhu.edu/events/photo/page/1/'
request_url2 = 'https://peabody.jhu.edu/events/photo/page/2/'
request_url3 = 'https://peabody.jhu.edu/events/photo/page/3/'
request_url4 = 'https://baltshowplace.tumblr.com/'

def parse_event_datetime(event_date_text,event_time_text):
  if event_time_text:
    fulldatetext = event_date_text + ' ' + event_time_text
    if ':' in event_time_text:
      fulldatetime = datetime.strptime(fulldatetext, '%A, %B %d, %Y %I:%M%p')
    else:
      fulldatetime = datetime.strptime(fulldatetext, '%A, %B %d, %Y %I%p')
  else:
    fulldatetime = datetime.strptime(event_date_text, '%A, %B %d, %Y')
  return fulldatetime

def scrape_page_showspace(request_url):

  showspace_location_dict = {
    '2410 Erdman Ave':'UNKNOWN',
    '32nd St &amp; Brentwood':'UNKNOWN',
    '4001 Harford Rd':'UNKNOWN',
    '6007 Pinehurst Rd':'UNKNOWN',
    '8x10':'UNKNOWN',
    'An Die Musik':'UNKNOWN',
    'Area 405':'UNKNOWN',
    'BSO':'UNKNOWN',
    'Barcocina':'UNKNOWN',
    'Black Cherry Puppet Theater':'UNKNOWN',
    'Bliss Meadows (5105 Plainfield Avenue)':'UNKNOWN',
    'Bliss Meadows (5105 Plainfield Ave)':'UNKNOWN',
    'Bloom’s':'UNKNOWN',
    'Bogus Gallery (1511 Guilford Ave)':'UNKNOWN',
    'Book Thing':'UNKNOWN',
    'CFG Arena':'UNKNOWN',
    'Canton Waterfront Park':'UNKNOWN',
    'Caroll Skatepark':'UNKNOWN',
    'Central Library (400 Cathedral St)':'UNKNOWN',
    'Charles St':'UNKNOWN',
    'Checkerspot Brewing':'UNKNOWN',
    'Club 603':'UNKNOWN',
    'Club Car':'UNKNOWN',
    'Creative Alliance':'UNKNOWN',
    'Cult Classic Brewing':'UNKNOWN',
    'Current Space':'UNKNOWN',
    'Cylburn Arboretum':'UNKNOWN',
    'DM bands for address':'UNKNOWN',
    'DM inmysoulzine for address':'UNKNOWN',
    'Druid Hill Park':'UNKNOWN',
    'Ema’s Corner':'UNKNOWN',
    'Ema’s Corner (33 W North Ave)':'UNKNOWN',
    'Hippodrome':'UNKNOWN',
    'Holy Frijoles':'UNKNOWN',
    'House of Chiefs':'UNKNOWN',
    'Keystone Korner':'UNKNOWN',
    'Le Mondo':'UNKNOWN',
    'Lith Hall':'UNKNOWN',
    'Lwnsphere (4518 Raspe Ave)':'UNKNOWN',
    'Mercury Theatre':'UNKNOWN',
    'Metro':'UNKNOWN',
    'Mobtown Ballroom':'UNKNOWN',
    'Monument City Brewing':'UNKNOWN',
    'Morsbergers':'UNKNOWN',
    'Mosaic':'UNKNOWN',
    'Motor House':'UNKNOWN',
    'Normals Books':'UNKNOWN',
    'Old Major':'UNKNOWN',
    'Orion Studios':'UNKNOWN',
    'Ottobar':'UNKNOWN',
    'Ottobar Upstairs':'UNKNOWN',
    'Patterson Park':'UNKNOWN',
    'Peabody Heights':'UNKNOWN',
    'Pier Six':'UNKNOWN',
    'Powerplant':'UNKNOWN',
    'Red Emma’s':'UNKNOWN',
    'Reverb':'UNKNOWN',
    'Roland Water Tower':'UNKNOWN',
    'Shamrock Inn':'UNKNOWN',
    'Skate Park of Baltimore':'UNKNOWN',
    'Soundstage':'UNKNOWN',
    'Station North':'UNKNOWN',
    'Stem &amp; Vine':'UNKNOWN',
    'The Bluebird':'UNKNOWN',
    'The Compound':'UNKNOWN',
    'The Depot':'UNKNOWN',
    'The Forest (DM ___by_my_reanimated_corpse for address)':'UNKNOWN',
    'The Forest (DM bands for address)':'UNKNOWN',
    'The Hargrove':'UNKNOWN',
    'The Lyric':'UNKNOWN',
    'The Manor':'UNKNOWN',
    'The Recher':'UNKNOWN',
    'The Undercroft':'UNKNOWN',
    'The Vortex at CAA Park':'UNKNOWN',
    'The Voxel':'UNKNOWN',
    'The Wine Collective':'UNKNOWN',
    'True Vine':'UNKNOWN',
    'Union Craft Brewing':'UNKNOWN',
    'Warehouse Cinema Rotunda':'UNKNOWN',
    'Watermelon Room (DM bands for address)':'UNKNOWN',
    'Waverly Brewing Company':'UNKNOWN',
    'Waverly United Methodist':'UNKNOWN',
    'Wax Atlas':'UNKNOWN',
    'Wiggle Room (3000 Falls Rd)':'UNKNOWN',
    'Zen West':'UNKNOWN',
  }
  location_set = set()
  firstpage = requests.get(request_url).text

  firstpage_single_line = ' '.join(firstpage.splitlines())

  firstpagelines = firstpage.splitlines()

# find and report
  list_of_matching_months = re.findall(r"(\s*<section\s+class=\"post\">.*?</div>)",firstpage_single_line)
  first_matching_month = list_of_matching_months[0]

  for thismonth in [first_matching_month]:
    list_of_links = re.findall(r"href=\"(.*?)\"",thismonth)
    single_link = re.search(r"href=\"(.*?)\"",thismonth)
    thismonth_url = single_link.group(1)
    print(thismonth_url)
    # clicking through to current month's results
    thismonth_result = requests.get(thismonth_url).text
    list_of_matching_strings = re.findall(r"(\s*</figure>\s*</div>\s*</div>\s*<p>.*?<section\s+class=\"inline-meta post-extra\">)",firstpage_single_line)

    thismonth_result_single_line = ' '.join(thismonth_result.splitlines())
    daylist = re.split(r"<p><br></p>",thismonth_result_single_line)
    for thisday in daylist:
      event_date_match = re.search(r"<h2>(.*?)</h2>",thisday)
      event_date_text = event_date_match.group(1)
      list_of_events = re.findall(r"(<p>\s*\w.*?</p>)",thisday)
      for event in list_of_events:
        print('HERE IS AN EVENT')
        event_title_match = re.search(r"<p>(.*?)</p>",event)
        event_title_text = event_title_match.group(1)
        print(event_title_text)

        event_url_match = 'FIXME'
        event_url_text = thismonth_url
        print(event_url_text)

        print(event_date_text)

        event_time_match = re.search(r"<p>.*?\.\s+(\d.*?(?:AM|PM))\s*[,.@&-]",event)
        if event_time_match:
          event_time_text = event_time_match.group(1)
          fulldatetime = 'hi'
          fulldatetime = parse_event_datetime(event_date_text,event_time_text)
          print(fulldatetime)

        event_location_match = re.search(r"@\s+(.*?)\s*</p>",event)
        if event_location_match:
          event_location_text = event_location_match.group(1)
          if event_location_text:
            print(event_location_text)
            location_set.add(event_location_text)

        event_street_address_match = "ERROR"
        if event_location_text:
          event_street_address_text = showspace_location_dict[event_location_text]
          print('ERROR')

        event_cost_match = re.search(r"<p>.*?\.\s+\w.*?(?:AM|PM)\s*[,.@&-]\s+(.*?)\s+@",event)
        if event_cost_match:
          event_cost_text = event_cost_match.group(1)
          print(event_cost_text)
        else:
          print("DUNNO")

        event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",thismonth_result_single_line)
        if event_description_match:
          event_description_text = event_description_match.group(1)
          print(event_description_text)
        else:
          print("NONE")
  print(location_set)
  location_list = list(location_set)
  location_list.sort()
  print(location_list)

def scrape_page_peabody(request_url):
  result = requests.get(request_url).text

  result_single_line = ' '.join(result.splitlines())

  resultlines = result.splitlines()

  # find and report
  list_of_matching_strings = re.findall(r"(<article.*?</article>)",result_single_line)

  for result in list_of_matching_strings:
    list_of_links = re.findall(r"href=\"(.*?)\"",result)
    single_link = re.search(r"href=\"(.*?)\"",result)
    subsite_url = single_link.group(1)
    subsite_result = requests.get(subsite_url).text
    print()
    print("*****************************************************")
    print()
    #print(subsite_result)
    subsite_result_single_line = ' '.join(subsite_result.splitlines())
    event_title_match = re.search(r"<h1\s+class=\"tribe-events-single-event-title[^>]*>(.*?)</h1>",subsite_result_single_line)
    event_title_text = event_title_match.group(1)
    print(event_title_text)

    event_url_match = 'FIXME'
    event_url_text = subsite_url
    print(event_url_text)

    event_date_match = re.search(r"<div\s+class=\"tse-date-details\">\s*(.*?)</div>",subsite_result_single_line)
    event_date_text = event_date_match.group(1)
    event_date_text = re.sub(r"\s+"," ",event_date_text)
    print(event_date_text)

    event_time_match = re.search(r"<div\s+class=\"tribe-events-abbr\s+tribe-events-start-time[^>]*>\s*(.*?)</div>",subsite_result_single_line)
    event_time_text = event_time_match.group(1)
    print(event_time_text)

    event_location_match = re.search(r"<div\s+class=\"tribe-venue\">\s*(.*?)</div>",subsite_result_single_line)
    event_location_text = event_location_match.group(1)
    print(event_location_text)

    event_cost_match = re.search(r"<div\s+class=\"tribe-events-event-cost\">\s*(.*?)</div>",subsite_result_single_line)
    event_cost_text = event_cost_match.group(1)
    print(event_cost_text)

    #event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",subsite_result_single_line)
    #event_description_text = event_description_match.group(1)
    #print(event_description_text)

#scrape_page_peabody(request_url1)
#scrape_page_peabody(request_url2)
#scrape_page_peabody(request_url3)
scrape_page_showspace(request_url4)
