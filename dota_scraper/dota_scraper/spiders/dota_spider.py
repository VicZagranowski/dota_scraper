# -*- coding: utf-8 -*-
import jmespath
import scrapy
from dota_scraper.items import DotaScraperItem


class DotaSpiderSpider(scrapy.Spider):
    name = 'dota_spider'
    allowed_domains = ['opendota.com']
    start_urls = ['https://api.opendota.com/api/heroStats?']
    matchups_url = 'https://api.opendota.com/api/heroes/{}/matchups?'

    def parse(self, response: scrapy.http.response):
        """
        Main parsing method
        :param response: scrapy.Response object
        :return: scrapy.Request
        """
        data = response.json()
        top_heroes = self.extract_top_hereos(data)

        for hero in top_heroes:
            url = self.matchups_url.format(hero.get('id'))
            kwargs = self.parse_kwargs(data, hero)
            yield scrapy.Request(
                url,
                callback=self.parse_matchups,
                cb_kwargs=kwargs
            )

    def parse_matchups(
            self,
            response: scrapy.http.response,
            mapping: list[dict],
            selected_hero: str
    ):
        """
        A callback for specific hero to determine what are the strongest
        heroes against him
        :param response: scrapy.Response object
        :param mapping: mapping of type {"hero_id": "hero_name"}
        :param selected_hero: hero for which the callback is called
        :return: DotaScraperItem()
        """
        data = response.json()
        lowest_winrate_heroes = self.extract_lowest_winrate(data)
        hero_list = self.map_id_to_heroes(lowest_winrate_heroes, mapping)

        yield DotaScraperItem(
            selected_hero=selected_hero,
            lowest_winrate=hero_list
        )

    # Util methods
    def parse_kwargs(self, data, hero):
        """
        Util method to collect the values that will be passed
        further on into callback
        :param data: data to process for mapping
        :param hero: selected_hero from top 3 popular
        :return: dict
        """
        mapping_pattern = '[*].{hero_id: hero_id, name: localized_name}'
        mapping = jmespath.search(mapping_pattern, data)
        return dict(
            selected_hero=hero.get('localized_name'),
            mapping=mapping
        )

    def map_id_to_heroes(
            self,
            lowest_winrate_heroes: list[dict],
            mapping: list[dict]
    ):
        """
        Util method to map the id of top 10 heroes to heroes names
        :param lowest_winrate_heroes: top 10 against the win rate is lowest
        :param mapping: mapping of type {"hero_id": "hero_name"}
        :return: list of hero names
        """
        hero_list = []
        for hero in lowest_winrate_heroes:
            pattern = f"[?hero_id==`{hero.get('hero_id')}`].name | [0]"
            hero_name = jmespath.search(pattern, mapping)
            hero_list.append(hero_name)
        return hero_list

    def extract_top_hereos(self, data: list[dict]):
        """
        Util sorting method
        :param data: stat for the most popular heroes
        :return: sorted list of top 3 most popular
        """
        x = sorted(
            data,
            key=lambda k: k['turbo_wins'] * 100 / k['turbo_picks']
        )
        return x[0:3]

    def extract_lowest_winrate(self, data: list[dict]):
        """
        Util sorting method
        :param data: data of matchups against a specific hero
        :return: sorted list of top 10 strongest hero against selected
        """
        x = sorted(
            data,
            key=lambda k: k['wins'] * 100 / k['games_played'],
            reverse=True
        )
        return x[0:10]
