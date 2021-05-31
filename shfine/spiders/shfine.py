# -*- coding: utf-8 -*-
import scrapy
import time
import unicodedata
from bs4 import BeautifulSoup
from shfine.items import ShfineItem

head_url = 'http://183.194.249.79/web/'

url_dict = {'jingan': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=3df201d9-c63e-4c54-b9a5-e252737cf31f',
            'pudong': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=b2327449-70d8-4478-9fc5-d6aa497b3b88',
            'huangpu': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=70d9f0e8-a1c4-416b-a07a-e2f0907f147f',
            'xuhui': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=19c7bc7d-4b4a-4da0-bdf5-7dd0f173ae3e',
            'changning': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=30529bf1-ed50-4b88-95b4-f85ebcf6d8fe',
            'putuo': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=3837ddba-8f4c-4874-9d97-f6c017b103de',
            'hongkou': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=259de04e-88d9-4d35-8685-0c9c3d240e55',
            'yangpu': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=21bb4894-bd36-4a8f-92ee-c55015f18568',
            'baoshan': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=2b03c0b7-14c7-4169-8746-b3dda9e3d872',
            'minhang': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=730e0c38-1c09-435c-8bad-f8ae09bfc358',
            'jiading': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=09cdbfd9-7c3a-4671-9d23-752ea78c2406',
            'jinshan': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=2e6a515f-25dd-4a79-a4cb-32d50b4b7ad6',
            'songjiang': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=c476b5b3-289c-4f9b-81cd-c42bd7330e2a',
            'qingpu': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=16cae63a-df85-4ae0-89b4-e8a68b6649c3',
            'fengxian': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=5ae1dedc-b4a1-4c1e-858e-95a5d1c21a3e',
            'chongming': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=baf07198-efbd-44af-976e-af794986ef01',
            'zongdui': 'http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=1a7adcbf-bf99-4f31-91e3-660717ba13a1'}


class ShfineSpider(scrapy.Spider):
    """
    Spider for the urban management fine in Shanghai.

    The meta of `scrapy.Request` means different catagories of the webpage. 
    `Page = 0` means the main page which contains all the entries of cases.
    `Page = 1` means the detailed sub-page of each case.
    `Page = 2` means this `scrapy.Request` is for the next page (by clicking the "next" button using Selenium).

    References:
        https://blog.csdn.net/qq_43004728/article/details/84636468 (Very useful!)
        https://github.com/clemfromspace/scrapy-selenium
        https://www.pluralsight.com/guides/advanced-web-scraping-tactics-python-playbook
        https://www.cnblogs.com/miners/p/9049498.html
    """
    name = 'shfine'  # ShangHai fine
    allowed_domains = ['www.cgzf.sh.gov.cn']

    def __init__(self, district, max_page=None):
        '''
        Parameters:
            district (str): name of district in Pinyin (such as 'pudong').
            max_page (int): maximum number of pages to crawl. 
        '''
        self.max_page = max_page

        if district in url_dict.keys():
            self.url = url_dict[district]
            self.district = district
        else:
            raise ValueError(
                f"Your input district `{district}` is not supported! Use `district='zongdui'` for 城管总队. Please check carefully!")

        super().__init__()

    def start_requests(self):
        print(f'### Crawling data for "{self.district} district"')
        print('Current page: 1')
        yield scrapy.Request(self.url, callback=self.parse, dont_filter=True, meta={'page': '0'})

    def parse(self, response):
        print(response.url)
        soup = BeautifulSoup(response.body, "lxml")
        item = ShfineItem()

        for ii, case in enumerate(soup.select("ul li")):
            item['date'] = case.select_one("span.id").text
            item['title'] = case.select_one("span.title").text
            item['bureau'] = case.select_one("span.opt").text
            item['url'] = head_url + case.select_one("a").attrs['href']
            print(item['title'], item['date'])

            yield scrapy.Request(url=item['url'], callback=self.parse_case, dont_filter=True, meta={'page': "1"})

        yield scrapy.Request(url=response.url, callback=self.parse, meta={'page': "2"}, dont_filter=True)

    def parse_case(self, response):
        # Go to the subpage of each case
        small_soup = BeautifulSoup(response.body, "lxml")

        if '企业或组织名称' in small_soup.select_one('table').text:
            # 是企业
            page_info = dict(zip(['case_name', 'fine_id', 'company_name', 'person_name', 'person_id',
                                  'fine_reason', 'fine_law', 'fine_sum', 'institute',
                                  'fine_date', 'memo'],
                                 [item.text.strip() for item in small_soup.select('table td')])
                             )
        else:
            # 是个人
            page_info = dict(zip(['case_name', 'fine_id', 'person_name', 'person_id',
                                  'fine_reason', 'fine_law', 'fine_sum', 'institute',
                                  'fine_date', 'memo'],
                                 [item.text.strip() for item in small_soup.select('table td')])
                             )
            page_info['company_name'] = ''
        
        for key in page_info.keys():
            page_info[key] = unicodedata.normalize("NFKD", page_info[key])

        yield page_info
