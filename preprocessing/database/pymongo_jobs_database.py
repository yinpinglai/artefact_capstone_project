import pymongo
import datetime

class PyMongoJobsDatabase:

    def __init__(self) -> None:
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['dissertation']
        self.collection = self.db['jobs']

    def retrieve_all_jobs(self) -> list[dict]:
        try:
            retrieve_jobs_result = self.collection.find()
            return list(retrieve_jobs_result)
        except:
            print("Error while executing retrieving job advertisement records form database\n")
        return []

    def retrieve_unprocessed_jobs(self) -> list[dict]:
        try:
            retrieve_unprocessed_jobs_result = self.collection.find({
                '$or': [
                    {'has_processed_manually': {'$exists': False}},
                    {'has_processed_manually': {'$eq': False}}
                ]
            })
            return list(retrieve_unprocessed_jobs_result)
        except:
            print("Error while executing retrieving unprocessed jobs\n")
        return []
        
    def retrieve_processed_jobs(self, last_updated_at) -> list[dict]:
        try:
            retrieve_processed_jobs_result = self.collection.find({
                'has_processed_manually': { '$eq': True },
                '$or': [
                    {'has_processed_automatically': {'$exists': False}},
                    {'has_processed_automatically': {'$eq': False}}
                ],
                'updated_at': { '$gte': last_updated_at },
            })
            return list(retrieve_processed_jobs_result)
        except:
            print("Error while executing retrieving processed jobs which are greater than or equal to {}\n"
                    .format(last_updated_at))
        return []
    
    def update_job_description_text(self, data) -> bool:
        try:
            data['updated_at'] = datetime.datetime.now()
            updated_result = self.collection.update_one(
                {'id': data['id']},
                {'$set': {
                    'has_processed_automatically': True,
                    'updated_at': data['updated_at'],
                    'tokenized_job_description': data['tokenized_job_description'],
                    'job_description_text_processed': data['job_description_text_processed'],
                }},
                upsert=False,
            )
            return updated_result.modified_count > 0
        except:
            print("Error while updating a processed job: {}\n".format(data['id']))
        return False

    def update_job_description_html(self, data) -> bool:
        try:
            data['updated_at'] = datetime.datetime.now()
            updated_result = self.collection.update_one(
                {'id': data['id']},
                {'$set': {
                    'has_processed_manually': True,
                    'updated_at': data['updated_at'],
                    'job_description_html_processed': data['job_description_html_processed'],
                }},
                upsert=False,
            )
            return updated_result.modified_count > 0
        except:
            print("Error while updating an unprocessed job: {}\n".format(data['id']))
        return False

    def remove_job_record(self, id) -> bool:
        try:
            deleted_result = self.collection.delete_one(
                {'id': id},
            )
            return deleted_result.deleted_count > 0
        except:
            print("Error while deleting a job record: {}\n".format(id))
        return False
