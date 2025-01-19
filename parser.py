import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ["https://postupi.online/professii/?sort_type=2"]

    def parse(self, response):
        for block in response.css('div.card-box-wrap div.list-col'):
            yield {
                'profession': block.css('div.list-col__info a::text').get()
            }

        next_page = response.xpath('//a[@title = "дальше"]/@href').get()
        if next_page:
            yield Request(f'{next_page}', callback=self.parse)


    # def parse_detail(self, response):
    #     for job_tag in response.css('tbody tr'):
    #         yield {
    #             'profession': job_tag.css('td a::text').get(),
    #             'field_of_activity': response.meta['field_of_activity'],
    #             'average salary': job_tag.css('strong::text').get()  
    #         }