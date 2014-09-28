import re

(nhg, ngit) = (0, 0)
f = open ('RepoSize.csv')
for l in f: 
  ar = l .split(';')
  vcs = ar [1]
  s = int (ar [0])
  if vcs == 'hg':
     nhg += s
  if vcs == 'git':
     ngit += s
f .close()

f = open ('RepoSize.csv')
ng = ngit/6
nh = nhg/6
for l in f:
  ar = l .rstrip() .split(';')
  vcs = ar [1]
  s = int (ar [0])
  n = ar [5]
  if (vcs == 'hg'):
     nhg -= s
     teamH = int(nhg/nh) + 1
     print str (teamH) + ';' + vcs + ';' + n
  else:
     ngit -= s
     teamG = int(ngit/ng) + 1
     print str (teamG) + ';' + vcs + ';' + n
