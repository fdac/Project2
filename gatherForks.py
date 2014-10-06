import sys, re, pymongo, json
import requests


jsonDict = {}

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']
# Reference a particular collection in the database
coll = db ['repos']


#do for forks, watchers, commits, clone, pullrequests
collName = 'forks'
def main(argv):
  if (len (argv) > 1):
    colName = argv [1]
  coll1 = db [collName]
  for r in coll .find ({}, { "links" : 1 } ):  
    url = r ['links'] [collName] ['href']
    id = r ['_id']
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
    if len (v) > 0:
      coll1.insert ( { 'url': url, 'parent': id, 'values': v} )
