import envoy, re, time

#Please set these as appropriate for your VM
DiskCapacity = 25000000*1000
netid='xxxxx'


n2s = {}
f = open ('RepoSize.csv')
for l in f: 
  ar = l .rstrip () .split(';')
  vcs = ar [1]
  s = int (ar [0])
  n2s [ar [5]] = s

start = time .time()
now = start
nmax = DiskCapacity
nused = 0
f = open ('divided')
toCopy = []
for l in f: 
  ar = l .rstrip () .split(';')
  t = int (ar [0])
  n = ar[2]
  p = re. sub('/', '_', n)
  s = n2s [ n ]
  vcs = ar [1]
  if (t == 1):
    cmdl = 'hg clone -U https://bitbucket.org/' + n + ' ' + p
    if vcs == 'git':
       next
    if (nused + s > DiskCapacity):
       now0 = time .time()
       print str (nused) + ' cloned in ' + str (now0 - now) 
       now = time .time()
       rsync = " ".join (toCopy)
       r = envoy .run ('rsync -ae "ssh -p2200" ' + rsync + ' ' + netid + '@da2.eecs.utk.edu:hg')
       r1 = envoy .run ('find ' + rsync + ' -delete')
       now = time .time()
       print str (nused) + ' synced in ' + str (now - now0)
       print r .std_out 
       print r .std_err
       print r1 .std_out 
       print r1 .std_err 
       nused = 0
       toCopy = []
    nused += s
    toCopy .append (p)
    r = envoy .run (cmdl)
    ttt = time .time()
    print str (r.status_code) + ';' + str (nused) + ';' + str (ttt) + ';' + cmdl
f .close()
