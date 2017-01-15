# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RootZoneDatabaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TLD(scrapy.Item):
        tld = scrapy.Field()
        whois = scrapy.Field()
	sponsor = scrapy.Field()
	delegation_record = scrapy.Field()
	administrator = scrapy.Field()
