# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class BiggirlssmallkitchenSpider(Spider):
    name = "biggirlssmallkitchen"
    allowed_domains = ["biggirlssmallkitchen.com"]
    start_urls = (
        'http://www.biggirlssmallkitchen.com/category/blog',
    )
    root_url = 'http://www.biggirlssmallkitchen.com'

    def parse(self, response):
        for item in response.xpath('//div[@class="postgrid"]//a/@href').extract():
            yield Request(item, self.parse_recipe)

        next_page = response.xpath('//div[@class="navright"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, self.parse)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['ingredients'] = response.xpath('//*[@itemprop="ingredients"]/text()').extract()
        item['description'] = response.xpath('//*[@itemprop="description"]/text()').extract_first()
        item['prepTime'] = response.xpath('//*[@itemprop="prepTime"]/text()').extract_first()
        item['cookTime'] = response.xpath('//*[@itemprop="cookTime"]/text()').extract_first()
        item['totalTime'] = response.xpath('//*[@itemprop="totalTime"]/text()').extract_first()
        item['recipeInstructions'] = response.xpath('//*[@itemprop="recipeInstructions"]/text()').extract()
        item['image_urls'] = {}
        index = 1
        for image in response.xpath('//div[@class="content clearfix"]//img/@src | //div[@class="featimage"]//img/@src').extract():
            item['image_urls'][image] = index
        return item

