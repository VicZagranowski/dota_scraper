# -*- coding: utf-8 -*-

BOT_NAME = 'dota_scraper'

SPIDER_MODULES = ['dota_scraper.spiders']
NEWSPIDER_MODULE = 'dota_scraper.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'dota_scraper.pipelines.DotaScraperPipeline': 300,
}
