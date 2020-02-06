# Copyright (C) 2020 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Requires:
#   - gh_key file in the same directory as the script containing a valid github key
#   - repos.csv file containing a comma separated list of org,repo pair on each line with no header

# Output:
#   - outputs a repo_data.csv file with results, including partial results if an api call failed.
#   - prints errors to the screen

def build_repo_list(filename):

    import csv

    repo_list = []

    with open(filename, 'r') as csv_file:
        output = csv.reader(csv_file)
        for line in output:
            repo = line[0] +  '/' + line[1]
            repo_list.append(repo)

    return repo_list

def get_repo_data():
    import time, string
    from github import Github # Uses https://github.com/PyGithub/
    from common_gh_functions import read_key

    # read csv with org,repo and reformat as list of org/repo for api
    repo_list = build_repo_list('repos.csv')

    # read key from file named gh_key in the current dir
    key = read_key("gh_key")
    g = Github(key)

    # create csv output file and write header line
    csv_output = open('repo_data.csv', 'w')
    csv_output.write('Project,Repo URL,Last Commit Date,Last Commit Author,Issues Needing Attention,PRs Needing Attention,Stars,Forks,Last Release (date),Contributors,Private\n') 

    rate_threshold = 5

    for repo_string in repo_list:

        if g.rate_limiting[0] < rate_threshold:
            print("Exiting: API rate limit reached - reset could take an hour")
            break

        print('Processing:', repo_string)

        try:
            repo = g.get_repo(repo_string)
            csv_output.write(repo_string)
            csv_output.write(',')

            url = repo.html_url
            csv_output.write(url)
            csv_output.write(',')

            recent_commit = repo.get_branch(repo.default_branch).commit.commit
            recent_commit_date = str(recent_commit.author.date)
            csv_output.write(recent_commit_date)
            csv_output.write(',')
            recent_commit_author = str(recent_commit.author.email)
            csv_output.write(recent_commit_author)
            csv_output.write(',')
            
            
            # Note: repo.open_issues_count also contains open pull requests, so need to subtract PRs to separate nums
            open_all_num = repo.open_issues_count
            open_prs = repo.get_pulls(state='open')
            open_prs_num = len(list((open_prs))) # very expensive operation, esp for large repos with lots of open PRs
            csv_output.write(str(open_prs_num))
            csv_output.write(',')

            open_issues_num = open_all_num - open_prs_num
            csv_output.write(str(open_issues_num))
            csv_output.write(',')

            stars = str(repo.stargazers_count)
            csv_output.write(str(stars))
            csv_output.write(',')

            forks = str(repo.forks_count)
            csv_output.write(str(forks))
            csv_output.write(',')

            try:
                recent_release_date = str(repo.get_latest_release().created_at)
                csv_output.write(str(recent_release_date))
                csv_output.write(',')
            except:
                csv_output.write(',')
                
            contributors = str(len(list(repo.get_contributors())))
            csv_output.write(str(contributors))
            csv_output.write(',')

            private = str(repo.private)
            csv_output.write(private)
            csv_output.write('\n')


#            line = ",".join([repo_string,  url, recent_commit_date, str(open_issues_num), str(open_prs_num), stars, forks, recent_release_date, contributors]) + "\n"
        except:
            print('incomplete or missing data for', repo_string)
            csv_output.write('\n')



get_repo_data()
