import http.client
import time
from hashlib import sha1
import random
import string
import json

callerId = "williambengtsson"
timestamp = str(int(time.time()))
unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
s = callerId+timestamp+"1B8yJRDjHUQwND92jnQ3awLOCaj6NxFfi3HInjN4"+unique
hashstr = sha1(s.encode('utf-8')).hexdigest()

limit = 1000
query = "vasastan"
offset = 0

url = "/sold?q="+query+"&limit="+str(limit)+"&offset="+str(offset)+"&callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr

connection = http.client.HTTPConnection("api.booli.se")
connection.request("GET", url)
response = connection.getresponse()
data = response.read()
connection.close()

if response.status != 200:
    print("fail")

parsed = json.loads(data)

totaltCount = parsed["totalCount"]



with open('newItem.json') as json_data:
    d = json.load(json_data)

count = d["count"]

#for i in range(0, count):
    #newItem = d["listings"][i]
    #parsed["listings"].append(newItem)
    #print(i)

#newItem = d["listings"][1]
#parsed["listings"].append(newItem)

with open('data.json', 'w') as outfile:
    json.dump(parsed, outfile, indent=4)