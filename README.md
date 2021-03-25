## Snyk Bulk Actions Scripts

These are a collection of scripts to edit integration settings for every organization in a group in Snyk.

They use the snyk python library and python 3 to interact gracefully with the Snyk api. The `jq` json querying tool is nice for browsing / parsing if you need it.

Ensure you have "SNYK_TOKEN" and "SNYK_GROUP" environment variables set.

`SNYK_TOKEN` can be a users token or a group service account token. This token must have admin rights to all orgs you want to update.

`SNYK_GROUP` can be found at https://app.snyk.io/ under the Settings -> General for the Group in question

Because this is a bulk action that can change hundreds of organizations, there is a sequence of steps to follow. This is both to make the process fast and to minimize the chances of unintended changes.

1) `get_settings.py` gets every organization in a group and then for the integration settings for each organization. Each organization is saved in a separate file as `org_cache/$organization.json`
2) `filter_orgs.py` takes the folder of organizations created by `get_settings.py` and runs a filter of integration, setting name, and setting value and outputs an array of the organizations matching that filter
3) `put_settings.py` take an array of organizations and the desired integration setting and applies it to each organization

So: get all the organizations, filter through them to build a list of the ones you want to change, and finally make that change.

### Setup
- clone this directory to a machine with python 3.9 on it (even better with pyenv & pipenv installed)
- pip3 install pysnyk
- (optional) if you have jq and snyk cli already working on the workstation this will setup SNYK_TOKEN for you: `export SNYK_TOKEN=$(jq -r '.api' ~/.config/configstore/snyk.json)`
- check that this works by getting a list of groups: `python3 get_groups.py`
- set the group ID with `export SNYK_GROUP=1341234....`


### get_settings.py

If `SNYK_TOKEN` and `SNYK_GROUP` are set correctly, run `python3 get_settings.py` to populate the local cache of organizations and their integration states.

example:
```
❯ python3 get_settings.py
retrieving list of organizations
retrieving org settings
getting list of integrations in Test Organization
writing settings to org_cache/test-organization-fa7.json
getting list of integrations in Sneezing Dog, Inc.
writing settings to org_cache/sneezing-dog-inc.json
getting list of integrations in Broker
writing settings to org_cache/broker-59l.json
getting list of integrations in Angrydome
writing settings to org_cache/angrydome.json
done
```

### filter_orgs.py

This filter script works with the org_cache folder of data. To get a list of organizations that have their gitlab integration with `pullRequestTestEnabled` set to `True` (which will fail PRs if vulnerabilities are present), this is the command:
```
❯ python3 filter_orgs.py org_cache gitlab pullRequestTestenabled "true"
[
  {
    "id": "2bcac16c-650a-406a-b2b2-5c723fbd5593",
    "name": "Sneezing Dog, Inc.",
    "slug": "sneezing-dog-inc.",
    "url": "https://app.snyk.io/org/sneezing-dog-inc.",
    "group": {
      "name": "Chris Barker",
      "id": "dcf9cae3-2f54-4ad2-98af-e70b844657f3"
    },
    "integrations": [
      {
        "id": "78eea8d8-a65b-4ffc-87c4-11a383e57b44",
        "settings": {
          "autoDepUpgradeEnabled": false,
          "autoDepUpgradeIgnoredDependencies": [],
          "autoDepUpgradeLimit": 5,
          "autoRemediationPrs": {
            "freshPrsEnabled": true,
            "backlogPrsEnabled": false,
            "usePatchRemediation": true
          },
          "pullRequestFailOnAnyVulns": false,
          "pullRequestFailOnlyForHighSeverity": false,
          "pullRequestFailOnlyForIssuesWithFix": false,
          "pullRequestTestEnabled": true
        },
        "name": "gitlab"
      }
    ]
  }
]
```

To just get Organization names, one can pipe this into `jq`:
```
❯ python3 filter_orgs.py org_cache gitlab pullRequestTestEnabled True | jq '.[]|.name'
"Sneezing Dog, Inc."
```

Save the full output to a file for the next step, updating those settings:
```
❯ python3 filter_orgs.py org_cache gitlab pullRequestTestEnabled True > to_modify.json
```


### put_settings.py

This takes output of filter_orgs.py and along with the desired integration configuration and applies to the organization in Snyk. When you run this, this script will make changes to organization settings!
```
❯ python3 put_settings.py to_modify.json gitlab pullRequestTestEnabled False
updating gitlab integration for org Sneezing Dog, Inc.
Sneezing Dog, Inc. has had setting of pullRequestTestEnabled for gitlab set to False
done
```

Once this command is done, before trying to run another filter operation, you will need to update the organization cache, running `get_settings.py` again.