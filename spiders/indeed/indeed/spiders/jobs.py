import re
import json
import scrapy

from urllib.parse import urlencode
from scrapy.http import Request, Response
from indeed.utils.json_utils import JSONUtils
from indeed.utils.url_interpreter import URLInterpreter

class IndeedAdvertisementsSpider(scrapy.Spider):

    name = "indeed_advertisements"

    base_url = "https://hk.indeed.com"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv'}}
    }

    @classmethod
    def get_search_url(cls, keyword: str, location: str, offset: int = 0) -> str:
        '''
        Get the URL for searching jobs on Indeed.

        Parameters:
        keyword: str - The search keyword
        location: str - The location for searching
        offset: int - (Optional) The number of pages to be skipped
        '''
        parameters = {
            "q": keyword,
            "l": location,
            "filter": 0,
            "start": offset,
        }
        return '{}/jobs?{}'.format(IndeedAdvertisementsSpider.base_url, urlencode(parameters))
    
    @classmethod
    def get_search_keyword(cls, keywords: list[str]) -> str:
        '''
        Get the search keyword by the keyword list for searching on JobsDB. Perform below
        actions to create the search keyword string:
        - Convert the keyword to lower case
        - Join all keywords with ' '

        Parameters:
        keywords: list[str] - The keyword list

        Returns:
        keyword: str - The search keyword
        '''
        return ' '.join([keyword.lower() for keyword in keywords])
    
    def start_requests(self) -> None:
        '''
        Before starts the job of crawling job advertisements on Indeed
        '''
        keywords_combination_list = JSONUtils.load_keywords_json()
        location = 'Hong Kong'

        for keywords in keywords_combination_list:
            search_keyword = IndeedAdvertisementsSpider.get_search_keyword(keywords=keywords)
            search_job_url = IndeedAdvertisementsSpider.get_search_url(keyword=search_keyword, location=location)

            yield scrapy.Request(
                url = search_job_url,
                callback = self.parse_advertisement_list,
                meta = {
                    'keyword': search_keyword,
                    'location': location,
                    'offset': 0,
                }
            )

    def parse_advertisement_list(self, response) -> Request:
        '''
        Parse the response of the advertisement list from Indeed

        Parameters:
        response: scrapy.http.Response - The response instance which is received from Indeed

        Returns:
        request: scrapy.http.Request - The request for querying the details of the job advertisement
        '''
        keyword = response.meta['keyword']
        location = response.meta['location']
        offset = response.meta['offset']
        script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)

        if script_tag is not None:
            json_blob = json.loads(script_tag[0])

            jobs_advertisement_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_advertisement_list):
                if job.get('jobkey') is not None:
                    job_details_url = '{}/m/basecamp/viewjob?viewtype=embedded&jk={}'.format(
                        IndeedAdvertisementsSpider.base_url,
                        job.get('jobkey'),
                    )
                    yield scrapy.Request(
                        url = job_details_url,
                        callback = self.parse_advertisement_details,
                        meta = {
                            'keyword': keyword,
                            'location': location,
                            'page': round(offset / 10) + 1 if offset > 0 else 1,
                            'position': index,
                            'job_key': job.get('jobkey'),
                        }
                    )

    def parse_advertisement_details(self, response: Response) -> dict:
        '''
        Parse the response of the details of advertisement from Indeed

        Parameters:
        response: scrapy.http.Response - The response instance which is received from Indeed

        Returns:
        job_advertisement: dict - The job advertisement data
        '''
        keyword = response.meta['keyword']
        location = response.meta['location']
        page = response.meta['page']
        position = response.meta['position']
        job_key = response.meta['job_key']
        script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)

        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job_details = json_blob["jobInfoWrapperModel"]["jobInfoModel"]

            yield {
                'id': job_key,
                'url': URLInterpreter.parse_url(url=response.url),
                'job_key': job_key,
                'job_title': job_details.get('jobTitle'),
                'job_description_html': job_details.get('sanitizedJobDescription').get('content') if job_details.get('sanitizedJobDescription') is not None else '',
                'posted_at': job_details.get('pubDate'),
                'keyword': keyword,
                'location': location,
                'page': page,
                'position': position,
            }
