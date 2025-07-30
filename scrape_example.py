"""Simple requests demo"""
import requests
import re
from datetime import datetime
import json
import venue_data

request_url1 = 'https://peabody.jhu.edu/events/photo/page/1/'
request_url2 = 'https://peabody.jhu.edu/events/photo/page/2/'
request_url3 = 'https://peabody.jhu.edu/events/photo/page/3/'
#request_url4 = 'https://baltshowplace.tumblr.com/'

all_events = []

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

def adjust_full_month_text(thismonth_result):
  thismonth_result_single_line = ' '.join(thismonth_result.splitlines())
  thismonth_result_single_line = re.sub(r"<h2><b><i>\*\*\*PLEASE CHECK VENUE WEBSITES OR FACEBOOK PAGES FOR INFO ON WHETHER SHOWS HAVE BEEN CANCELLED\*\*\*</i></b></h2>","",thismonth_result_single_line)
  return thismonth_result_single_line

def get_daylist(thismonth_result_single_line):
  if re.search(r"<h2>\s*JANUARY\s+2022\s*</h2>",thismonth_result_single_line):
    thismonth_result_single_line = re.sub(r"</p><h2>","</p></q><h2>",thismonth_result_single_line)
    daylist = re.findall(r"(<h2>(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday).*?</q>)",thismonth_result_single_line)
  else:
    daylist = re.split(r"<p><br\s*\/?></p>",thismonth_result_single_line)
  return daylist

def adjust_thisday(thisday):
  thisday = re.sub(r"<br /><br />","</p>",thisday)
  thisday = re.sub(r"March 5, 2022<br />","March 5, 2022",thisday)
  thisday = re.sub(r"February 1, 2022<br />","February 1, 2022",thisday)
  thisday = re.sub(r"December 24, 2021<br />","December 24, 2021",thisday)
  thisday = re.sub(r"December 29, 2021<br />","December 29, 2021",thisday)
  thisday = re.sub(r"August 1, 2021<br />","August 1, 2021",thisday)
  thisday = re.sub(r"December 1, 2019<br />","December 1, 2019",thisday)
  thisday = re.sub(r"January 2, 2020<br />","Thursday, January 2, 2020",thisday)
  thisday = re.sub(r"July 28, 2019</p>","July 28, 2019",thisday)
  thisday = re.sub(r"<h2>JANUARY 2022</h2><h2>Saturday, January 1, 2022</h2>","<h2>Saturday, January 1, 2022</h2>",thisday)
  return thisday

def adjust_event_date_text(event_date_text):
  event_date_text = re.sub(r"2023<br\s+\/>","2023",event_date_text)
  return event_date_text

def adjust_event(event):
  event = re.sub(r"\@ \+ Jiffy","+ Jiffy",event)
  event = re.sub(r"Meet Me @ The Altar","Meet Me at The Altar",event)
  event = re.sub(r"\s*<br\s*/>","",event)
  event = re.sub(r"&rsquo;","’",event)
  event = re.sub(r"</strike>","",event)
  return event

def adjust_event_time_text(event_time_text):
  event_time_text = re.sub(r"\b15PM","5PM",event_time_text)
  event_time_text = re.sub(r"\b20PM","8PM",event_time_text)
  event_time_text = re.sub(r"\b22PM","10PM",event_time_text)
  event_time_text = re.sub(r"\b3PMPM","3PM",event_time_text)
  event_time_text = re.sub(r"\b7 PM","7PM",event_time_text)
  event_time_text = re.sub(r"\b8 PM","8PM",event_time_text)
  event_time_text = re.sub(r"\b9 PM","9PM",event_time_text)
  event_time_text = re.sub(r"\b10 PM","10PM",event_time_text)
  return event_time_text

