#!/bin/bash

cd /Users/ypinglai/Workspaces/UOEO/dissertation

source ./venv/bin/activate
cd spiders/jobsdb

scrapy crawl jobsdb_advertisements
