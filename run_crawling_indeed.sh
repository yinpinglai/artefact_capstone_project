#!/bin/bash

cd /Users/ypinglai/Workspaces/UOEO/dissertation

source ./venv/bin/activate
cd spiders/indeed

scrapy crawl indeed_advertisements
