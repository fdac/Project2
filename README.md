Project2a
========

Retrieve and store BitBucket VCS
----------------------------------

Investors were intrigued by the presentation on the prospects of 
DeveloperParadise, but had a few questions and requests: 

1. How accurate is the language specification in the project
   description?
1. How much actual source code each repository has?
1. Why is there such a rapid growth of Ruby projects (e.g., are they
   being moved from other forges)?
1. What are the types of applications being built on BitBucket?
1. Why the comparison was made only with the BitBucket, not the
   market leader GitHub or older players like GoogleCode or
   SourceForge?
1. Are repository importance measures (last update) reasonable or
   could better?
1. DeveloperParadise needs to show projects with significant impact for
   publicity: do they have a higher concentration of such projects
   than BB? Could it attract some of the BB projects to DP?
   

They agreed to provide limited funding to your teams to investigate
these questions further.  In particular, they provided $1700 in AWS
credits and sufficient storage space for you to complete this
investigation.

Project2a will focus on retrieving raw data necessary to answer these
questions, Project2b on extracting data from retrieved VCS and storing it in 
a way to facilitate the subsequent analysis, and Project2c on
analyzing it and on providing answers to investors.

The investors are a bit impatient and want a brief technical readout
of the data retrieval progress in one week. They would like to know
if their money is used wisely, in particular, they would like to
know how many MB of repository data is retrieved per $ of provided
funding, how long it will take to get all the data, and what
approaches will be used to analyze it.

Instructions for Project2a 
--------------------------
To speed up the process, the tasks will be distributed among newly
formed six teams.  Each team will find a list of repositories that
they need to retrieve in file 'divided' (the columns "team", "vcs",
and "repository" are semicolon separated).

[Instructions on servers/VMs to use](https://github.com/fdac/aws)

A brief version:

1. To store repositories please use any one of five da2 vms 

 ```
 ssh -p2200 yournetid@da2.eecs.utk.edu
 ...
 ssh -p2204 yournetid@da2.eecs.utk.edu
 ```
   Your home directory will be the same across these five da2 VMs.

1. To clone the repos please use AWS VMs of the type specified for your team:
 (the various instances are described [here](http://aws.amazon.com/ec2/pricing))
 * Team1: t2.micro
 * Team2: t2.medium
 * Team3: m3.2xlarge
 * Team5: any type
 * Team5: r3.2xlarge
 * Team6: i2.xlarge
 * note: For instances with no instance storage (t2.micro,t2.medium) it is possible to specify
   ebs storage. The largest repository on BB is 22Gb, so
   you should use at least that much storage for your instance.

1. To clone hg repositories (e.g., ape_hand/new) please use

 ```
 hg clone -U https://bitbucket.org/ape_hand/new ape_hand_new
 ```
1. To clone git repositories (e.g., opensymphony/xwork) please use

 ```
 git clone --mirror https://bitbucket.org/opensymphony/xwork opensymphony_xwork
 ```
1. Once the disk of the AWS VM is filled, please rsync to 
your home directory of the da2 VM via

 ```
 rsync -ae 'ssh -p 2200' ListofRepoFolders yournetid@da2.eecs.utk.edu:
 ```
1. Here is an example script: you may want to modify
the amount of disk left (1000000) to be just above the size of the
repo about to be cloned as is done in the next example:

 ```
 TEAM=1
 grep ^$TEAM';hg' divided > todohg
 grep ^$TEAM';git' divided > todogit
 mkdir hg
 cd hg
 cat ../todohg | while read repo
 do path=$(echo $repo | sed 's"/"_")
   hg clone -H https://bitbucket.org/$repo $path
   spcleft=$(df -k . | tail -1 | awk '{ print $4 }')
   if [[ $spcleft -lt 1000000 ]]
   then
      #rsync and remove what has been copied
      rsync -ae 'ssh -p2200' * YourNetId@da2.eecs.utk.edu:hg/
      ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done
   fi
 done
 cd ../
 #similar for git
 ```
1. Alternatively, you may consider writing a more sophisticated python
script with timing of individual operations, e.g., something
along the following lines:
```
import envoy, re, time
n2s = {}
f = open ('RepoSize.csv')
for l in f: 
  ar = l .split(';')
  vcs = ar [1]
  s = int (ar [0])
  n2s [ar [5]] = s

start = time .time()
now = start
nmax = DiskCapacity
nused = 0
f = open ('divided')
for l in f: 
  ar = l .split(';')
  t = int (ar [0])
  n = ar[2]
  p = re. sub('/', '_', n)
  s = n2s [ n ]
  vcs = ar [1]
  if (t == myTeam):
    cmd = 'git clone --mirror https://bitbucket.org/' + n + ' ' + p
    if vcs == 'hg':
	   cmd = 'hg clone -U https://bitbucket.org/' + n + ' ' + p
    if (nused + s > DiskCapacity):
	   now0 = time .time()
	   print str (nused) + ' cloned in ' + str (now0 - now) 
	   now = time .time()
	   envoy .run ('rsync -ae "ssh -p2200" * YourNetId@da2.eecs.utk.edu:hg')
       envoy .run ('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
	   now = time .time()
	   print str (nused) + ' synced in ' + str (now - now0) 
	   nused = 0
	nused += s
	envoy .run (cmd)
f .close()
```
It may be worth-while to count time for git repos separately from
the time for hg repos: the cloning time may differ a lot.


Instructions for Project2bc
---------------------------
forthcoming...


References
----------
1. [Large-scale code reuse in open source software](https://github.com/fdac/Project2/blob/master/floss.pdf)
   In ICSE'07 Intl. Workshop on Emerging Trends in FLOSS Research
   and Development, Minneapolis, Minnesota, May 21 2007.
1. [Amassing and indexing a large sample of version control systems: towards the census of public source code history](https://github.com/fdac/Project2/blob/master/MSR2009_0113_mockus_audris.pdf)
   In 6th IEEE Working Conference on Mining Software Repositories,
   May 16-17 2009
1. [Lean GHTorrent: GitHub Data on Demand](https://github.com/fdac/Project2/blob/master/p384-gousios.pdf)
   In Proceedings of the 11th Working Conference on Mining Software
   Repositories, MSR 2014 (384–387)
1. [The relationship between folder use and the number of forks: A case study on github repositories](https://github.com/fdac/Project2/blob/master/folder-short.pdf). In
   ESEM, Torino, Italy, September 2014.
