import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["edunews.ru"]
    start_urls = ["https://edunews.ru/professii/obzor/"]

    def parse(self, response):
        for url in response.css('p.rating_professii span a'):
            yield Request(
                f'https://edunews.ru{url.css("::attr(href)").get()}',
                callback=self.parse_detail,
                meta={'field_of_activity': url.css('::text').get()}
            )


    def parse_detail(self, response):
        for job_tag in response.css('tbody tr'):
            yield {
                'profession': job_tag.css('td a::text').get(),
                'field_of_activity': response.meta['field_of_activity'],
                'average salary': job_tag.css('strong::text').get()  
            }