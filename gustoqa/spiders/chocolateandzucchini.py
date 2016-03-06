# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class ChocolateandzucchiniSpider(Spider):
    name = "chocolateandzucchini"
    allowed_domains = ["chocolateandzucchini.com"]
    start_urls = (
        'http://chocolateandzucchini.com/recipes-by-category/',
    )

    def parse(self, response):
        for category in response.xpath('//div[@class="recipegrid"]/div/div/div/a/@href').extract():
            yield Request(category, self.parse_category)

    def parse_category(self, response):
        for recipe in response.xpath('//div[@class="recipegrid"]/div/div/div/a/@href').extract():
            yield Request(recipe, self.parse_recipe)

        for page in response.xpath('//div[@class="navnumbers"]/a/@href').extract():
            yield Request(page, self.parse_category)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['prepTime'] = response.xpath('//*[@itemprop="prepTime"]/text()').extract_first()
        item['cookTime'] = response.xpath('//*[@itemprop="cookTime"]/text()').extract_first()
        item['totalTime'] = response.xpath('//*[@itemprop="totalTime"]/text()').extract_first()
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['ingredients'] = []
        for ingredient in response.xpath('//li[@itemprop="ingredients"]'):
            item['ingredients'].append(''.join([s for s in ingredient.xpath('.//text()').extract()]))
        item['recipeInstructions'] = []
        for instruction in response.xpath('//*[@itemprop="recipeInstructions"]'):
            item['recipeInstructions'].append(''.join([s for s in instruction.xpath('.//text()').extract()]))
        item['recipeCategory'] = [s.replace('*', '') for s in response.xpath('//div[@class="archivetitle"]/a/text()').extract()]
        item['image_urls'] = {response.xpath('//*[@itemprop="image"]/@src').extract_first(): 1}
        return item
