
import sys, re, pymongo, json
import requests


jsonDict = {}
url0 = 'https://api.bitbucket.org/2.0/repositories/'
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']
# Reference a particular collection in the database
coll = db ['repos']

f = open ('repos.todo')
for n in f:    
  n = n .rstrip ()
  url = url0 + n
  r = requests.get (url)
  t = r.text
  if t != 'Forbidden':
    if re.search("^{", t):
      jsonDict = json.loads (t)
      if "full_name" in jsonDict:
         coll .insert (jsonDict) 
         print url
      else:
         print url + "/ no name"
         sys.stderr.write (url + " " + t + "\n")
    else:
      print url + "/ not json"
      sys.stderr.write (url + " " + t + "\n")
  else:
    print url + "/ forbidden"
    sys.stderr.write (url + " is forbidden" + "\n")
