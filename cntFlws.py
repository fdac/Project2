import pymongo,operator
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['following']
fws = { }
fwd = { }
all = set ()
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):  
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://bitbucket.org/api/2.0/users/","").replace("/following","")
  if l not in fwd:
    fwd [l] = set ()
  all .add (l)
  for i in v:
    n = i ["username"]
    all .add (n)
    fwd [l] .add (n)
    if n not in fws: 
      fws [n] = set ()
    fws [n] .add (l)

coll = db ['followers']
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://bitbucket.org/api/2.0/users/","").replace("/followers","")
  if l not in fws: 
    fws[l] = set ()
  all .add (l)
  for i in v:
    n = i ["username"]
    all .add (n)
    if n not in fwd:
      fwd [n] = set ()
    fwd [n] .add (l)
    fws [l] .add (n)

for l in list (all):
  followers = ""
  nFlw = "0"
  followed = ""
  nFwd = "0"
  if l in fws:
    if len (list(fws [l])) > 0:
      nFlw = str (len(list(fws [l])))
      followers = ':' .join (list(fws [l])).encode("utf-8")
  if l in fwd:
    if len (list(fwd [l])) > 0:
      nFwd = str (len(list(fwd [l])))
      followed = ':' .join (list(fwd [l])).encode("utf-8")
  print l.encode("utf-8") + ';' + nFlw + ';' + nFwd + ';' + followers + ';' + followed 
