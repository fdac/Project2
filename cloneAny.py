import sys, envoy, re, time

n2s = {}
p2n = {}
n2v = {}
f = open ('RepoSize.csv')
for l in f: 
  ar = l .rstrip () .split(';')
  vcs = ar [1]
  s = int (ar [0])
  n = ar [5]
  p = re. sub('/', '_', n)
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
  n = p2n [ p ]
  s = n2s [ n ]
  vcs = n2v [ n ]
  tmo = str (s/1000000 + 100)
  cmdl = 'timeout ' + tmo +  ' hg clone -U https://bitbucket.org/' + n + ' ' + p
  if vcs == 'git':
    cmdl = 'timeout ' + tmo + ' git clone --mirror https://bitbucket.org/' + n + ' ' + p
  r = envoy .run (cmdl)
  nused += s
  ttt = time .time()
  print str (r.status_code) + ';' + str (nused) + ';' + str (ttt) + ';' + cmdl
  sys.stdout.flush()
