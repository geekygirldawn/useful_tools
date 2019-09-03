# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Functions for use with the GitHub API.

def read_key(file_name):

    # Reads the first line of a file containing the GitHub API key
    # Usage: key = read_key('gh_key')
    # Can also be the full path to the file with key

    with open(file_name, 'r') as kf:
        key = kf.readline().rstrip() # remove newline & trailing whitespace
    return key

def download_file(url,output_file):

    # NOTE: Make sure you pass in the raw file.
    # Example: sig_file = download_file('https://raw.githubusercontent.com/kubernetes/community/master/sigs.yaml', '/tmp/sigs.yaml')

    import wget
    import os
    import shutil
    import random
    
    output_bak = output_file + '_bak_' + str(random.randint(0,1024))

    if os.path.exists(output_file):
        shutil.move(output_file, output_bak)

    sig_file = wget.download(url, out=output_file)
    
    return sig_file



