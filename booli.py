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

def booli_api():
  limit = 1000
  print("Enter api-key:")
  api_key = input()
  print("\nEnter query (e.g. 'birkastan' or '98530'):")
  query = input()
  output_file = 'download/data_booli_'+query+'.json'
  offset = 0
  
  output = json.loads(callbooliapi(limit, query, offset, api_key))

  if 'message' in output:
    print("\nMessage: "+output["message"])
    return

  totalCount = output["totalCount"]
  print("\nTotal number of reccords: "+str(totalCount)+"\n")

  noRequests = totalCount // limit + 1

  outfile = open(output_file, 'w')
  json.dump(output, outfile, indent=4)

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

    with open(output_file, 'w') as outfile:
      json.dump(output, outfile, indent=4)

  outfile.close()
  return output_file

if __name__ == "__main__":
  booli_api()
