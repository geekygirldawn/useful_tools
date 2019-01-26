#!/bin/bash

# Copyright (C) 2015 Dawn M. Foster
# Licensed under GNU General Public License (GPL), version 3 or later: http://www.gnu.org/licenses/gpl.txt

# Examples
# ./quick_file_backup.sh --source_path /Volumes/GoogleDrive/My\ Drive/Presentations_and_Events/ --dest_path ~/Documents/file_backup/
# ./quick_file_backup.sh --source_path /Volumes/GoogleDrive/My\ Drive/Presentations_and_Events/FOSDEM_2019/ --dest_path ~/Dropbox/Backups/ --versioning

# --versioning		Use if you want the files dropped into timestamped dirs (leaves a bajillion dirs to clean up)
# --source_path 	Path where the files exist now - include trailing slash
# --dest_path		Path where the copied files will live - include trailing slash

# Set Defaults
VERSIONING=0
DATE=`date +%Y-%m-%d-%H-%M-%S`

# Read arguments from the command line and store them in variables

while [[ $# > 0 ]]
do
key="$1"

case $key in
     --versioning)
     VERSIONING=1
     shift
     ;;
     --source_path)
     SOURCE_PATH="$2"
     shift
     ;;
     --dest_path)
     DEST_PATH="$2"
     shift
     ;;
        *)
            # unknown option
     ;;
esac

shift
done

if [ $VERSIONING = 1 ]; then
    cp -R "$SOURCE_PATH" "$DEST_PATH"$DATE
else
    cp -R "$SOURCE_PATH" "$DEST_PATH"
fi


