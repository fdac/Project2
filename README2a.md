Project2a
========

Intermediate Results
--------------------

### Data

Please note that the question of architecting cloud applications
that are effective for data gathering as in Project 2a is a rich
topic for a final project.

```
| Team | AWS VM       |  Time |        Cost/Hr | Gb retrived | Gb/$ | Gb/h | Comments                                                               |
|------+--------------+-------+----------------+-------------+------+------+------------------------------------------------------------------------|
| T1   | t1.micro     |   105 |           .013 |         600 |  440 |    6 | The remaining repos are cloned using 7 instances                       |
| T2   | t2.medium    | 111.5 |       .052+.07 |         808 |   59 |    7 | Clones to 1Tb EBS magnetic volume/no rsync                             |
| T3   | m3.2xlarge   |    39 |           0.56 |         215 |   10 |    6 |                                                                        |
| T4   | c3.2xlargex3 |   5.4 | 0.42*3+.05+.14 |      1039.9 |  133 |  193 | 3 instances and a total of 24 processes (8 per instance or 1 per core) |
| T5   | r3.2xlarge   |    39 |            0.7 |         288 |   11 |    7 |                                                                        |
| T6   | i2.xlarge    |  5.08 |           0.85 |          49 |   11 |   10 |                                                                        |
| T6   | i2.xlarge    |  1.99 |           0.85 |          49 |   29 |   25 | clone only                                                             |
| hg   | m3.large     |   3.6 |           0.14 |        24.9 |   49 |    7 | clone only                                                             |
| git  | m3.large     |   2.5 |           0.14 |        22.3 |   64 |    9 | clone only                                                             |
| hg   | t1.micro     |  4.19 |           .013 |        19.6 |  360 |    5 | clone only                                                             |
| git  | t1.micro     |  2.25 |           .013 |        21.7 |  742 |   10 | clone only                                                             |
```
Please email me corrected numbers, I copied these from the
whiteboard. Also, if you have not done yet, please send me the architecture:
e.g., threads to clone, threads to sync and any special disk/network 
setup, etc.

For example, the data cloning architectures for Team3-2, Team4-2,
Team5-2, and Team6-2 are below:

![Retrieval architecture for Team3-2](https://github.com/fdac/Project2/blob/master/T3Arch.png "T3 Architecture")
![Retrieval architecture for Team4-2](https://github.com/fdac/Project2/blob/master/T4Arch.png "T4 Architecture")
![Retrieval architecture for Team5-2](https://github.com/fdac/Project2/blob/master/T5Arch.png "T5 Architecture")
![Retrieval architecture for Team6-2](https://github.com/fdac/Project2/blob/master/T6Arch.png "T6 Architecture")

###Difficulties Encountered:
1. Various ssh key authentication issues, including, for rsync: see
   Step 5 in "Instructions for Project2a" below.
1. Some repos require password while cloning. Redirecting standard
   input does not appear to work. The following script (put it in
   file 'run' and run via 'expect run > ~/statsHg 2> ~/statsHg.err'. Install 'expect' command via
   "sudo apt-get install expect"). Many of repos for Team 6 keep
   asking "user:" "password:" sequence indefinitely. Sending Ctrl-D
   takes care of that. Team3 has used BB API to check if the
   repository is private just before the cloning and report that
   to work well.

 ```
 #!/usr/bin/expect
 set timeout -1
 spawn python cloneHg.py
 expect {           
    "Username for 'https://bitbucket.org':" {
        send "\r"
        exp_continue
    } 
    "Password for 'https://bitbucket.org':" {
        send "\r"
        exp_continue
    }
    "user:" {
        send "\004"
        exp_continue
    }
    "password:" {
        send "\004"
        exp_continue
    }
 }
 ```
 For example
 ```
 git clone --mirror https://bitbucket.org/szlorens/degramobile szlorens_degramobile
 ```
 asks for password. Alternatively, you can use command timeout which kills a process that takes
        longer than specified time.
 
1. Issues with adapting python/bash scripts. Please take a look at
  [cloneHg.py](https://github.com/fdac/Project2/blob/master/cloneHg.py)
  and
  [cloneGit.py](https://github.com/fdac/Project2/blob/master/cloneGit.py)
  Both seem to work.
1. No module envoy:

 ```
 sudo apt-get install python-pip
 sudo pip install envoy
 ```

1. How to run the script unattended.
 If you exit the shell from where you started a script the script
 gets hangup signal and, unless it ignores it, is terminated. There
 are several ways around that.
 1. Run 'nohup ./ScriptName'
 2. If it is already running
 see [here](http://stackoverflow.com/questions/625409/how-do-i-put-an-already-running-process-under-nohup)
 3. Use [screen](http://stackoverflow.com/questions/3202111/set-screen-names-with-gnu-screen)
  


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
 * Team4: any type
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
Note: to use key-based authentication for paswordless login ssh uses
a key pair: a private and a public key. You can use the 'micro' key on
fdac/aws or create a different one. If you ssh from VM A to VM B,
 you need the secret key on A (as ~/.ssh/id_rsa to avoid adding -i
 pathToKey option to ssh) and the public key on B as a
one line in  ~/.ssh/authorized_keys. Note that authorized_keys can have
 multiple lines for multiple public keys). If you need access from B to
 A, then also put the secret key as B's ~/.ssh/id_rsa and the public key as
 a line in A's ~/.ssh/authorized_keys. Please make sure that ~/.ssh
 and ~/.ssh/id_rsa are *not* readable or writable by anyone
 else. E.g., run:
 ```
 chmod -R 600 ~/.ssh
 ```
 on both A an B.

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
Here are python files for cloning [hg](https://github.com/fdac/Project2/blob/master/cloneHg.py) and [git](https://github.com/fdac/Project2/blob/master/cloneGit.py) that appear to work.