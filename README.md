# core_routing_failover_script
Core Call Routing Failover Tool

1. The script imports necessary modules:
   - `yaml`: for parsing YAML files.
   - `json`: for parsing JSON files.
   - `os`: for interacting with the operating system.
   - `requests`: for making HTTP requests.
   - `logging`: for logging information and errors.
   - `subprocess`: for executing Git commands.
   - `datetime`: for getting the current date and time.

2. Some global variables are defined:
   - `LOCAL_DIR`: the local directory path where the script will work.
   - `GIT_SSH`: the SSH URL of the GitHub repository.
   - `LOG_FILE`: the name of the log file.

3. The logging configuration is set up using the `logging.basicConfig()` function. It specifies the log level, format, and handlers (file and stream).

4. The script tries to load input data from a JSON file named `core_routing/input.json`. If the file is not found or there is an error parsing it, an error message is logged, and the script exits with a non-zero status.

5. The script extracts relevant information from the input data loaded from the JSON file:
   - `username`: the value associated with the key 'user'.
   - `reason`: the value associated with the key 'reason'.
   - `ticket`: the last part of the value associated with the key 'issue'.
   - `cur_date_time`: the current date and time formatted as "day-month-year_hour-minute".
   - `new_branch`: a new branch name created by combining the ticket number and current date/time.
   - `repo_path`: the local directory path for the new branch.

6. The `create_pull_request()` function is defined to create a pull request on GitHub using the GitHub API. It sets up the necessary parameters such as repository owner, repository name, source branch, target branch, API endpoint URL, and authentication token. It sends a POST request with the required headers and data to create the pull request. The response status code is checked, and appropriate log messages are recorded.

7. The `git_init()` function is defined to initialize the local Git repository. It changes the current working directory to `LOCAL_DIR`, creates a new directory with the name `new_branch`, clones the repository from `GIT_SSH` into the `repo_path`, and checks out the new branch. Appropriate log messages are recorded for each step.

8. The `git_operations()` function is defined to perform Git operations. It changes the current working directory to `repo_path`, stages all changes, commits the changes with a predefined message, and pushes the changes to the remote repository. Git commands are executed using `subprocess.run()`. 

9. The `check_and_update_states()` function is defined to check and update the states of certain records based on the desired state provided in the input data. It iterates over the desired state, loads the records data from a YAML file specific to each data center, filters the records based on certain tags, and compares the desired state with the existing options data of the records. If there is a difference, the state is updated, and appropriate log messages are recorded. Finally, the updated records are saved back to the YAML file.

10. The script's main block executes the following steps:
    - Calls the `git_init()` function to initialize the local Git repository.
    - Calls the `check_and_update_states()` function to check and update the states of records. The function returns a boolean indicating whether any changes were made.
    - If there were changes (`status` is `True`), the `

git_operations()` function is called to stage, commit, and push the changes to the remote repository.
    - Finally, if there were changes, the `create_pull_request()` function is called to create a pull request on GitHub.

11. If no changes were made during the process, a log message is recorded stating that no changes were made.

That's the overall flow and functionality of the script. It combines Git operations, YAML file parsing, and GitHub API requests to update records, commit changes, and create a pull request.
