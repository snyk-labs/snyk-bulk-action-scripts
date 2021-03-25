import snyk
import os
import json
import sys

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
snykgroup = os.environ['SNYK_GROUP']

orgfile = sys.argv[1]

client = snyk.SnykClient(snyktoken)

print('retrieving list of organizations')
orgs_resp = client.get("orgs")
orgs_resp = json.loads(orgs_resp.text)

orgs: list = orgs_resp['orgs']

# filter that errant fake org & ensure we're only working with one group
orgs = [o for o in orgs if o['group'] ]
orgs = [o for o in orgs if o['group']['id'] == snykgroup ]

org_ids: list = []

def get_int_settings(org_id,integrations,client):
    int_set= []
    for k,v in integrations.items():
        print(f'getting settings for {k}')
        tmp_dict = {}
        tmp_dict['id'] = v
        urlcall = f'org/{org_id}/integrations/{v}/settings'
        resp = client.get(urlcall)
        settings = json.loads(resp.text)
        tmp_dict['settings'] = settings
        tmp_dict['name'] = k
        int_set.append(tmp_dict)
    return int_set

# get integration IDs
def get_org_integrations(orgs, client):
    for org in orgs:
        id = org['id']
        name = org['name']
        print(f'getting list of integrations in {name}')
        urlcall = f'org/{id}/integrations'
        resp = client.get(urlcall)
        integrations = json.loads(resp.text)
        integrations = get_int_settings(id,integrations,client)
        org['integrations'] = integrations
        slug = org['slug']
        fname = f'org_cache/{slug}.json'
        jwrite(org,fname)
    return orgs

print('retrieving org settings')
orgs = get_org_integrations(orgs,client)

print(f'writing org list with settings to {orgfile}')
jwrite(orgs,orgfile)
print('done')
