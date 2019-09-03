# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

def get_k8s_owners_data():

    # Usage: k8s_owners_data gh_key raw_github_url
    # Example: k8s_owners_data.py gh_key https://raw.githubusercontent.com/kubernetes-sigs/kubefed/master/OWNERS

    import sys
    import yaml
    from github import Github

    from common_gh_functions import read_key, download_file, username_details

    # Read arguments
    gh_key = str(sys.argv[1])
    url = str(sys.argv[2])

    # Read GitHub API key from file and create a github instance using that key
    key = read_key(gh_key)
    g = Github(key)

    filename = download_file(url)

    stream = open(filename, 'r')
    yaml_file = yaml.safe_load(stream)

    try:
        print('\nApprovers:')
        for username in yaml_file['approvers']:
            try:
                name, company = username_details(g, username)
                print(username, name, company) 
            except:
                print(username)

        print('\nReviewers:')
        for username in yaml_file['reviewers']:
            try:
                name, company = username_details(g, username)
                print(username, name, company)
            except:
                print(username)
    except:
        print('Cannot get users and companies')


get_k8s_owners_data()
