# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import datetime

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from indeed.utils.html_utils import HTMLUtils

class IndeedPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item=item)

        if adapter.get('job_description_html'):
            adapter['job_description_text'] = HTMLUtils.remove_html_tags(html=adapter['job_description_html'])

        return item

class RemoveDuplicateJobPipeline:

    def __init__(self) -> None:
        self.ids_seen = set()

    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item=item)
        
        if adapter['id'] in self.ids_seen:
            raise DropItem("Duplicated item found: {}".format(item))
        else:
            self.ids_seen.add(adapter['id'])
            return item

class ConvertToLowerCasePipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item=item)

        if adapter.get('job_description_text'):
            adapter['job_description_text'] = adapter['job_description_text'].lower()
    
        return item

class SaveToMongoDBPipeline:

    def __init__(self) -> None:
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['dissertation']
        self.collection = self.db['jobs']

    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item=item)

        item_to_be_persisted = dict(item)
        item_to_be_persisted['source'] = 'indeed'
        item_to_be_persisted['created_at'] = datetime.datetime.now()    
        item_to_be_persisted['updated_at'] = datetime.datetime.now()
        
        try:
            result = self.collection.find({
                'id': item_to_be_persisted['id']
            })

            if len(list(result)) > 0:
                self.collection.update_one(
                    {'id': item_to_be_persisted['id']},
                    {'$set': {
                        'url': item_to_be_persisted['url'],
                        'job_key': item_to_be_persisted['job_key'],
                        'job_title': item_to_be_persisted['job_title'],
                        'location': item_to_be_persisted['location'],
                        'job_description_html': item_to_be_persisted['job_description_html'],
                        'job_description_text': item_to_be_persisted['job_description_text'],
                        'posted_at': item_to_be_persisted['posted_at'],
                        'source': item_to_be_persisted['source'],
                        'updated_at': item_to_be_persisted['updated_at'],
                    }},
                    upsert=False,
                )
            else:
                item_to_be_persisted['has_processed_manually'] = False
                item_to_be_persisted['has_processed_automatically'] = False
                item_to_be_persisted['has_deleted'] = False
                self.collection.insert_one(item_to_be_persisted)

        except:
            print("Unable to create or update a job record: {}".format(
                adapter.get('id')
            ))

        return item
