# booking score scrapy
## 1. Introduction
Retrieve hotels info, including name, address, total rating and location rating from booking.com for education purpose.
Google Map API is used in this project to obtain the geocoding info such as latitude and longitude of each hotel.
## 2. Environment
### 2.1. scrapy 1.6.0
#### Installation
```
source activate your_virtualenv
conda install Scrapy
```  
A Simple Tutorial from Documentation：Check [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
### 2.2. googlemaps 2.5.1
This is the python client for Google Maps Services.  
#### Installation
```
source activate your_virtualenv
conda install -c conda-forge googlemaps
```  
#### Usage
This example is given in the github homepage [Python Client for Google Maps Services](https://github.com/googlemaps/google-maps-services-python)  
To use Geocoding API, Visit https://developers.google.com/console to get an API key.
```python
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='Add Your Key here')

# Geocoding an address
geocode_result = gmaps.geocode('8 Whiteman Street, Southbank, 3006 Melbourne, Australia')
```
### 2.3. geopy 1.19.0 (Alternative)
geopy is a Python 2 and 3 client for several popular geocoding web services.
#### Installation
```
source activate your_virtualenv
conda install -c conda-forge geopy
```
#### Usage
See more info in [GeoPy Documentation](https://geopy.readthedocs.io/en/stable/).
```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("8 Whiteman Street, Southbank, 3006 Melbourne, Australia")
print((location.latitude, location.longitude))
```
## 3. Usage
1. Specify the data you wish to scrape in mySpider/items.py.
```python
import scrapy

class BookingHotelItem(scrapy.Item):
    # define the fields for your item
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    rating = scrapy.Field()
    loc_rating = scrapy.Field()
    pass
```
2. Set the first request url in mySpider/spiders/BookingSpider.py.
```python
start_urls = ['https://www.booking.com/searchresults.en-gb.html.....']
```
3. Set your API key in mySpider/googleAPI.py.
```python
KEY = 'your api key'
```
4. Run and save as .csv file.
```
scrapy crawl booking -o booking_rating_8+_Melbourne.csv
```
## 4. Comments
1. Response from Geocoding API is like:
```json
[
      {
         "address_components" : [
            {
               "long_name" : "8",
               "short_name" : "8",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Whiteman Street",
               "short_name" : "Whiteman St",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Southbank",
               "short_name" : "Southbank",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Melbourne City",
               "short_name" : "Melbourne",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Victoria",
               "short_name" : "VIC",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Australia",
               "short_name" : "AU",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "3006",
               "short_name" : "3006",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "8 Whiteman St, Southbank VIC 3006, Australia",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : -37.8214972,
                  "lng" : 144.9609047
               },
               "southwest" : {
                  "lat" : -37.8263877,
                  "lng" : 144.9564941
               }
            },
            "location" : {
               "lat" : -37.82343669999999,
               "lng" : 144.9580861
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : -37.8214972,
                  "lng" : 144.9609047
               },
               "southwest" : {
                  "lat" : -37.8263877,
                  "lng" : 144.9564941
               }
            }
         },
         "place_id" : "ChIJ93onsFJd1moRXl_4CMKq_HA",
         "types" : [ "premise" ]
      }
]
```
2. Hotel info is stored in a script like:
```html
<script type="application/ld+json">
{
   "@context" : "http://schema.org",
   "name" : "Crown Metropol Melbourne",
   "url" : "https://www.booking.com/hotel/au/crown-metropol.en-gb.html",
   "description" : "Crown Metropol offers luxury accommodation on Melbourne’s Southbank. Guests have access to an exclusive lounge and bar with panoramic city views.",
   "aggregateRating" : {
      "ratingValue" : 8.9,
      "bestRating" : 10,
      "@type" : "AggregateRating",
      "reviewCount" : 5228
   },
   "address" : {
      "addressRegion" : "Victoria",
      "@type" : "PostalAddress",
      "addressCountry" : "Australia",
      "streetAddress" : "8 Whiteman Street, Southbank, 3006 Melbourne, Australia",
      "addressLocality" : "8 Whiteman Street",
      "postalCode" : "3006"
   },
   "@type" : "Hotel",
   "hasMap" : "https://maps.googleapis.com/maps/api/staticmap?zoom=15&sensor=false&markers=color:blue%7c-37.8258628,144.9575897&center=-37.8258628,144.9575897&size=1600x1200&client=gme-booking&channel=booking-frontend&signature=-vpHILSBtvgRszWuwOdaA6K4bDg=",
   "priceRange" : "Prices for upcoming dates start at AUD 259 per night (We Price Match)",
   "image" : "https://r-ak.bstatic.com/images/hotel/max500/360/36091341.jpg"
}
</script>
```
3. Specific scores can be found under `<div id="review_list_score" class="">` tag.
<img src="https://github.com/zhiqinzhang/booking_score_scrapy/blob/master/mySpider/imagecache/screenshot_score.png" width = "40%" height = "40%" alt="图片名称" align=center />
4. Ideal output file will look like this:
<img src="https://github.com/zhiqinzhang/booking_score_scrapy/blob/master/mySpider/imagecache/screenshot_output.png" width = "915" height = "406" alt="图片名称" align=center />
