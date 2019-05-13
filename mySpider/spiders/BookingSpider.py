import scrapy
from mySpider.items import BookingHotelItem
import json
from mySpider.googleAPI import get_google_results


class BookingSpider(scrapy.Spider):

    name = 'booking'
    allowed_domains = ['booking.com']
    start_urls = ['https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1DCAQoggI4mgRICVgEaA-IAQGYAQm4AQfIAQzYAQPoAQH4AQKIAgGoAgO4Av613uYFwAIB&sid=371a16a6e405b3643fb3921f7ba39d4d&tmpl=searchresults&ac_click_type=b&ac_position=1&class_interval=1&dest_id=-1586844&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&iata=MEL&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=index&srpvid=79e73c1d0d4c02b0&ss=Melbourne%2C%20Victoria%2C%20Australia&ss_all=0&ss_raw=Melbourne&ssb=empty&sshis=0&nflt=review_score%3D80%3B&rsf=']

    def parse(self, response):
        for hotel in response.xpath('//h3/a[@class="hotel_name_link url"]'):
            hotel_url = hotel.xpath('@href').get()
            hotel_url = response.urljoin(hotel_url).replace('\n','')
            hotel_url = hotel_url.replace('?from=searchresults#hotelTmpl','')
            hotel_url = hotel_url.replace('?bhgwe_bhr=0&from=searchresults#hotelTmpl','')
            yield response.follow(hotel_url, self.parse_hotel)

        next_page = response.xpath("//div/nav/ul/li[@class='bui-pagination__item bui-pagination__next-arrow']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_hotel(self, response):
        hotel = BookingHotelItem()
        details = response.xpath('//script[@type="application/ld+json"]/text()').get()
        details_dict = json.loads(details)
        hotel['name'] = details_dict['name']
        hotel['address'] = details_dict['address']['streetAddress']
        hotel['rating'] = response.xpath('//li[@data-question="total"]/p[@class="review_score_value"]/text()').get()
        hotel['loc_rating'] = response.xpath('//li[@data-question="hotel_location"]/p[@class="review_score_value"]/text()').get()
        location = get_google_results(hotel['address'])
        hotel['latitude'] = location['latitude']
        hotel['longitude'] = location['longitude']
        return hotel