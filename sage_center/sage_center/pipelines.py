# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import BaseItemExporter, PythonItemExporter, XmlItemExporter

class EventExporter(XmlItemExporter):
    pass

class SageCenterPipeline:
    # def process_item(self, item, spider):
    #     return item

    def open_spider(self, spider):
        self.event_to_exporter = {}

    def close_spider(self, spider):
        for exporter, xml_file in self.event_to_exporter.values():
            exporter.finish_exporting()
            xml_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        title = adapter["title"]
        if title not in self.event_to_exporter:
            xml_file = open(f"{title}.xml", "wb")
            exporter = EventExporter(xml_file)
            exporter.start_exporting()
            self.event_to_exporter[title] = (exporter, xml_file)
        return self.event_to_exporter[title][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item