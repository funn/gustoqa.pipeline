# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.exceptions import DropItem

from gustoqa.items import GustoqaItem


class CookieandkateSpider(Spider):
    name = "cookieandkate"
    allowed_domains = ["cookieandkate.com"]
    start_urls = (
        'http://cookieandkate.com/recipes/',
    )

    def parse(self, response):
        for item in response.xpath('//*[@class="lcp_catlist_item"]/a/@href').extract():
            yield Request(item, self.parse_recipe)

    def parse_recipe(self, response):
        item = GustoqaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//*[@class="ERSName"]//text()').extract_first()
        if not item['name']:
            raise DropItem('Not a recipe.')
        item['description'] = response.xpath('//*[@class="ERSSummary"]/text()').extract_first()
        item['recipeYield'] = response.xpath('//*[@itemprop="recipeYield"]/text()').extract_first()
        item['recipeCategory'] = response.xpath('//span[@class="entry-categories"]/a/text()').extract()
        item['ingredients'] = []
        for ingredient in response.xpath('//li[@itemprop="ingredients"]'):
            item['ingredients'].append(''.join([s for s in ingredient.xpath('text()').extract()]))
        item['ingredients'] = response.xpath('//*[@itemprop="ingredients"]/text()').extract()
        item['prepTime'] = response.xpath('//*[@itemprop="prepTime"]/text()').extract_first()
        item['cookTime'] = response.xpath('//*[@itemprop="cookTime"]/text()').extract_first()
        item['totalTime'] = response.xpath('//*[@itemprop="totalTime"]/text()').extract_first()
        item['author'] = response.xpath('//*[@itemprop="author"]/text()').extract_first()
        item['datePublished'] = response.xpath('//*[@itemprop="datePublished"]/text()').extract_first()
        item['recipeInstructions'] = response.xpath('//*[@itemprop="recipeInstructions"]/text()').extract()
        item['image_urls'] = {response.xpath('(//div[contains(concat(" ", normalize-space(@class), " "), " entry-content ")]//img/@src)[1]').extract_first(): 1}
        return item
