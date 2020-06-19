# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:43:10 2020

@author: mohsh
"""
import scrapy
from ..items import ZomatoItem
import re

class ZomSpideySpider(scrapy.Spider):
    name = 'zom_spidey_'
    allowed_domains = ['zomato.com']
    start_urls = ['https://www.zomato.com/mumbai/restaurants']
    page_num = 0
    res_link= ''
    city='mumbai'
    def parse(self, response):
        for item in self.second_parser(response):
            yield item
        if self.page_num < 1:
            self.page_num+=1
            next_url = "https://www.zomato.com/mumbai/restaurants?page="+str(self.page_num)
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)    
            
    def second_parser(self, response):
        div = response.css(".search-card")
        for c in div:
            items = ZomatoItem()
            items['rest_name'] = c.css('.fontsize0::text').extract()
            res_link = c.css('.fontsize0').css("::attr('href')").get()
            items['res_link'] = c.css('.fontsize0').css("::attr('href')").get()
            items['rating'] = c.css('.rating-value').css("::text").extract()
            items['area'] = c.css('b').css("::text").extract()
            items['address'] = c.css(".ln22").css("::text").extract()
            div2 = c.css(".clearfix.row")
            for d in div2:
                items['cuisine'] = d.css(".col-s-11.col-m-12.nowrap.pl0").css("::text").extract()
                items['cost_for_two'] = d.css(".res-cost .pl0").css("::text").extract()
            link = c.css(".item.result-menu").css("::attr('href')").get()
            if link is not None:
                items['has_menu_available'] = 1
            else:
                items['has_menu_available'] = 0
            order_link = c.css(".result-menu+ a").css("::attr('href')").get()
            if order_link is None:
                items['can_order_via_zomato'] = "No"
            else:
                items['can_order_via_zomato'] = "Yes"
            if res_link is not None:
                request= scrapy.Request(res_link, callback=self.third_parser)
                request.meta['items'] = items
                yield request
        
    def third_parser(self, response):
        items = response.meta["items"]
        number_of_reviews = response.css(".lhdg1m-6.gcPmsM").css("::text").extract()
        number_of_reviews[0] = number_of_reviews[0].replace(",", "")
        items['dining_reviews'] = re.findall("\d+", number_of_reviews[0])
        items['delivery_reviews'] = re.findall("\d+", number_of_reviews[1])
        rest_type = response.css(".bULMfr").css("::text").extract()
        if rest_type is not None:
            items['rest_type'] = rest_type[0]
        else:
            items['rest_type'] = null
        yield items