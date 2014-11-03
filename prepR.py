import time
from datetime import datetime
from dateutil.parser import parse

rstats = {}
ustats = {}
stats = {}
if __name__ == '__main__':
  f = open ('RepoSize.csv')
  for l in f: 
    ar = l .rstrip () .split(';')
    vcs = ar [1]
    fr = str(time.mktime(parse(ar[3]).timetuple()))
    to = str(time.mktime(parse(ar[4]).timetuple()))
    s = ar [0]
    n = ar [5]
    u = n .split ("/")[0]
    n = n .replace ("/","_")
    rstats [n] = (vcs, s, fr, to, u)
  us = open('cntFlws.out', 'r').readlines()
  for u in us:
    u = u.strip()
    n, nFl, nFd, flws, fwd = u.split(';')
    ustats [n] = (nFl, nFd)
  repos = open('cntWch.out', 'r').readlines()
  for repo in repos:
    repo = repo.strip()
    n, nW, nFr, nPu, w, f, p = repo.split(';')
    n = n .replace('/', '_')
    stats [n] = (nW, nFr, nPu)
  print "repo;nW;nFr;nPu;nDe;nAu;nFi;vcs;Siz;from;to;u;nFl;nFd";
  repos = open('measures.out', 'r').readlines()
  for repo in repos:
    repo = repo.strip()
    n, nDe, nAu, nFi, authors, files = repo.split(';')
    nW, nFr, nPu = ("0", "0", "0")
    if n not in rstats:
      continue
    if n in stats:
       nW, nFr, nPu = stats [n]
    vcs, Siz, fr, to, u = rstats [n]
    nFl, nFd = ("0", "0")
    if u in ustats:
      nFl, nFd = ustats [u]
    res = (n, nW, nFr, nPu, nDe, nAu, nFi, vcs, Siz, fr, to, u, nFl, nFd)
    print ';' .join (res)
