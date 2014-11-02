import subprocess, sys, re, time

n2s = {}
p2n = {}
n2v = {}
f = open ('RepoSize.csv')
for l in f: 
  ar = l .rstrip () .split(';')
  vcs = ar [1]
  s = int (ar [0])
  n = ar [5]
  if re.search ("/\.$", n):
     p = re. sub('/.$', '', n)
     p = 'bitbucket.org_' + p + '/' + p
  else:
     p = 'bitbucket.org_' + re. sub('/', '_', n)
  p2n [ p ] = n
  n2s [ n ] = s
  n2v [ n ] = vcs

start = time .time()
now = start
nused = 0
fname = 'todo'
if len (sys .argv) > 1:
	fname = sys.argv[1]
f = open (fname)
toCopy = []
for l in f: 
  p = l .rstrip ()
  if p not in p2n:
     sys.stderr.write(p + " is not found\n")
     continue
  n = p2n [ p ]
  vcs = n2v [ n ]
  cmdl = 'hg log -v --style ~audris/bin/multiline1 bb/' + p + ' | gzip > delta/' + p + '.delta.gz'
  if vcs == 'git':
    cmdl = 'git --git-dir=bb/' + p + ' log --numstat -M -C --diff-filter=ACMR --full-history --pretty=tformat:"STARTOFTHECOMMIT%n%H;%T;%P;%an;%ae;%at;%cn;%ce;%ct;%s" | /usr/bin/perl ~audris/bin/extrgit.perl | gzip > delta/' + p + '.delta.gz'
  r = subprocess.call (cmdl, shell=True)
  ttt = time .time()
  print str (r) + ';' + str (ttt-start) + ';' + cmdl
