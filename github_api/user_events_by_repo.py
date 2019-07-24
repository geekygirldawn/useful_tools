# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Get a list of events (pull request, issues, comments, etc.) by a specific user within
# a specific repository search string or across all repositories for the past 3 months

def get_user_repo_events():

    # Usage: user_events_by_repo.py gh_key gh_username repo_string
    # Example: user_events_by_repo.py gh_key geekygirldawn chaoss
    # gh_key is the path to a file containing your GitHub API key as one line

    # Limitation - this uses the event API, which is limited to the past 3 months of activity data

    # For all events across all repos use 'ALL' as the repo_string
    # Example: user_events_by_repo.py gh_key gh_username ALL

    # If you just want a list of unique sorted urls for the events, add this when you call the script
    # | sed 's/^.*http/http/' | sort -u
    # Example: user_events_by_repo.py gh_key geekygirldawn chaoss | sed 's/^.*http/http/' | sort -u

    import sys
    from github import Github # Uses https://github.com/PyGithub/
    from common_gh_functions import read_key

    # Read arguments
    gh_key = str(sys.argv[1])
    username = str(sys.argv[2])
    repo_string = str(sys.argv[3])

    # Read GitHub API key from file and create a github instance using that key
    #key = read_key('gh_key')
    key = read_key(gh_key)
    g = Github(key)

    # Gets person's name and reads all events over the past 3 months for this user
    name = g.get_user(username).name
    person = g.get_user(username).get_events()

    # Make sure people know exactly what they are getting
    print('\n\nReading events from past 3 months for', name, username, 'in repos matching', repo_string, '\n')

    # Loop through events, count them, and print details about each event
    count = 0

    for event in person:
        if (repo_string in event.repo.url) or (repo_string == 'ALL'):

            if ('Issue' in event.type):
                print(event.created_at, event.type, event.payload['action'], 
                      event.payload['issue']['html_url'])
            elif ('Pull' in event.type):
                print(event.created_at, event.type, event.payload['action'], 
                      event.payload['pull_request']['html_url'])
            else:
                # Wrapped print in try / except since not every event has an html url
                try:
                    print(event.created_at, event.type,
                          event.repo.html_url)
                except:
                    print(event.created_at, event.type, event.repo.url)

            count+=1

    print("Number of events", count)

get_user_repo_events()
    
