import re, json, pymongo
import gzip, sys, os, shutil, pickle

def parse(text, name):
  size = 0
  data = {}
  data['name'] = decode(name)
  data['commits'] = []
  if text == '':
    return (0, {}, {})
  last_revision = ''
  authors = {}
  delta = 0
  files = {}
  text = text .replace('\r', '')
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
      authors [decode(props[5])] = 1
      files [decode(props[3])] = 1
      delta += 1
  else:
    # It's Git
    size += len (text)
    lines = text.splitlines()
    commit = {}
    for line in lines:
      props = line.split(';')
      revision = props[0]
      authors [decode(props[3])] = 1
      if len (props) > 8:
        files [decode(props[8])] = 1
      else: sys.stderr.write ('Bad format:' + ';'.join(props) + '\n')
      delta += 1
  return delta, authors, files

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
  deltas = db['measures']
  # Get list of files
  files = open('mlist', 'r').readlines()
  counter = 0
  for f in files:
    f = f.strip()
    name = f .replace ('bitbucket.org_', '') .replace ('.delta.gz', '')
    print f,
    contents = gzip.open(delta_dir + f).read()
    delta,authors,files = parse(contents, name)
    na = len(authors.keys())
    nf = len(files.keys())
    print f + ';' + name + ';' + str(delta) + ';' + str(na)+ ';' + str(nf) + ';' + ':'.join (authors.keys()) + ';' + ':'.join(files.keys())
	    
