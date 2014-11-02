import sys, re, pymongo, json
import requests


jsonDict = {}
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']


#do for forks, watchers, commits, clone, pullrequests
collName = 'uToRepo'

def chunks(l, n):
  if n < 1: n = 1
  return [l[i:i + n] for i in range(0, len(l), n)]

f = open (collName + '.todo')
coll1 = db [collName]
for n in f:    
  n = n .rstrip ()
  url = "https://bitbucket.org/api/2.0/repositories/" + n 
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
      break
  if len (v) > 0:
    # size may be bigger in bson, factor of 2 doesnot always suffice    
    if (size < 16777216/3):
      coll1.insert ( { 'url': url, 'values': v } )
    else:
      s = size;
      n = 3*s/16777216
      i = 0
      for ch in chunks (v, n):
        coll1.insert ( { 'chunk': i, 'url': url, 'values': ch } )
        i = i + 1 
