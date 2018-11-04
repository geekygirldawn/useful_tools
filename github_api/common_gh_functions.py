def read_key(file_name):

    # Reads the first line of a file containing the GitHub API key
    # Usage: key = read_key('gh_key')
    # Can also be the full path to the file with key

    with open(file_name, 'r') as kf:
        key = kf.readline().rstrip() # remove newline & trailing whitespace
    return key


