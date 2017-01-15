# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags

from root_zone_database.items import TLD

class IanaSpider(CrawlSpider):
	name = "iana"
	allowed_domains = ["iana.org"]
	start_urls = (
		'http://www.iana.org/domains/root/db',
	)

	rules = (
		Rule(
			SgmlLinkExtractor(allow=r'/domains/root/db/'),
			callback='parse_item',
		),
	)

	def parse_item(self, response):
		xpath = Selector(response)
		loader = ItemLoader(item=TLD(), response=response)
		loader.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)
		loader.add_value('delegation_record', response.url)
		loader.add_xpath('tld', '//h1/text()', re='Delegation Record for .(.*)')
		loader.add_xpath('whois', "//p/text()", re='(whois.*)')
		loader.add_xpath('administrator', '//h2[contains(text(), "Administrative Contact")]/following-sibling::b[1]/following-sibling::text()[1]')
		loader.add_xpath('sponsor', '//h2[contains(text(), "Sponsoring Organisation")]/following-sibling::b[1]/text()')
		yield loader.load_item()
