# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TtItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    behot_time = scrapy.Field()
    new_url = scrapy.Field()
    pass