def scrape_month_showspace(request_url):
  location_set = set()
  thismonth_url = request_url
  #print(thismonth_url)
  # clicking through to current month's results
  thismonth_result = requests.get(thismonth_url).text
  thismonth_result_single_line = adjust_full_month_text(thismonth_result)
  daylist = get_daylist(thismonth_result_single_line)
  #print('list of days')
  #print(len(daylist))
  for thisday in daylist:
    thisday = adjust_thisday(thisday)
    event_date_match = re.search(r"<h2>(.*?)</h2>",thisday)
    if event_date_match:
      event_date_text = event_date_match.group(1)
      event_date_text = adjust_event_date_text(event_date_text)
      #event_date_text = re.sub(r"2023<br\s+\/>","2023",event_date_text)
      list_of_events = re.findall(r"(<p>\s*\w.*?(?:</p>))",thisday)
      for event in list_of_events:
        print('HERE IS AN EVENT')
        event = adjust_event(event)
        event_title_match = re.search(r"<p>(.*?)</p>",event)
        event_title_text = event_title_match.group(1)
        print(event_title_text)

        event_url_match = 'FIXME'
        event_url_text = thismonth_url
        print(event_url_text)

        print(event_date_text)

        event_time_text = 'NONE'
        fulldatetime = 'NONE'
        event_time_match = re.search(r"<p>.*?\.\s+(\d+\D*(?:AM|PM))\s*[,.@&-]",event)
        if event_time_match:
          event_time_text = event_time_match.group(1)
          print(event_time_text)
          event_time_text = adjust_event_time_text(event_time_text)
          print(event_time_text)
          fulldatetime = parse_event_datetime(event_date_text,event_time_text)
          print(fulldatetime)

        event_location_match = re.search(r"@\s+(.*?)\s*</p>",event)
        if event_location_match:
          event_location_text = event_location_match.group(1)
          if event_location_text:
            print(event_location_text)
            location_set.add(event_location_text)

        canonical_location_text = venue_data.all_venue_dict[event_location_text]
        print(canonical_location_text)

        event_street_address_text = "ERROR"
        event_street_coords_text = "ERROR"
        if event_location_text:
          event_street_address_text = venue_data.showspace_location_dict[event_location_text]
          event_coords_text = venue_data.showspace_location_coords[event_location_text]
          print(event_street_address_text)
          print(event_coords_text)

        event_cost_text = 'UNKNOWN'
        event_cost_match = re.search(r"<p>.*?\.\s+\w.*?(?:AM|PM)\s*[,.@&-]\s+(.*?)\s+@",event)
        if event_cost_match:
          event_cost_text = event_cost_match.group(1)
          print(event_cost_text)
        else:
          print(event_cost_text)

        event_description_text = 'NONE'
        event_description_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>\s*(.*?)</div>",thismonth_result_single_line)
        if event_description_match:
          event_description_text = event_description_match.group(1)
          print(event_description_text)
        else:
          print(event_description_text)

        thisevent = {}
        thisevent['title'] = event_title_text
        thisevent['url'] = event_url_text
        thisevent['date'] = event_date_text 
        thisevent['time'] = event_time_text
        thisevent['fulldatetime'] = str(fulldatetime)
        thisevent['location'] = event_location_text
        thisevent['canonical_location'] = canonical_location_text
        thisevent['street_address'] = event_street_address_text
        thisevent['coords'] = event_coords_text
        thisevent['cost'] = event_cost_text
        thisevent['description'] = event_description_text
        all_events.append(thisevent)

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

