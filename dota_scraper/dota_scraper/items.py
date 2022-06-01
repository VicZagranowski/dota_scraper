# -*- coding: utf-8 -*-
import scrapy


class DotaScraperItem(scrapy.Item):
    selected_hero = scrapy.Field()
    lowest_winrate = scrapy.Field()
