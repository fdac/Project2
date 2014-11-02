 Instructions for Project2c 
--------------------------

To finish Project2 (and Project2c)
---------------------------------
- calculate a measure of your choice
- fit a model that explains or uses that measure (as in the example)


Example
=======
fdac/Project2/Measures-R.ipynb

It uses data from file prepR.r.

How was prepR.r was generated?
```
python measures.py > measures.out
python cntWch.py > cntWch.out
python cntFlws.py > cntFlws.out
python prepR.py > prepR.r
```

##For Oct 24 think of a measure of influence based on the data in MongoDB.
Photo of the whiteboard with several ideas:
![WB](https://github.com/fdac/Project2/blob/master/WB.jpg "Measures of Influence")

T4 prepared the following list:
Influence of a user in a project:
- # commits in a project
- amount of code added to a project(s)

Influence of a user:
- # of projects part of
- # of quality projects part of (define quality)
- # of non-owner projects working on
- # of followers
- # of connections (followers or following)
- # of implemented pull requests

Influence of a project:
- # of forks
- # of pull requests
- # of unique commiters
- # of projects that depend on a project (define dependency)
- # of clones



We will focus on identifying likely-to-be-popular-in-the-future
projects and, in order to get some ideas on how to measure that, 
please read the following opinion pieces:
* [How to join a project](https://opensource.com/business/14/9/jump-into-open-source-project)
* [Ways to contribute](http://blog.smartbear.com/programming/14-ways-to-contribute-to-open-source-without-being-a-programming-genius-or-a-rock-star/)

Here is a  summary chart (provided by auxiliary):
![A summary chart](https://github.com/fdac/Project2/blob/master/OSS.png "Participating in OSS")

On github we can count followers:
```
import pymongo
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['test']
coll = db ['followers']
fws = {}
for r in coll .find ({}, { "login" : 1, "follows":1,"_id":0 } ):  
  l, f = (r ["login"], r ["follows"])
  if f in fws:
    fws [f] .add (l)
  else:
    fws [f] = { l }

fwsC = []
for f in fws:
   fwsC .append ((f, len (fws[f])))
srt = sorted (fwsC, key = lambda x : x[1], reverse=True)[0:10]
for f in srt:
  print f[0] + ' has ' + str (f[1]) + " followers" 

Output:
torvalds has 18884 followers
paulirish has 12194 followers
visionmedia has 10785 followers
schacon has 10565 followers
mojombo has 9833 followers
defunkt has 8919 followers
pjhyett has 8584 followers
ryanb has 6167 followers
wycats has 5603 followers
mattt has 5379 followers
```

Similarly on bitbucket we can do the same (once the collection followers is 
populated)
```
import pymongo,re
client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['followers']
fws = {}
for r in coll .find ({}, { "url":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["url"], r ["values"])
  l = re.sub ("https://bitbucket.org/api/2.0/users/", "", l)
  l = re.sub ("/followers", "", l)
  for n in v:
    f = n ["username"]
    if l in fws:
      fws [l] .add (f)
    else:
      fws [l] = { f }

fwsC = []
for f in fws:
   fwsC .append ((f, len (fws[f])))
srt = sorted (fwsC, key = lambda x: x[1], reverse=True)[0:10]
for f in srt:
  print f[0] + ' has ' + str (f[1]) + " followers" 

Output:
ubernostrum has 398 followers
sjl has 326 followers
ianb has 270 followers
mitsuhiko has 253 followers
jespern has 240 followers
dhellmann has 182 followers
jezdez has 158 followers
homakov has 151 followers
BruceEckel has 137 followers
geckofx has 118 followers

```
## The law of Followers
It appears that .2M users of BB (vs 9.5M for GH)
can provide at most .4K followers (vs 20K for GH), or
a maximum of 2 followers per K users in BB (vs maximum of
2 followers per K users in GH). Hmm... Should this law be named?

Note that while there are  only 193K users with repos, the following 
recursive script finds almost double that number (getUsers.sh)
```
python watchersToUsers.py | sort -u > wch.u
python followersToUsers.py | sort -u > fw.u
python followingToUsers.py | sort -u > fwg.u
python eventsToUsers.py | sort -u > evt.u 
cut -d/ -f7 fw.out  | sort -u > fw.done
cat fw.done wch.u fw.u fwg.u evt.u | sort -u > all.u
join -v1 -t\; all.u fw.done > followers.todo
python gatherFw.py >> fw.out 2>> fw.err &
```

