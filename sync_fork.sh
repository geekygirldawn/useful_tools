#!/bin/bash

# Copyright (C) 2018 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Need to set upstream first using something like:
# git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git
 
# Quick Script to sync a fork from Github with the latest
# changes from the upstream project. This is mostly to prevent me from
# forgetting that last step of pushing the changes.

git fetch upstream
git checkout master
git merge upstream/master
git push origin master
