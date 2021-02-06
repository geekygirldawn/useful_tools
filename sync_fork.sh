#!/bin/bash

# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Need to set upstream first using something like:
# git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git
 
# Quick Script to sync a fork from Github with the latest
# changes from the upstream project. This is mostly to prevent me from
# forgetting that last step of pushing the changes.

# Get branch name as input for branches that are now called main or something else.
# Currently defaults to master, but I should eventually change this when more have moved.

read -p "Branch name [master]: " branch

branch=${branch:-master}

printf "Using branch $branch\n\n"

# Check for unstashed / un-checked in changes

git status

read -p "Do you want to proceed? " -r

if [[ $REPLY =~ ^[Yy]$ ]]
then
    git fetch upstream
    git checkout $branch
    git merge upstream/$branch
    echo 		# print blank line
else
    echo 		# print blank line
    echo "Stopping without sync"
    exit 0
fi

echo 		# print blank line

read -p "Are you ready to push these changes to your local fork? " -r 

if [[ $REPLY =~ ^[Yy]$ ]]
then
    git push origin $branch
else
    echo 		# print blank line
    echo "Stopping without pushing changes"
    exit 0
fi
