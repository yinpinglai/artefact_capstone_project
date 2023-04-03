#!/bin/bash

cd /Users/ypinglai/Workspaces/UOEO/dissertation

source ./venv/bin/activate
cd spiders/indeed

log_folder=./logs/indeed
log_file=$(date +%Y%m%d_%H%M%S).log
echo "The application will export log messages into $log_file"

mkdir -p $log_folder
touch $log_folder/$log_file
scrapy crawl indeed_advertisements --logfile $log_folder/$log_file
