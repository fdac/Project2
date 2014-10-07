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
if (len (sys .argv) > 1):
  collName = sys .argv [1]


def chunks(l, n):
  if n < 1: n = 1
  return [l[i:i + n] for i in range(0, len(l), n)]

coll1 = db [collName]
for r in coll .find ({}, { "links" : 1 } ):  
  url = r ['links'] [collName] ['href']
  id = r ['_id']
  url1 = url + "/?pagelen=100"
  v = []
  size = 0
  while True:
    try: 
      r = requests.get (url1)
      t = r.text
      jsonDict = json.loads (t)
      if ('values' in jsonDict):
        for el in jsonDict ['values']:
          v. append (el)
          size += sys .getsizeof (el)
      if 'next' not in jsonDict: 
        print str (len (v)) + ';' + str (size) + ';' + url1
        sys .stdout .flush ()
	break
      else: url1 = jsonDict['next']
      print str (len (v)) + ';' + str (size) + ';' + url1
      sys .stdout .flush ()
    except Exception as e:
      print "Could not get:" 
      print url
      print e
      sys .stdout .flush ()
  if len (v) > 0:    
    if (size < 16777216/2):
      coll1.insert ( { 'url': url, 'parent': id, 'values': v } )
    else:
      s = size;
      n = 2*s/16777216
      for ch in chunks (v, n):
        coll1.insert ( { 'url': url, 'parent': id, 'values': ch } ) 
