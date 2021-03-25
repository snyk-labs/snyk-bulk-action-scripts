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

# grab token
snyktoken = os.environ['SNYK_TOKEN']

# very janky settings config
orgfile = sys.argv[1]
int_name = sys.argv[2]
setting = sys.argv[3]
set_val = sys.argv[4]

orgs = jopen(orgfile)

set_val = json.loads(str(set_val).lower())
setting = str(setting)

new_setting = {setting: set_val}

client = snyk.SnykClient(snyktoken)

for org in orgs:
    org_id = org['id']
    org_name = org['name']
    for integration in org['integrations']:
        int_id = integration['id']
        name = integration['name']
        # this check is technically redundant, but want to make sure before we update anything
        if name == int_name:
            callurl = f'org/{org_id}/integrations/{int_id}/settings'
            notice = f'updating {name} integration for org {org_name}'
            print(notice)
            resp = client.put(callurl, new_setting)
            if resp.status_code == 200:
                print(f'{org_name} has had setting of {setting} for {name} set to {set_val}')
            else:
                print(f'{org_name} failed to have setting changed, error {resp.status_code}')
       
print('done')