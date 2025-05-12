"""Simple requests demo"""
import requests
import re

request_url1 = 'https://peabody.jhu.edu/events/photo/page/1/'
request_url2 = 'https://peabody.jhu.edu/events/photo/page/2/'
request_url3 = 'https://peabody.jhu.edu/events/photo/page/3/'

def scrape_page(request_url):
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

    event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",subsite_result_single_line)
    event_description_text = event_description_match.group(1)
    print(event_description_text)

scrape_page(request_url1)
scrape_page(request_url2)
scrape_page(request_url3)
