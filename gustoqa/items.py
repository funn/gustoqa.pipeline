# -*- coding: utf-8 -*-
from scrapy import Item, Field


class GustoqaItem(Item):
    name = Field()
    url = Field()
    ingredients = Field()
    recipeYield = Field()
    prepTime = Field()
    cookTime = Field()
    totalTime = Field()
    recipeInstructions = Field()
    image_urls = Field()
    images = Field()
    description = Field()
    recipeCategory = Field()
    datePublished = Field()
    author = Field()
