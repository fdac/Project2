
import re, pymongo, json
import requests


jsonDict = {}

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']
# Reference a particular collection in the database
coll = db ['repos']


#do for forks, watchers, commits, clone, pullrequests

collName = 'forks'
coll1 = db [collName]
for r in coll .find ({}, { "links" : 1 } ):  
  url = r ['links'] [collName] ['href']
  url1 = url + "/?pagelen=100"
  v = []
  while True:
     r = requests.get (url)
     t = r.text
     jsonDict = json.loads (t)
     for myIterator in jsonDict ['values']:
        v. append (myIterator)
     if 'next' not in jsonDict: break
     else: url1 = jsonDict['next']
     exit ()
  if len (v) > 0:
     coll1.insert ( { 'url': url, 'values': v} )
