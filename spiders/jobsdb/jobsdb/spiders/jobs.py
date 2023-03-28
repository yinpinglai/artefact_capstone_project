import re
import scrapy

from scrapy.http import Request, Response
from jobsdb.utils.json_utils import JSONUtils

class JobsDBAdvertisementsSpider(scrapy.Spider):

    name = "jobsdb_advertisements"

    base_url = "https://hk.jobsdb.com"
    
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv'}}
    }

    EMPTY_SPACE_REGEX = re.compile('\s')

    @classmethod
    def get_search_url(cls, keyword: str, page_num: int):
        '''
        Get the URL for searching jobs on JobsDB.

        Parameters:
        keyword: str - The search keyword
        page_num: int - The target pagination number

        Returns:
        search_url: str - The URL for searching jobs on JobsDB.
        '''
        return '{}/hk/search-jobs/{}/{}'.format(cls.base_url, keyword, str(page_num))
    
    @classmethod
    def get_search_keyword(cls, keywords: list[str]) -> str:
        '''
        Get the search keyword by the keyword list for searching on JobsDB. Perform below
        actions to create the search keyword string:
        - Replace all empty space with '-'
        - Convert the keyword to lower case
        - Join all keywords with '-'

        Parameters:
        keywords: list[str] - The keyword list

        Returns:
        keyword: str - The search keyword
        '''
        return '-'.join([cls.EMPTY_SPACE_REGEX.sub('-', keyword.lower()) for keyword in keywords])

    
    def start_requests(self) -> None:
        '''
        Before starts the job of crawling job advertisements on JobsDB
        '''
        keywords_combination_list = JSONUtils.load_keywords_json()

        for keywords in keywords_combination_list:
            search_keyword = JobsDBAdvertisementsSpider.get_search_keyword(keywords=keywords)
            search_job_url = JobsDBAdvertisementsSpider.get_search_url(keyword=search_keyword, page_num=1)
            yield scrapy.Request(
                url = search_job_url,
                callback = self.parse_advertisement_list,
                meta = {
                    'keyword': search_keyword,
                    'page_num': 1,
                }
            )
    
    def parse_advertisement_list(self, response: Response) -> Request:
        '''
        Parse the response of the advertisement list from JobsDB

        Parameters:
        response: scrapy.http.Response - The response instance which is received from JobsDB

        Returns:
        request: scrapy.http.Request - The request for querying the details of the job advertisement
        '''
        keyword = response.meta['keyword']
        job_advertisements = response.xpath('//*[@id="jobList"]/div/div[2]/div/div')

        for job_advertisement in job_advertisements:
            meta = job_advertisement.xpath('./@data-search-sol-meta').get()
            meta_dict = JSONUtils.get_dict_from(meta)
            job_id = meta_dict['jobId']

            advertisement_url_selector = job_advertisement.xpath('./div/div/article/div/div/div[1]/div[1]/div[2]/h1/a/@href')
            advertisement_url = '{}/{}'.format(JobsDBAdvertisementsSpider.base_url, advertisement_url_selector.get())

            posted_at = job_advertisement.xpath('//time/@datetime').get()

            yield scrapy.Request(
                url = advertisement_url,
                callback = self.parse_advertisement_details,
                meta = {
                    'job_id': job_id,
                    'keyword': keyword,
                    'posted_at': posted_at,
                }
            )

    def parse_advertisement_details(self, response: Response) -> dict:
        '''
        Parse the response of the details of advertisement from JobsDB

        Parameters:
        response: scrapy.http.Response - The response instance which is received from JobsDB

        Returns:
        job_advertisement: dict - The job advertisement data
        '''
        job_id = response.meta['job_id']
        posted_at = response.meta['posted_at']
        keyword = response.meta['keyword']
        content_container_selector = response.xpath('//*[@id="contentContainer"]')
        header_selector = content_container_selector.xpath('//div/div/div[1]')
        content_selector = content_container_selector.xpath('//div/div/div[2]')

        yield {
            'id': job_id,
            'url': response.url,
            'keyword': keyword,
            'posted_at': posted_at,
            'job_title': header_selector.xpath('//div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/h1/text()').get(),
            'location': header_selector.xpath('//div[2]/div[1]/div/div/div[2]/div/div/div/div[1]/div/span/text()').get(),
            'job_description_html': content_selector.xpath('//div/div[1]/div/div[2]/div/div[2]/div/span/div').get(),
        }
