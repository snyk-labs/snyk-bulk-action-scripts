import sys
import json
import os

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

org_dir = sys.argv[1]
int_name = sys.argv[2].lower()
setting = sys.argv[3].lower()
set_val = sys.argv[4]

# we let json parse this to ensure this is a real datatype
set_val = json.loads(str(set_val).lower())

# we're loading all our orgs from disk
# print(f'loading org data from {org_dir}')
orgs: list = []
for root, dirs, files in os.walk(org_dir): 
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root,file)
            orgs.append(jopen(file_path))

# this is here to simplify matching without modifying the result
# makes all strings recursively lowercase in the dictionary passed to it
def to_lower(cap: dict) -> dict:
    lower = {}
    for key,value in cap.items():
        if isinstance(value, dict):
            value = to_lower(value)
        if isinstance(key, str):
            key_lower = key.lower()
        lower[key_lower] = value
    return lower

def filter_int(integration, int_name, setting, set_val):
    lower_int = to_lower(integration)
    if lower_int['name'] == int_name and setting in lower_int['settings']:
        n_set = lower_int['settings'][setting]
        n_val = set_val
        if n_set == n_val:
            return True
    return False

def check_int (integrations, int_name, setting, set_val):
    return [i for i in integrations if filter_int(i, int_name, setting, set_val)]

# for every org, remove every integration that doesn't match our filter
for org in orgs:
    integrations = check_int(org['integrations'], int_name, setting, set_val)
    org['integrations'] = integrations

# now remove any org that has no integrations left
orgs = [o for o in orgs if len(o['integrations']) > 0]

# these are the only orgs (and integrations) that match our filter
jprint(orgs)