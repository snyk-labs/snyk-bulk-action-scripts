import sys
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

orgfile = sys.argv[1]

int_name = sys.argv[2]

setting = sys.argv[3]

set_val = sys.argv[4]

# we let json parse this to ensure this is a real datatype
set_val = json.loads(str(set_val).lower())

orgs = jopen(orgfile)

def filter_int(integration, int_name, setting, set_val):
    if integration['name'] == int_name and setting in integration['settings']:
        # n_set = str(integration['settings'][setting]).lower()
        # n_val = str(set_val).lower()
        n_set = integration['settings'][setting]
        n_val = set_val
        if n_set == n_val:
            return True
    return False

def check_int (integrations, int_name, setting, set_val):
    return [i for i in integrations if filter_int(i, int_name, setting, set_val)]

for org in orgs:
    integrations = check_int(org['integrations'], int_name, setting, set_val)
    org['integrations'] = integrations

orgs = [o for o in orgs if len(o['integrations']) > 0]

jprint(orgs)