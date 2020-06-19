# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZomatoItem(scrapy.Item):
    # define the fields for your item here like:
    rest_name = scrapy.Field()
    rating = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    cuisine = scrapy.Field()
    cost_for_two = scrapy.Field()
    can_order_via_zomato = scrapy.Field()
    location = scrapy.Field()
    res_link = scrapy.Field()
    dining_reviews = scrapy.Field()
    delivery_reviews = scrapy.Field()