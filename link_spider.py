# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ['https://maharatech.gov.eg']

    def __init__(self):
        self.link_count = 0
        self.max_links =10
        

    def parse(self, response):
        if self.link_count >= self.max_links:
            return

        for link in response.css('a::attr(href)').getall():
            if link.startswith('http') or link.startswith('https'):
                full_link = response.urljoin(link)
                yield {'url': full_link}
                self.link_count += 1
                if self.link_count >= self.max_links:
                    return
                yield scrapy.Request(full_link, callback=self.parse)

