"""Simple requests demo"""
import requests
import re

request_url = 'https://peabody.jhu.edu/events/photo/page/1/'

result = requests.get(request_url).text

result_single_line = ' '.join(result.splitlines())

resultlines = result.splitlines()
#print(result)

## find and report
#for thisline in resultlines:
#  branch = re.search(r"((<article).*)",thisline)
#  if branch:
#    print(branch.group(1))

# find and report
list_of_matching_strings = re.findall(r"(<article.*?</article>)",result_single_line)

for result in list_of_matching_strings:
  #print(result)
  #print('***************************************************')
  list_of_links = re.findall(r"href=\"(.*?)\"",result)
  single_link = re.search(r"href=\"(.*?)\"",result)
  #print(list_of_links)
  subsite_url = single_link.group(1)
  print(subsite_url)
  subsite_result = requests.get(subsite_url).text
  print("HHHHHHHHHHHHHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
  #print(subsite_result)
  subsite_result_single_line = ' '.join(subsite_result.splitlines())
  #<div class="tribe-events-single-event-description
  single_match = re.search(r"<div\s+class=\"tribe-events-single-event-description[^>]*>(.*?)</div>",subsite_result_single_line)
  print(single_match.group(1))
