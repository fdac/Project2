Where the measures are right now
---------------------------
- Repository descriptions (repo), "followers", "forks", "pullrequests", "watchers"
are collections in mongodb (database 'bitbucket')
- All repos are in ~audris/bitbucket.org\_USER\_REPO
- Commits are in ~audris/delta/bitbucket.org\_USER\_REPO.delta.gz
  (auxiliary and markdcarringer kindly agreed to import that data as collection delta into mongodb)
  The script used to extract commits from repositories is in fdac/Project2/deltaAny.py)

Instructions for Project2b 
--------------------------

While the VCS data is being cloned, we could productively work towards
answering some of the investor questions. Lets consider the first
two questions: 
* How accurate is the language specification in the project
   description?
* How much actual source code each repository has?

To answer them we need to get files in each repository, for example,
for repo XXXXX:
```
git --git-dir=XXXXX ls-tree -r --name-only HEAD
hg log -v --style hg.fmt -R XXXXX | sort -u
```
would output a list of all files. The content of hg.fmt is:
```
changeset="{files}"
file="{file}\n"
```
To count lines in files, it would be necessary to get the latest
version of each file (or all version of every file) and count the
lines. Answering this question could be a challenging final project.

There are other questions investors asked, and answering any one of
them could also be a challenging final project.

For  Project2b, however, we need to practice the use of MongoDB...

MongoDB is a nosql database thats primarily useful for storing
json strings. 

A connection to the MongoDB server (da0.eecs.utk.edu) provides you with an
option to use three databases: gutenberg, bitbucket, and test (github).

Within each database there are one or more collections (tables) with
data. In particular, database 'bitbucket' has fully populated collection
'repos' that contains information retrieved by the following requests:
```
https://api.bitbucket.org/2.0/repositories/XXX/XXX
```

Other collections: forks and watchers are fully populated
but commits and pullrequests are not fully
populated at present. Your team will need to populate them for the
projects your team is responsible for.
An example script that populates the collection is gatherForks1.py.


Some examples of extracting data from MongoDB are given in
PlayWithMongo.ipynb.

For Project 2b, we will need to write and start scripts to populate data for 
the following collections in database bitbucket:
* commits and pullrequests.
The scrips can run on the da VMs that can directly connect to MongoDB on da0


To connect to mongodb from ealsewhere please use port forwarding:
```
ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -N YourNetId@da2.eecs.utk.edu 
```
To shorten your command line you can put the following into the computer's
.ssh/config:
```
host davm0
  hostname da2.eecs.utk.edu
  IdentitiesOnly yes
  IdentityFile ~/.ssh/micro
  LocalForward 27017 da0.eecs.utk.edu:27017
  port 2200
```
Then mongodb will be accecssible from that computer as 
```
client = pymongo.MongoClient (host="localhost")
```

If you want to run ipython on the da vms, don't forget to 
forward the port 8888 to the right vm! 

## A direct way to extract commits
You can modify the following scripts to extract commits a bit faster than via
BB REST API
```
cat YOUR_HG_REPOS | while read i
do j=$(echo $i| sed 's"/"_"')
   hg log -v --style ~audris/bin/multiline1 bitbucket.org_$j | gzip > bitbucket.org_$j.log.gz
done

cat YOUR_GIT_REPOS | while read i
git --git-dir=$i log --numstat -M -C --diff-filter=ACMR --full-history \
 --pretty=tformat:"STARTOFTHECOMMIT%n%H;%T;%P;%an;%ae;%at;%cn;%ce;%ct;%s" \
 | perl ~audris/bin/extrgit.perl | gzip > $i.delta.gz
```
