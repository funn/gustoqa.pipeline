# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class CookbooksSpider(Spider):
    name = "cookbooks"
    allowed_domains = ["101cookbooks.com"]
    start_urls = (
        'http://www.101cookbooks.com/archives.html',
    )
    root_url = 'http://www.101cookbooks.com'

    def parse(self, response):
        for recipe in response.xpath('//a[@class="list-group-item"]'):
            yield Request(recipe.xpath('@href').extract_first(), self.parse_recipe, meta={'category': recipe.xpath('../@id').extract_first()})

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['recipeCategory'] = response.meta['category']
        item['name'] = response.xpath('//div[@id="recipe"]/h1/text()').extract_first()
        if item['name'] is None:
            raise DropItem('Not a recipe.')
        if len(item['name'].split()) > 1 and 'recipe' in item['name'].rsplit(' ', 1)[1].lower():
            item['name'] = item['name'].rsplit(' ', 1)[0]  # cut off word 'recipe' from the end.
        item['url'] = response.request.url
        item['ingredients'] = [s.strip() for s in response.xpath('//div[@id="recipe"]/blockquote/p/text()').extract()]
        item['recipeInstructions'] = response.xpath('//div[@id="recipe"]/p//text()').extract()[:-1]  # drop 'Print Recipe'
        if 'makes' in item['recipeInstructions'][-1] or 'serves' in item['recipeInstructions'][-1]:
            item['recipeYield'] = item['recipeInstructions'][-1]
            item['recipeInstructions'] = item['recipeInstructions'][:-1]
        item['prepTime'] = response.xpath('//span[@class="preptime"]/text()').extract_first()
        item['cookTime'] = response.xpath('//span[@class="cooktime"]/text()').extract_first()
        item['image_urls'] = {}
        index = 1
        for image in response.xpath('//div[@class="hrecipe"]//img/@src').extract():
            if 'print.gif' not in image:
                if image[0] == '/':
                    item['image_urls'][self.root_url + image] = index
                else:
                    item['image_urls'][image] = index
                index += 1
        return item

