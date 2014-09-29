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

Project2a will focus on retrieving data necessary to answer these
questions, Project2b on storing that data, and Project2c on
analyzing it and providing answers to investors.

The investors are a bit impatient and want a brief technical readout
of the data retrieval progress in one week. They would like to know
if their money is used wisely, in particular, they would like to
know how many MB of repository data is retrieved per $ of provided
funding, how long it will take to get all the data, and what
approaches will be used to analyze it.

Instructions for Project1a 
--------------------------
To speed up the process, the tasks will be distributed among newly
formed six teams.  Each team will find a list of repositories that
they need to retrieve in file 'divided' (the columns "team", "vcs",
and "repository" are semicolon separated).

[Instructions on servers/VMs to use](https://github.com/fdac/aws)

Each team will use a different type of AWS machine:
(the various instances are described [here](http://aws.amazon.com/ec2/pricing)
* Team1: t2.micro
* Team2: t2.medium
* Team3: m3.2xlarge
* Team5: r3.2xlarge
* Team6: i2.xlarge

To clone hg repositories please use
```
hg clone -U 
```

To clone git repositories please use
```
git clone --mirror
```

Once the disk of the AWS VM is filled, please rsync to 
the home directory of the DA VM via
```
rsync -a
```

Instructions for Project2bc
---------------------------
forthcoming...


References
----------
1. [Large-scale code reuse in open source software](https://github.com/fdac/Project2/floss.pdf)
   In ICSE'07 Intl. Workshop on Emerging Trends in FLOSS Research
   and Development, Minneapolis, Minnesota, May 21 2007.
1. [Amassing and indexing a large sample of version control systems: towards the census of public source code history](https://github.com/fdac/Project2/MSR2009_0113_mockus_audris.pdf)
   In 6th IEEE Working Conference on Mining Software Repositories,
   May 16-17 2009
1. [Lean GHTorrent: GitHub Data on Demand](https://github.com/fdac/Project2/p384-gousios.pdf)
   In Proceedings of the 11th Working Conference on Mining Software
   Repositories, MSR 2014 (384–387)
1. [The relationship between folder use and the number of forks: A case study on github repositories](https://github.com/fdac/Project2/folder-short.pdf). In
   ESEM, Torino, Italy, September 2014.