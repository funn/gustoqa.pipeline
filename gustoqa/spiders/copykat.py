# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class CopykatSpider(Spider):
    name = "copykat"
    allowed_domains = ["copykat.com"]
    start_urls = (
        'http://www.copykat.com/',
    )

    def parse(self, response):
        for category in response.xpath('//li[contains(concat(" ", normalize-space(@class), " "), " cat-item ")]/a/@href').extract():
            yield Request(category, self.parse_category)

    def parse_category(self, response):
        for recipe in response.xpath('//h2[@class="entry-title"]/a/@href').extract():
            yield Request(recipe, self.parse_recipe)

        for page in response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " archive-pagination ")]/ul/li/a/@href').extract():
            yield Request(page, self.parse_category)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//h3[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['description'] = response.xpath('//span[@itemprop="description"]/text()').extract_first()
        item['recipeCategory'] = response.xpath('//span[@itemprop="recipeCategory"]/text()').extract()
        item['author'] = response.xpath('(//ul[@class="recipe-meta"]/li)[1]/span/text()').extract_first()
        item['prepTime'] = response.xpath('(//ul[@class="recipe-meta"]/li)[3]/span/text()').extract_first()
        item['cookTime'] = response.xpath('(//ul[@class="recipe-meta"]/li)[4]/span/text()').extract_first()
        item['recipeYield'] = response.xpath('//span[@itemprop="recipeYield"]/text()').extract_first()
        item['ingredients'] = []
        for ingredient in response.xpath('//ul[@class="ingredients"]/li'):
            item['ingredients'].append(''.join(ingredient.xpath('.//text()').extract()))
        item['recipeInstructions'] = []
        for instruction in response.xpath('//span[@itemprop="recipeInstructions"]/p'):
            item['recipeInstructions'].append(''.join(instruction.xpath('.//text()').extract()))
        item['image_urls'] = {response.xpath('(//div[@class="entry-content"]//img/@src)[1]').extract_first(): 1}
        return item
