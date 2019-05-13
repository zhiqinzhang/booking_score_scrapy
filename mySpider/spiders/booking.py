import scrapy

class BookingSpider(scrapy.Spider):

    name = "Booking"
    start_urls = [
        'https://www.booking.com/searchresults.zh-cn.html?ss=melbou'
    ]

    def __init__(self):
        self.base_url = "https://www.booking.com"

    def parse(self, response):
        for hotel in response.xpath('//h3/a/span[@class="sr-hotel__name\n"]'):
            yield {
                'hotel_name': hotel.xpath('text()').get()
            }

        next_page = response.xpath("//div/nav/ul/li[@class='bui-pagination__item bui-pagination__next-arrow']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)











