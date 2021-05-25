# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import re
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from scrapy.exceptions import CloseSpider


class SeleniumMiddlerware(object):
    """
    Middleware for connecting Selenium and Scrapy
    """

    def __init__(self):
        self.driver = webdriver.Safari()
        # If not using MacOS, change Safari to another browser.

    def process_request(self, request, spider):
        if int(request.meta['page']) == 2:  # 翻页，浏览器还需要在main page才行
            print('Middleware to next page: ', request.url)

            next_button = self.driver.find_elements_by_css_selector(
                'span.nav-list a')[-2]

            current_num = int(
                self.driver.find_elements_by_css_selector("a.active")[0].text)

            # max_num = int(self.driver.find_elements_by_css_selector(
            #     'span.nav-list a')[-3].text)
            print('Next page:', current_num + 1)

            if spider.max_page is not None:
                if current_num >= spider.max_page:
                    raise CloseSpider(
                        f'STOPPED! Already crawled {current_num} pages!')

            next_button.click()  # go to next page
            try:
                WebDriverWait(self.driver, 60).until(
                    lambda s: int(s.find_elements_by_css_selector("a.active")[0].text) == current_num + 1)
            except TimeoutException:
                print("TimeoutException: Element summary not found")

            html = self.driver.page_source

        else:
            if int(request.meta['page']) == 0:  # main page
                print('Middleware: ', request.url)
                self.driver.get(request.url)
                try:
                    WebDriverWait(self.driver, 60).until(
                        lambda s: s.find_element_by_css_selector('ul li').is_displayed())
                except TimeoutException:
                    print("TimeoutException: Element summary not found")

                html = self.driver.page_source

            elif int(request.meta['page']) == 1:  # subpage
                # open a new browser for subpage, in headless mode
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--headless')
                self.subdriver = webdriver.Chrome(
                    '../chromedriver', options=chrome_options)
                print('Middleware to subpage: ', request.url)
                self.subdriver.get(request.url)
                try:
                    WebDriverWait(self.subdriver, 60).until(
                        lambda s: s.find_element_by_class_name('case-detail').is_displayed())
                except TimeoutException:
                    print("TimeoutException: Element detail not found")

                html = self.subdriver.page_source
                # self.subdriver.close()

        # 构造一个请求的结果，将谷歌浏览器访问得到的结果构造成response，并返回给引擎
        response = scrapy.http.HtmlResponse(
            url=request.url, body=html, request=request, encoding='utf-8')
        return response
