# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    upc = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    