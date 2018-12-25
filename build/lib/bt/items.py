# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source_name = Field()
    create_time = Field()
    source_size = Field()
    source_link = Field()
    source_list = Field()  # json
    source_hot = Field()
    old_link = Field()