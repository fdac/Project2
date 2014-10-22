import pymongo,re
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
name = 'events'
coll = db [name]
fws = {'a'}
for r in coll .find ({}, { "full_name":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["full_name"], r ["values"])
  l = re.sub ("/.*", "", l)
  fws .add (l)
  for n in v:
    if "user" in n:
       f = n ["user"]
       if f is not None:
          if "username" in f:
             fws .add (f ["username"])

for f in fws:
   print f
