import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from root_zone_database.items import TLD
from w3lib.html import replace_escape_chars, remove_tags
from itemloaders.processors import MapCompose

class IanaSpider(CrawlSpider):
    name = 'iana_spider'
    allowed_domains = ['iana.org']
    start_urls = ['http://www.iana.org/domains/root/db']
    rules = (
        Rule(
            LinkExtractor(allow=(r'/domains/root/db/', )), callback='parse_item'
        ),
    )

    def parse_item(self, response):
        l = ItemLoader(item=TLD(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)
        l.add_value('delegation_record', response.url)
        l.add_xpath('tld', '//h1/text()', re='Delegation Record for .(.*)')
        l.add_xpath('whois', "//p/text()", re='(whois.*)')
        l.add_xpath('administrator', '//h2[contains(text(), "Administrative Contact")]/following-sibling::b[1]/following-sibling::text()[1]')
        l.add_xpath('sponsor', '//h2[contains(text(), "Sponsoring Organisation")]/following-sibling::b[1]/text()')
        yield l.load_item()
