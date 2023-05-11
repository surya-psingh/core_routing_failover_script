import yaml
import json

# Load input data
with open('core_routing_failover_script/input.json') as f:
    input_data = json.load(f)
desired_state = input_data['state']

for datacenter in desired_state.keys():

    RECORDS_FILE = f"core_routing_failover_script/p8t.us/subdomains/view-{datacenter}/records.yml"

    state = {datacenter: desired_state[datacenter]}
    print(state)
    # Load records data
    with open(RECORDS_FILE) as f:
        records = yaml.safe_load(f)

    tags = ["production"]

    # Get username from JSON
    username = input_data['user']

    # Filter records by tags
    filtered_records = {}
    for record, record_data in records.items():
        if all(tag in record_data.get('tags', []) for tag in tags):
            filtered_records[record] = record_data

    # Get state of each region
    for region, region_data in state.items():
        for record, record_data in filtered_records.items():
            for dc in region_data:
                options_data = record_data.get('options', {}).get(dc)
                if options_data.get('enabled') and (region_data.get(dc) == 'disabled'):
                    # Update state to disabled
                    options_data['enabled'] = False
                    print(f"Record {record}, region {dc} updated to disabled.")
                elif not options_data.get('enabled') and (region_data.get(dc) == 'enabled'):
                    # Update state to enabled
                    options_data['enabled'] = True
                    print(f"Record {record}, region {dc} updated to enabled.")

    # Update records with filtered records
    records.update(filtered_records)

    # Save updated records file
    with open(RECORDS_FILE, 'w') as f:
        yaml.dump(records, f)
