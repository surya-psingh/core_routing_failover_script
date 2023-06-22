import yaml
import json
import os
import requests
from datetime import datetime


LOCAL_DIR = "/tmp"
GIT_SSH = "git@github.com:surya-psingh/core_routing_failover_script.git"

# Load input data
with open('core_routing/input.json') as f:
    input_data = json.load(f)

# Get username from JSON
username = input_data['user']
# Get the reason for failover
reason = input_data['reason']
# Get the ticket number for the issue
ticket = input_data['issue'].split('/')[-1]
cur_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
new_branch = ticket + "_" + cur_date_time
repo_path = LOCAL_DIR + '/' + new_branch


def create_pull_request(username, reason):

    # set up the repository and branch names
    repo_owner = "surya-psingh"
    repo_name = "core_routing_failover_script"
    source_branch = new_branch
    target_branch = "main"

    # set up the API endpoint URL and authentication token
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    auth_token = "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"

    # set up the request headers and body
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {
        "title": reason,
        "head": source_branch,
        "base": target_branch,
        "body": f"Initiated b {username}"
    }

    # make the API call to create the pull request
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    # check if the request was successful
    if response.status_code == 201:
        print("Pull request created successfully!")
    else:
        print(f"Error creating pull request: {response.text}")


def git_init():
    os.chdir(LOCAL_DIR)
    print(f"Changing directory to {LOCAL_DIR}")
    print(f"Repo path is {repo_path}")
    try:
        os.mkdir(new_branch)
        os.system(f"git clone {GIT_SSH} {repo_path}")
    except FileExistsError as e:
        print("Folder already exists")
    finally:
        os.chdir(repo_path)
        os.system(f"git checkout -b {new_branch}")


def git_operations():
    os.chdir(repo_path)
    os.system("git add .")
    os.system("git commit -m 'Records updated successfully'")
    os.system(f"git push -u origin {new_branch}")


def check_and_update_states():
    updated_status = False
    desired_state = input_data['state']
    for datacenter in desired_state.keys():

        RECORDS_FILE = f"{repo_path}/p8t.us/subdomains/view-{datacenter}/records.yml"

        state = {datacenter: desired_state[datacenter]}
        # Load records data
        with open(RECORDS_FILE) as f:
            records = yaml.safe_load(f)

        tags = ["production"]

        # Filter records by tags
        filtered_records = {}
        for record, record_data in records.items():
            if all(tag in record_data.get('tags', []) for tag in tags):
                filtered_records[record] = record_data

        # Get state of each region
        for region, region_data in state.items():
            for record, record_data in filtered_records.items():
                for dc in region_data:
                    if dc in record_data['options'].keys():
                        options_data = record_data.get('options', {}).get(dc)
                        if options_data.get('enabled') and (region_data.get(dc) == 'disabled'):
                            # Update state to disabled
                            options_data['enabled'] = False
                            print(
                                f"Record {record}, region {dc} updated to disabled.")
                            updated_status = True
                        elif not options_data.get('enabled') and (region_data.get(dc) == 'enabled'):
                            # Update state to enabled
                            options_data['enabled'] = True
                            print(
                                f"Record {record}, region {dc} updated to enabled.")
                            updated_status = True

        # Update records with filtered records
        records.update(filtered_records)

        # Save updated records file
        with open(RECORDS_FILE, 'w') as f:
            yaml.dump(records, f)
    return updated_status


if __name__ == "__main__":
    git_init()
    status = check_and_update_states()
    if status:
        git_operations()
        create_pull_request(username, reason)
    else:
        print("No changes were made.")