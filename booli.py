import sys

if sys.version_info[0] > 2:
    import http.client as http
else:
    import httplib as http

import time
from hashlib import sha1
import random
import string
import json

def callbooliapi(limit, query, offset, api_key):
  callerId = "williambengtsson"
  timestamp = str(int(time.time()))
  unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
  s = callerId+timestamp+api_key+unique
  hashstr = sha1(s.encode('utf-8')).hexdigest()
  
  url = "/sold?q="+query+"&limit="+str(limit)+"&offset="+str(offset)+"&callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr

  connection = http.HTTPConnection("api.booli.se")
  connection.request("GET", url)
  response = connection.getresponse()
  data = response.read()
  connection.close() 

  if response.status != 200:
    print("fail")

  return data

def main():
  limit = 1000
  api_key = sys.argv[1]
  query = sys.argv[2]
  offset = 0
  
  output = json.loads(callbooliapi(limit, query, offset, api_key))

  totalCount = output["totalCount"]
  print("totalCount = "+str(totalCount))

  noRequests = totalCount // limit + 1

  outfile = open('data_booli_'+query+'.json', 'w')

  for i in range(1, noRequests): 
    offset = i * limit
    parsed = json.loads(callbooliapi(limit, query, offset, api_key))
    count = parsed["count"]
    for j in range(0, count):
      newItem = parsed["sold"][j]
      output["sold"].append(newItem)

    output["count"] = totalCount

    output.pop('totalCount', None)
    output.pop('limit', None)
    output.pop('offset', None)

    json.dump(output, outfile, indent=4)

  outfile.close()

if __name__ == "__main__":
  main()
