import pymongo,operator
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
wchs = {}
all = {}
frks = {}
prs = {}
coll = db ['pullrequests']
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://api.bitbucket.org/2.0/repositories/","").replace("/pullrequests","")
  all [l] = 1
  if l not in prs: prs[l] = set ()
  for i in v:
    a = i ["author"]
    if a is not None:
      u = a ["username"] 
      prs [l] .add (u)

coll = db ['watchers']
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):  
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://api.bitbucket.org/2.0/repositories/","").replace("/watchers","")
  if l not in wchs: wchs [l] = set ()
  all [l] = 1
  for i in v:
    wchs [l] .add (i["username"])

coll = db ['forks']
for r in coll .find ({}, { "url" : 1, "values":1,"_id":0 } ):
  u, v = (r ["url"], r ["values"])
  l = u .replace ("https://api.bitbucket.org/2.0/repositories/","").replace("/forks","")
  all [l] = 1
  if l not in frks: frks[l] = set ()
  for i in v:
    frks[l] .add (i["full_name"])


for l in all .keys ():
  nw, nf, np = 0, 0, 0
  w, f, p = '', '', ''
  if l in wchs:
    nw = len (wchs[l])
    w = ':' .join (list(wchs[l]))
  if l in frks:
    nf = len (frks[l])
    f = ':' .join (list(frks[l]))
  if l in prs:
    np = len (prs[l])
    p = ':' .join (list(prs[l]))
  print l + ';' + str(nw) + ';' + str  (nf) + ";" + str (np) + ';' + w + ';' + f + ';' + p
