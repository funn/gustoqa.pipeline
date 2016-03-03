# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class AggieskitchenSpider(Spider):
    name = "aggieskitchen"
    allowed_domains = ["aggieskitchen.com"]
    start_urls = (
        'http://aggieskitchen.com/recipe-index/',
    )

    def parse(self, response):
        for category in response.xpath('//div[@class="recipecat"]'):
            yield Request(category.xpath('a/@href').extract_first(), self.parse_category)

    def parse_category(self, response):
        for recipe in response.xpath('//div[@class="archivepost"]'):
            yield Request(recipe.xpath('a/@href').extract_first(), self.parse_recipe)

        for page in response.xpath('//div[@id="wp_page_numbers"]//a/@href').extract():
            yield Request(page, self.parse_category)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['author'], item['datePublished'], _ = ';'.join([s.strip() for s in response.xpath('//div[@class="postmeta"]/text()').extract()]).split(';')
        item['ingredients'] = response.xpath('//div[@class="ingredients"]/ul/li/text()').extract()
        item['recipeInstructions'] = response.xpath('//*[@itemprop="recipeInstructions"]/ol/li/text()').extract()
        item['recipeCategory'] = response.xpath('//a[@rel="category tag"]/text()').extract()
        item['image_urls'] = {response.xpath('(//div[@id="content"]//img/@src)[1]').extract_first(): 1}
        return item
