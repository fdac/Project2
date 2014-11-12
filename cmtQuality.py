import pymongo,operator,sys
from numpy import percentile
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['deltas']
cmtAll = {}
cmtRepo = {}
cmtAuthor = {}
nrec  = 0
for r in coll .find ({}, {"commits.comment":1,"commits.author":1,"name":1} ):
  c, n = (r ["commits"], r ["name"])
  for cmt in c:
    if "comment" not in cmt:
      continue
    a = cmt ["author"]
    cm = cmt ["comment"]
    if cm not in cmtAll:
      cmtAll [cm] = 1
    else:
      cmtAll [cm] += 1
    if n not in cmtRepo:
      cmtRepo [n] = { cm: 1 }
    else:
      if cm not in cmtRepo [n]:
        cmtRepo [n][cm] = 1
      else:
        cmtRepo [n][cm] = cmtRepo [n][cm] + 1
    if a not in cmtAuthor:
      cmtAuthor [a] = { cm: 1 }
    else:
      if  cm not in cmtAuthor [a]:
        cmtAuthor [a][cm] = 1
      else:
        cmtAuthor [a][cm] = cmtAuthor [a][cm] + 1
  nrec += 1
  if nrec % 10000 == 0:
    sys.stderr.write (str (nrec) + ' done\n')

for a in cmtAuthor .keys ():
  nCmt, lCmt  = 0, 0
  z = cmtAuthor [a] .values () 
  pct = percentile (z, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100])
  for cm in cmtAuthor [a]:
    nCmt += cmtAuthor [a][cm]
    lCmt += len (cm)
  print 'a;' + a.encode('utf-8') + ';' + str(len(cmtAuthor [a])) + ';' + str(nCmt) + ';' + str(lCmt) + ';' + ';' .join (map(str, pct))

for r in cmtRepo .keys ():
  nCmt, lCmt = 0, 0
  z = cmtRepo [r] .values ()
  pct = percentile (z, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100])
  for cm in cmtRepo [r]:
    nCmt += cmtRepo [r][cm]
    lCmt += len (cm)
  print 'r;' + r + ';' + str(len(cmtRepo [r])) + ';' + str(nCmt) + ';' + str(lCmt) + ';' + ';' .join(map(str,pct))
