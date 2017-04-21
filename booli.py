# import http.client #python 3
import httplib # python 2
import time
from hashlib import sha1
import random
import string
import json

def callbooliapi(limit, query, offset):
  callerId = "williambengtsson"
  timestamp = str(int(time.time()))
  unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
  s = callerId+timestamp+"1B8yJRDjHUQwND92jnQ3awLOCaj6NxFfi3HInjN4"+unique
  hashstr = sha1(s.encode('utf-8')).hexdigest()
  
  url = "/sold?q="+query+"&limit="+str(limit)+"&offset="+str(offset)+"&callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr
  
  # connection = http.client.HTTPConnection("api.booli.se") #python 3
  connection = httplib.HTTPConnection("api.booli.se") #python 2
  connection.request("GET", url)
  response = connection.getresponse()
  data = response.read()
  connection.close() 

  if response.status != 200:
    print("fail")

  return data



limit = 1000
query = "vasastan"
offset = 0

result = callbooliapi(limit, query, offset)

print "finished"
#print(callbooliapi(limit, query, offset))





# parsed = json.loads(data)
# output = parsed

# totalCount = parsed["totalCount"]

# print("totalCount = "+str(totalCount))

# noRequests = totalCount / limit + 1

# for i in range(1, noRequests): 
#   offset = i * limit
#   url = "/sold?q="+query+"&limit="+str(limit)+"&offset="+str(offset)+"&callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr
#   connection = httplib.HTTPConnection("api.booli.se") #python 2
#   connection.request("GET", url)
#   response = connection.getresponse()
#   data = response.read()
#   connection.close()
#   parsed = json.loads(data)
#   count = parsed["count"]
#   for i in range(0, count):
#     newItem = parsed["sold"][i]
#     output["sold"].append(newItem)


# with open('data.json', 'w') as outfile:
#     json.dump(output["sold"], outfile, indent=4)