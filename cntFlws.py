import pymongo,operator
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['following']
fws = { }
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):  
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://bitbucket.org/api/2.0/users/","").replace("/following","")
  for i in v:
    n = i ["username"]
    if n not in fws: 
      fws [n] = set ()
    fws [n] .add (l)

coll = db ['followers']
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://bitbucket.org/api/2.0/users/","").replace("/followers","")
  if l not in fws: 
    fws[l] = set ()
  for i in v:
    fws[l] .add (i ["username"])

for l in fws .keys ():
  if l in fws:
    if len (list(fws [l])) > 0:
      string = ':' .join (list(fws [l])).encode("utf-8")
      print l.encode("utf-8") + ';' + str (len(list(fws [l]))) + ';' + string
