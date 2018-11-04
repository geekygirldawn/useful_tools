def get_user_repo_events():

    # Usage: user_events_by_repo.py key_filename gh_username repo_string
    # Example: user_events_by_repo.py gh_key geekygirldawn chaoss
    # key_filename is the path to a file containing your GitHub API key as one line

    # Limitation - this uses the event API, which is limited to the past 3 months of activity data

    # Note: If you just want the list of URLs without duplicate events per URL you can use:
    # | grep http | uniq

    # For all events across all repos use 'ALL' as the repo_string
    # Example: user_events_by_repo.py key_filename gh_username ALL

    import sys
    from github import Github # Uses https://github.com/PyGithub/
    from common_gh_functions import read_key

    # Read arguments
    key_filename = str(sys.argv[1])
    username = str(sys.argv[2])
    repo_string = str(sys.argv[3])

    # Make sure people know exactly what they are getting
    print('\n\nReading events from past 3 months for', username, 'in repos matching', repo_string, '\n')

    # Read GitHub API key from file and create a github instance using that key
    key = read_key('gh_key')
    g = Github(key)

    # Reads all events over the past 3 months for this user
    person = g.get_user(username).get_events()

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
                print('Other event type:', event.type,
                       event.repo.url)
            count+=1

    print("Number of events", count)

get_user_repo_events()
    
