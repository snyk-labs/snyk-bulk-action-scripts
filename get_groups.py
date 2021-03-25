import snyk
import os
import json

def jprint(something):
    print(json.dumps(something,indent=2))

def jwrite(contents,filename):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, indent=2)

def jw(contents,filename):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile)

def jopen(filename):
    with open(filename, 'r') as infile:
        contents = json.load(infile)
    return contents


snyktoken = os.environ['SNYK_TOKEN']

client = snyk.SnykClient(snyktoken)

me_resp = client.get('user/me')
me_resp = json.loads(me_resp.text)

# we don't actually have a list of groups, but we can extract it from orgs
orgs: list = me_resp['orgs']
orgs = [(o['group']['name'], o['group']['id']) for o in orgs if o['group']]
groups = dict(orgs)
jprint(groups)

