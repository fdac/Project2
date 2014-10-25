#!/bin/bash
#db.repos.findOne({"full_name": { "$exists" : false }},{"_id":1})

while [[ $(cat followers.todo | wc -l) -gt 0 || $(cat watchers.todo | wc -l) -gt 0 ]] 
do python watchersToUsers.py | sort -u > wch.u
python followersToUsers.py | sort -u > fw.u
python followingToUsers.py | sort -u > fwg.u
python eventsToUsers.py | sort -u > evt.u 

cut -d/ -f1 repos.all | sort -u > rp.done
cut -d/ -f7 fw.out  | sort -u > fw.done
cut -d/ -f7 fwg.out  | sort -u > fwg.done
cat rp.done fw.done wch.u fw.u fwg.u evt.u uToRepo.done | grep -v ' ' | sort -u > all.u

join -v1 -t\; all.u fw.done > followers.todo
join -v1 -t\; all.u fwg.done > following.todo
[[ $(cat followers.todo | wc -l) -gt 0 ]] && python gatherFw.py >> fw.out 2>> fw.err 
[[ $(cat following.todo | wc -l) -gt 0 ]] && python gatherFwg.py >> fwg.out 2>> fwg.err 
#
cut -d/ -f7 uToRepo.out  | sort -u > uToRepo.done
join -v1 -t\; all.u uToRepo.done > uToRepo.todo

[[ $(cat uToRepo.todo | wc -l) -gt 0 ]] &&  python gatherRepos.py >> uToRepo.out 2>> uToRepo.err
#
python usersToRepos.py | cut -d\; -f1 > new.repos
cut -d\/ -f6-7 events.out | grep -v ' ' | sort -u > eventsRepos.done
cut -d\/ -f6-7 watchers.out | grep -v ' ' | sort -u > watchersRepos.done
python list.py | sort -u > repos.done
cat new.repos repos repos.done watchersRepos.done eventsRepos.done | grep -v '^$' |grep -v '^/' | sort -u > repos.all
join -t\; -v1 repos.all eventsRepos.done > events.todo
[[ $(cat events.todo | wc -l) -gt 0 ]] && python gatherEvents.py >> events.out 2> events.err
join -t\; -v1 repos.all repos.done > repos.todo
[[ $(cat repos.todo | wc -l) -gt 0 ]] && python gatherMetaData1.py >> repos.out 2>> repos.err
for i in watchers 
do cut -d\/ -f6-7 $i.out | sort -u > ${i}Repos.done
join -t\; -v1 repos.all ${i}Repos.done > $i.todo
[[ $(cat $i.todo | wc -l) -gt 0 ]] &&  python gatherForks1.py $i >> $i.out 2> $i.err
done

done 
