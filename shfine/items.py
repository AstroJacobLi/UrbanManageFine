# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShfineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    bureau = scrapy.Field()
    url = scrapy.Field()

    case_name = scrapy.Field()
    fine_id = scrapy.Field()
    person_name = scrapy.Field()
    fine_reason = scrapy.Field()
    fine_law = scrapy.Field()
    fine_sum = scrapy.Field()
    institute = scrapy.Field()
    fine_date = scrapy.Field()
    memo = scrapy.Field()
    pass
