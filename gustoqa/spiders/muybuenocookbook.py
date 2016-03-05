# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class MuybuenocookbookSpider(Spider):
    name = "muybuenocookbook"
    allowed_domains = ["muybuenocookbook.com"]
    start_urls = (
        'http://www.muybuenocookbook.com/category/recipes/',
    )

    def parse(self, response):
        for item in response.xpath('//div[@id="content"]/div/div/a/@href').extract():
            yield Request(item, self.parse_recipe)

        for page in response.xpath('//div[@id="wp_page_numbers"]/ul/li/a/@href').extract():
            yield Request(page, self.parse)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['recipeInstructions'] = []
        str_buffer = ''
        for instruction in response.xpath('//*[@itemprop="recipeInstructions"]//text()').extract():
            str_buffer += instruction.strip()
            if str_buffer != '':
                item['recipeInstructions'].append(str_buffer)
                str_buffer = ''
        item['ingredients'] = []
        for ingredient in response.xpath('//*[@class="ingredients"]//text()').extract():
            str_buffer += ingredient.strip()
            if str_buffer != '':
                item['ingredients'].append(str_buffer)
                str_buffer = ''
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['image_urls'] = {response.xpath('(//div[@id="content"]//img/@src)[1]').extract_first(): 1}
        return item
