import sys, re, pymongo, json
import requests


jsonDict = {}

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['bitbucket']
# Reference a particular collection in the database
coll = db ['repos']


for r in coll .find ({}, { "full_name" : 1 } ):
  if "full_name" in r:  
     url = r ["full_name"]
     print url
  else:
     sys.stderr.write ("No name " + r ["_id"])
