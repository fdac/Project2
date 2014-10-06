
import re, pymongo, json
import requests


jsonDict = {}
url = 'https://api.bitbucket.org/2.0/repositories/?pagelen=100'


client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']
# Reference a particular collection in the database
coll = db ['repos']

while True: 
  r = requests.get (url)
  t = r.text
  jsonDict = json.loads (t)
  for prj in jsonDict ['values']:
    coll .insert (prj) 
  if 'next' not in jsonDict: break
  else: url = jsonDict['next']

#f = open ('divided')
#for l in f: 
  # ar = l .rstrip () .split(';')
  # t = int (ar [0])
  # n = ar[2]
  # try:
  #   r = requests.get (url + n)
  #   if (r.ok):
  #     t = r.text
  #     jsonDict = json.loads (t)
  #     coll.insert (jsonDict) 
  #   else:
  #     print l + '\n'
  # except requests.exceptions.ConnectionError:
  #    sys.stderr.write('could not get ' + l + '\n')   
