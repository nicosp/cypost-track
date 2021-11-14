import json
import re
import sys
import urllib.request
from parser import HTMLTableParser
from dateutil.parser import parse

target = 'https://ips.cypruspost.gov.cy/ipswebtrack/IPSWeb_item_events.aspx?itemid=' + sys.argv[1]

def key(n):
  key = n.split('/')[0].replace('&', '').strip()
  return re.sub('\s+', '_', key.lower())

#
# Convert status
# Date to ISO and remove empty fields
#
def convertStatus(s):
  if 'date_time' in s:
      s['date_time'] = parse(s['date_time'], dayfirst=True).isoformat()
  return {k: v for k, v in s.items() if v != ''}

# get website content
req = urllib.request.Request(url=target)
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')

# instantiate the parser and feed it
p = HTMLTableParser()
p.feed(xhtml)

table = p.tables[0]
table.pop(0)

columns = table.pop(0)
keys = list(map(key, columns))

statusList = []
for item in table:
  status = dict(zip(keys, item))
  if status:
    statusList.append(convertStatus(status))

print(json.dumps(statusList, ensure_ascii=False))
