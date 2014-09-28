# This script outputs the size for 
# each public project on BitBucket

import json, requests

jsonDict = {}
url = 'https://api.bitbucket.org/2.0/repositories/?pagelen=100'

while True: 
  r = requests.get (url)
  t = r.text
  jsonDict = json.loads (t)
  for myIterator in jsonDict['values']:
    (scm, name, size, has_issues, created, updated) = ('', '', '', '', '', '') 
    for key, value in myIterator.iteritems(): 
      if key == 'scm':
        scm = value
      if key == 'size':
        size = str(value)
      if key == 'full_name':
        name = value
      if key == 'created_on':
        created = value
      if key == 'updated_on':
        updated = value
      if key == 'has_issues':
        has_issues = str(value)
    print size+';'+scm+';'+has_issues+';'+created+';'+updated+';'+name
  if 'next' not in jsonDict: break
  else: url = jsonDict['next']
