#!/bin/bash
python watchersToUsers.py | sort -u > wch.u
python followersToUsers.py | sort -u > fw.u
python followingToUsers.py | sort -u > fwg.u
python eventsToUsers.py | sort -u > evt.u 

cut -d/ -f7 fw.out  | sort -u > fw.done
cut -d/ -f7 fwg.out  | sort -u > fwg.done

cat fw.done wch.u fw.u fwg.u evt.u | sort -u > all.u
join -v1 -t\; all.u fw.done > followers.todo
join -v1 -t\; all.u fwg.done > following.todo
python gatherFw.py >> fw.out 2>> fw.err 
python gatherFwg.py >> fwg.out 2>> fwg.err 

