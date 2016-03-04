# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from gustoqa.items import GustoqaItem


class Food52Spider(Spider):
    name = "food52"
    allowed_domains = ["food52.com"]
    start_urls = (
        'http://www.food52.com/recipes',
    )
    root_url = 'http://food52.com'

    def parse(self, response):
        for item in response.xpath('//div[@data-type="recipe"]//a[@class="photo"]/@href').extract():
            yield Request(self.root_url + item, self.parse_recipe)

        next_page = response.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page:
            yield Request(self.root_url + next_page, self.parse)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        item['recipeYield'] = ''.join([s.strip() for s in response.xpath('//*[@itemprop="recipeYield"]//text()').extract()])
        item['ingredients'] = []
        for ingredient in response.xpath('//*[@itemprop="ingredients"]'):
            item['ingredients'].append(' '.join([s.strip() for s in ingredient.xpath('span/text()').extract()]))
            if item['ingredients'][-1][-1] == ':':
                item['ingredients'] = item['ingredients'][:-1]
        item['author'] = response.xpath('//*[@itemprop="author"]/text()').extract_first()
        item['recipeInstructions'] = [s.strip() for s in response.xpath('//*[@itemprop="recipeInstructions"]//text()').extract()]
        item['image_urls'] = {'http:' + response.xpath('//*[@itemprop="image"]/@src').extract_first(): 1}
        return item
