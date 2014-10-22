#!/bin/bash
python watchersToUsers.py | sort -u > wch.u
python followersToUsers.py | sort -u > fw.u
python followingToUsers.py | sort -u > fwg.u
python eventsToUsers.py | sort -u > evt.u 
cat fw.done wch.u fw.u fwg.u evt.u | sort -u > all.u
join -v1 -t\; all.u fw.done > followers.todo
python gatherFw.py >> fw.out 2>> fw.err &
