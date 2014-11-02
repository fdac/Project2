import pymongo,re
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['followers']
fws = { 'a' }
for r in coll .find ({}, { "url":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["url"], r ["values"])
  l = re.sub ("https://bitbucket.org/api/2.0/users/", "", l)
  l = re.sub ("/followers", "", l)
  fws .add (l)
  for n in v:
    f = n ["username"]
    fws .add (f)

for f in fws:
  print f .encode("utf-8") 
