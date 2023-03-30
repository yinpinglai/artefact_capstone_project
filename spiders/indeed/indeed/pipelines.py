# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
