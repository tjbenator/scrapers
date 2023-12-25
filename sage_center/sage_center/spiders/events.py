import scrapy


class EventsSpider(scrapy.Spider):
    name = "Sage Center Events"
    allowed_domains = ["visitsage.com"]
    start_urls = ["https://visitsage.com/"]

    # def parse(self, response):
    #     pass

    def parse(self, response):
        for cevent in response.css("div.views-row"):
            yield {
                "date_time": cevent.css("time.datetime").xpath("@datetime").get(),
                "title": cevent.css("span.field-content a::text").get(),
            }
