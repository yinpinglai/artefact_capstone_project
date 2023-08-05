# MSc of Computer Science - Capstone Project
## Installation
- Latest Docker Engine
- Python 3.7+

## Quick Start
1. Install Virtual Environment
```
$ pip3 install virtualenv
```
2. Create a virtual environment
```
$ python3 -m venv ./venv
```
3. Activate the virtual environment
```
$ source ./venv/bin/activate
```
4. Install all dependencies
```
$ pip3 install -r ./requirements.txt
```

## Stand up MongoDB in Docker
```
$ cd ./docker
$ docker-compose up -d
```

## Crawling data from Indeed
```
$ cd ./spiders/indeed
$ scrapy crawl indeed_advertisements --logfile ./logs/output.log
```

## Crawling data from JobsDB
```
$ cd ./spiders/jobdb
$ scrapy crawl jobsdb_advertisements --logfile ./logs/output.log
```
