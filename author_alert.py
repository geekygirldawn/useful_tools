#!/usr/local/bin/python

# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt
 
# Script that parses a blog feed, looks for a specific author, and sends an email if there is a new 
# post from that author. It's designed to be run under cron.

# CAVEATS: blog feed, author, email, intermediate filenames, and other stuff is hardcoded into 
# this script.

import feedparser
import os,sys
import csv
import sys, getopt

# Read options

try: 
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["path="])

except getopt.GetoptError:
    print 'Path not specified'
    sys.exit(2)

path = ''

for opt, arg in opts:
    if opt in ("-p", "--path"):
        path = arg

# set the full path for output files

out_file_path = path + '/data/out.txt'

# Parse the feed

blogfeed = feedparser.parse('http://thenewstack.io/blog/feed/')

# Read old data into a list for comparison before overwriting file in next step

orig_output_list = []

if os.path.isfile(out_file_path) is True:

    with open(out_file_path, 'rb') as orig_output_file:
        orig_output = csv.reader(orig_output_file, delimiter='|')

        for row in orig_output:
            orig_output_list.append(row[0]) # add title to list

# Initialize new output file (overwrites old if it exists)

output_file = open (out_file_path, 'w')

# Initialize variable used to indicate whether a post is new

new_post = False

# Go through feed to find articles by specified author write them to a pipe separated csv file

for post in blogfeed.entries:
    if post.author == 'Dawn Foster':
        output_file.write('{0}|{1}|{2}|{3}'.format(post.title, post.author, post.published, post.link))

        if post.title not in orig_output_list:
            new_post = True

output_file.close()

# Notify if new_post is True - total hack to use an exec, but c'est la vie :)

if new_post is True:
    os.system('cat /Users/dawn/gitrepos/feed_parsing/data/out.txt | /usr/bin/mail -s "New TNS Post" "geekygirldawn@gmail.com"')


