import sys, re, pymongo, json
import requests


jsonDict = {}

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['test']
# Reference a particular collection in the database
coll = db ['followers']


for r in coll .find ({}, { "login" : 1, "follows":1,"_id":0 } ):  
  l, f = (r ["login"], r ["follows"])
  print l + ";" + f
