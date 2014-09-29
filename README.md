Project2a
========

Retrieve and store BitBucket VCS
----------------------------------

Investors were intrigued by the presentation on the prospects of 
DeveloperParadise, but had a few questions. 

1. How accurate is the language specification in the project description?
2. What are the types of applications being built on BitBucket?
3. Why is there such a rapid growth of Ruby projects (e.g., are they being moved from other forges)?
4. Why the comparison was made only with the BitBucket, not the market leader GitHub or older players like GoogleCode or SourceForge?

They agreed to provide limited funding to your teams to investigate these questions further.
In particular, they provided $1700 in AWS credits and sufficient storage space for you to complete this investigation.  

Project2a will focus on retrieving and storing data that would enable answering these (and related) questions 
in Project2b. 

The investors are a bit impatient and want a brief technical readout of how the data retrieval is going in one week. They would like to know if the mone is used wisely, in particular, they would like to know how many MB of repository data is retrieved per $ of the provided funding, how long it will take to get all the data, 
and what approaches will be used to analyze it.

To speed up the process, the tasks will be distributed among newly formed seven teams.
Each team will find a list of repositories that they need to retrieve in 
file 'divided' (columns team  number, type of vcs, and the 
name of the repository are semicolon separated).

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