monthlisthere = [
  'https://baltshowplace.tumblr.com/post/790277781632237568/monday-august-4-2025-adjective-animal-colatura',
  'https://baltshowplace.tumblr.com/post/787474960748855296/july-2025',
  'https://baltshowplace.tumblr.com/post/784976508140814336/june-2025',
  'https://baltshowplace.tumblr.com/post/782020357674631168/may-2025',
  'https://baltshowplace.tumblr.com/post/779133136197074944/april-2025',
  'https://baltshowplace.tumblr.com/post/776414637419790336/saturday-march-1-2025',
  'https://baltshowplace.tumblr.com/post/773975117554384896/february-2025',
  'https://baltshowplace.tumblr.com/post/770972544848297984/january-2025',
  'https://baltshowplace.tumblr.com/post/768449088238895104/december-2024',
  'https://baltshowplace.tumblr.com/post/765527326372102144/november-2024',
  'https://baltshowplace.tumblr.com/post/762743700027834368/october-2024',
  'https://baltshowplace.tumblr.com/post/760202712078008320/september-2024',
  'https://baltshowplace.tumblr.com/post/756932438274588672/august-2024',
  'https://baltshowplace.tumblr.com/post/754400753730420736/july-2024',
  'https://baltshowplace.tumblr.com/post/751599042382954496/june-2024',
  'https://baltshowplace.tumblr.com/post/748699033203245056/may-2024',
  'https://baltshowplace.tumblr.com/post/746071191901667328/april-2024',
  'https://baltshowplace.tumblr.com/post/742995647288999936/march-2024',
  'https://baltshowplace.tumblr.com/post/740598285591527424/february-2024',
  'https://baltshowplace.tumblr.com/post/738051898274430976/january-2024',
  'https://baltshowplace.tumblr.com/post/734896694276276224/december-2023',
  'https://baltshowplace.tumblr.com/post/732115473125244928/november-2023',
  'https://baltshowplace.tumblr.com/post/729295254033989632/october-2023',
  'https://baltshowplace.tumblr.com/post/727137330486509569/september-2023',
  'https://baltshowplace.tumblr.com/post/723875701736013824/august-2023',
  'https://baltshowplace.tumblr.com/post/721226733690535936/july-2023',
  'https://baltshowplace.tumblr.com/post/718170190266974208/june-2023',
  'https://baltshowplace.tumblr.com/post/715529145102254080/may-2023',
  'https://baltshowplace.tumblr.com/post/712533186762113024/april-2023',
  'https://baltshowplace.tumblr.com/post/710109247541805056/march-2023',
  'https://baltshowplace.tumblr.com/post/707300923405467648/february-2023',
  'https://baltshowplace.tumblr.com/post/704765880227217408/january-2023',
  'https://baltshowplace.tumblr.com/post/701745406283022336/december-2022',
  'https://baltshowplace.tumblr.com/post/699230592118800385/november-2022',
  'https://baltshowplace.tumblr.com/post/696605191759413248/october-2022',
  'https://baltshowplace.tumblr.com/post/693434961899995136/september-2022',
  'https://baltshowplace.tumblr.com/post/690893366167306240/august-2022',
  'https://baltshowplace.tumblr.com/post/687626976553582592/july-2022',
  'https://baltshowplace.tumblr.com/post/685102368717701120/june-2022',
  'https://baltshowplace.tumblr.com/post/682654766641414144/may-2022',
  'https://baltshowplace.tumblr.com/post/680026459916599296/april-2022',
  'https://baltshowplace.tumblr.com/post/677037663343214592/march-2022',
  'https://baltshowplace.tumblr.com/post/674595075474571264/february-2022',
  'https://baltshowplace.tumblr.com/post/672057481921511424/january-2022-saturday-january-1-2022-baltimore',
  'https://baltshowplace.tumblr.com/post/668688297732816896/december-2021',
  'https://baltshowplace.tumblr.com/post/666346617298960384/november-2021',
  'https://baltshowplace.tumblr.com/post/663532031553224704/october-2021',
  'https://baltshowplace.tumblr.com/post/660549586203688961/september-2021',
  'https://baltshowplace.tumblr.com/post/657825359778267136/august-2021',
  'https://baltshowplace.tumblr.com/post/654738260727300096/july-2021-shows',
  'https://baltshowplace.tumblr.com/post/652207470830305280/june-2021-shows',
  'https://baltshowplace.tumblr.com/post/610908522479304704/march-2020-shows',
  'https://baltshowplace.tumblr.com/post/190542555134/february-2020-shows',
  'https://baltshowplace.tumblr.com/post/189893120099/january-2020-shows',
  'https://baltshowplace.tumblr.com/post/189344777799/december-2019-shows',
  'https://baltshowplace.tumblr.com/post/188691571144/november-2019-shows',
  'https://baltshowplace.tumblr.com/post/187973398609/october-2019-shows',
  'https://baltshowplace.tumblr.com/post/187337947144/september-2019-shows',
  'https://baltshowplace.tumblr.com/post/186641957054/august-2019-shows',
  'https://baltshowplace.tumblr.com/post/185898529844/july-2019-shows',
  'https://baltshowplace.tumblr.com/post/185260482249/june-2019-shows',
]
#thismonth_url = monthlisthere[21]
for thismonth in monthlisthere:
  thismonth_url = thismonth
  scrape_month_showspace(thismonth_url)

all_events_json = json.dumps(all_events)


with open('all_events.json', 'w') as f:
  print(all_events_json, file=f)
