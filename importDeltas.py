import re, json, pymongo
import gzip, sys, os, shutil, pickle

def parse(text, name):
    size = 0
    data = {}
    data['name'] = decode(name)
    data['commits'] = []
    if text == '':
        return (data, 0)
    last_revision = ''
    text .replace ('\r', '')
    # Determine if it uses Git
    if text.find('ENDOFCOMMENT') > 0 and text[:text.find(';')].find(':') > 0:
        # It's Mercurial
        changes = text.strip().split('ENDOFCOMMENT\n')
        commit = {}
	size += len (text)
        for change in changes:
            splits = change.split(';')
            # There may be semicolons in the comments too
            props = splits[:7]
            comment = ';'.join(splits[7:])
            revision = props[0]
            if revision != last_revision:
                # Save old commit
                data['commits'].append(commit)
                # Build a new commit
                commit = {}
                commit['revision'] = revision
                commit['vcs'] = 'hg'
                
                commit['parent'] = props[1]
                commit['branch'] = props[2]
                commit['date'] = props[4]
                commit['author_login'] = decode(props[5])
                commit['author'] = decode(props[6])
                commit['comment'] = decode(comment.strip())
                commit['files'] = []
                commit['files'].append({'name':decode(props[3])})
                last_revision = revision
            else:
                # Just add to files
                commit['files'].append({'name':decode(props[3])})
    else:
        # It's Git
	size += len (text)
        lines = text.splitlines()
        commit = {}
        for line in lines:
            props = line.split(';')
            revision = props[0]
            if revision != last_revision:
                # Save old commit
                data['commits'].append(commit)
                # Build a new commit
                commit = {}
                commit['revision'] = revision
                commit['vcs'] = 'git'
                commit['author'] = decode(props[1])
                commit['committer'] = decode(props[2])
                commit['author_login'] = decode(props[3])
                commit['committer_login'] = decode(props[4])
                commit['author_time'] = props[6]
                commit['committer_time'] = props[7]
                commit['comment'] = decode(';'.join(props[9:]).strip())
                locs = props[5].split(':')
                commit['files'] = []
                commit['files'].append({'name': decode(props[8]), 'loc_added': locs[0], 'loc_deleted': locs[1]})
                last_revision = revision
            else:
                # Just add to files
                locs = props[5].split(':')
                commit['files'].append({'name': decode(props[8]), 'loc_added': locs[0], 'loc_deleted': locs[1]})

    return data, size

def chunks(l, n):
    if n < 1: 
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]

def decode(text):
    return str(text).encode('string_escape')

if __name__ == '__main__':
    delta_dir = 'delta/'
    client = pymongo.MongoClient(host="da0.eecs.utk.edu")
    db = client['bitbucket']
    deltas = db['deltas']
    # Get list of files
    filenames = open('deltas.todo', 'r').readlines()
    counter = 0
    for filename in filenames:
        filename = filename.strip()
        print filename,
        contents = gzip.open(delta_dir + filename).read()
        delta, size = parse(contents, filename.replace('.delta.gz', '').replace('bitbucket.org_', ''))
        # size = sys.getsizeof(delta)
        #size += sys.getsizeof(pickle.dumps(delta))
        size += sys.getsizeof(delta)
        try:
		if size < 16777216 / 3:
            		deltas.insert(delta)
        	else:
            		s = size
            		n = 3 * s / 16777216
            		i = 0
            		for ch in chunks(delta['commits'], n):
                		deltas.insert({'name': delta['name'], 'commits': ch, 'chunk': i})
                		i += 1
        	print counter
        	sys.stdout.flush()
        	counter += 1
	except Exception as e:
		print 'error'
		sys.stderr.write (filename + " could not store\n")	
    
