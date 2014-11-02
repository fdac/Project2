import pymongo,re

rs = set ()
f = open ("repos")
for l in f:
  r = l .rstrip ()
  rs .add (r)

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['uToRepo']
for r in coll .find ({}, { "url":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["url"], r ["values"])
  for n in v:
    f = n ["full_name"]
    if f not in rs:
       print f + ';' + n ["created_on"]
