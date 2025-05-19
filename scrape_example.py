"""Simple requests demo"""
import requests
import re

request_url1 = 'https://peabody.jhu.edu/events/photo/page/1/'
request_url2 = 'https://peabody.jhu.edu/events/photo/page/2/'
request_url3 = 'https://peabody.jhu.edu/events/photo/page/3/'
request_url4 = 'https://baltshowplace.tumblr.com/'

def scrape_page_showspace(request_url):
  result = requests.get(request_url).text

  result_single_line = ' '.join(result.splitlines())

  resultlines = result.splitlines()

  print(result_single_line)
# find and report
  list_of_matching_strings = re.findall(r"(\s*<section\s+class=\"post\">.*?</div>)",result_single_line)

  print(list_of_matching_strings)

  for result in list_of_matching_strings:
    list_of_links = re.findall(r"href=\"(.*?)\"",result)
    single_link = re.search(r"href=\"(.*?)\"",result)
    subsite_url = single_link.group(1)
    print(subsite_url)
    subsite_result = requests.get(subsite_url).text
    list_of_matching_strings = re.findall(r"(\s*</figure>\s*</div>\s*</div>\s*<p>.*?<section\s+class=\"inline-meta post-extra\">)",result_single_line)

    #print(single_link)
    #print('**************************************')
    #print(subsite_result)
    #print(list_of_matching_strings)
    print()
    print("*****************************************************")
    print()
    #print(subsite_result)
    subsite_result_single_line = ' '.join(subsite_result.splitlines())
    list_of_events = re.findall(r"(<p>\s*\w.*?</p>)",subsite_result_single_line)
    for event in list_of_events:

      print('HERE IS AN EVENT')
      event_title_match = re.search(r"<p>(.*?)</p>",event)
      event_title_text = event_title_match.group(1)
      print(event_title_text)

      event_url_match = 'FIXME'
      event_url_text = subsite_url
      print(event_url_text)

      #event_date_match = re.search(r"<div\s+class=\"tse-date-details\">\s*(.*?)</div>",subsite_result_single_line)
      #event_date_match = re.search(r"<div\s+class=\"tse-date-details\">\s*(.*?)</div>",subsite_result_single_line)
      #event_date_text = event_date_match.group(1)
      #event_date_text = re.sub(r"\s+"," ",event_date_text)
      event_date_text = "THISDAY"
      print(event_date_text)

      print(event)
      event_time_match = re.search(r"<p>.*?\.\s+(\w.*?(?:AM|PM))\s*[,.@]",event)
      if event_time_match:
        event_time_text = event_time_match.group(1)
        if event_time_text:
          print(event_time_text)

      event_location_match = re.search(r"@\s+(.*)",event)
      if event_location_match:
        event_location_text = event_location_match.group(1)
        if event_location_text:
          print(event_location_text)

      #event_cost_match = re.search(r"<p>.*?\.\s+\w.*?(?:AM|PM)\s*[,.@]\s+(.*?)\s+@",event)
      #event_cost_text = event_cost_match.group(1)
      #if event_cost_text:
      #  print(event_cost_text)
      #else:
      #  print("DUNNO")

      #event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",subsite_result_single_line)
      #event_description_text = event_description_match.group(1)
      event_description_text = "NONE"
      print(event_description_text)

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
