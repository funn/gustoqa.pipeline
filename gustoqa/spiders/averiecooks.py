# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class AveriecooksSpider(Spider):
    name = "averiecooks"
    allowed_domains = ["averiecooks.com"]
    start_urls = (
        'http://www.averiecooks.com/category/recipes',
    )

    def parse(self, response):
        for recipe in response.xpath('//div[@id="content"]/ul/li/a/@href').extract():
            yield Request(recipe, self.parse_recipe)

        for page in response.xpath('//div[@class="nav-links"]/a/@href').extract():
            yield Request(page, self.parse)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['description'] = response.xpath('//*[@itemprop="description"]//text()').extract_first()
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['prepTime'] = response.xpath('((//div[@class="time"]/p)[2]//text())[3]').extract_first()
        item['cookTime'] = response.xpath('((//div[@class="time"]/p)[3]//text())[3]').extract_first()
        item['totalTime'] = response.xpath('((//div[@class="time"]/p)[4]//text())[3]').extract_first()
        item['ingredients'] = []
        for ingredient in response.xpath('//div[@class="ingredients"]/*/*'):
            item['ingredients'].append(''.join([s.strip() for s in ingredient.xpath('.//text()').extract()]))
        item['recipeInstructions'] = []
        for instruction in response.xpath('//*[@itemprop="recipeInstructions"]/ol/li'):
            item['recipeInstructions'].append(''.join(instruction.xpath('.//text()').extract()))
        item['recipeCategory'] = response.xpath('//div[@class="left"]/a/text()').extract()[1:]
        item['image_urls'] = {response.xpath('(//div[@id="content"]/div/p/img/@src)[1]').extract_first(): 1}
        return item
