# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from gustoqa.items import GustoqaItem


class SimplyrecipesSpider(Spider):
    name = "simplyrecipes"
    allowed_domains = ["simplyrecipes.com"]
    start_urls = (
        'http://www.simplyrecipes.com/index/',
    )

    def parse(self, response):
        for category in response.xpath('//ul[@class="tags"]/li/a/@href').extract():
            yield Request(category, self.parse_category)

    def parse_category(self, response):
        for item in response.xpath('//ul[@class="entry-list"]/li/a/@href').extract():
            yield Request(item, self.parse_recipe)

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield Request(next_page, self.parse_category)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        item['description'] = response.xpath('//*[@itemprop="description"]/@content').extract_first()
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['recipeCategory'] = response.xpath('//*[@itemprop="recipeCategory"]/a/text()').extract()
        item['ingredients'] = response.xpath('//*[@itemprop="recipeIngredient"]/text()').extract()
        item['prepTime'] = response.xpath('//*[@itemprop="prepTime"]/text()').extract_first()
        item['cookTime'] = response.xpath('//*[@itemprop="cookTime"]/text()').extract_first()
        item['author'] = response.xpath('//*[@itemprop="author"]//*[@itemprop="name"]/text()').extract_first()
        item['datePublished'] = response.xpath('//*[@itemprop="datePublished"]/@content').extract_first()
        item['recipeInstructions'] = response.xpath('//*[@itemprop="recipeInstructions"]/p/text()').extract()
        item['image_urls'] = {}
        index = 1
        for image in response.xpath('//div[@class="entry-content"]//img/@src').extract():
            if 'blank' not in image:
                item['image_urls'][image] = index
                index += 1
        return item
