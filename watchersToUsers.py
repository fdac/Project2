import pymongo,re
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
name = 'watchers'
coll = db [name]
fws = {'a'}
for r in coll .find ({}, { "url":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["url"], r ["values"])
  l = re.sub ("^.*/repositories/", "", l)
  l = re.sub ("/"+name, "", l)
  l = re.sub ("/.*", "", l)
  fws .add (l)
  for n in v:
    f = n ["username"]
    fws .add (f)

for f in fws:
   print f
