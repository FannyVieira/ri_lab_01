# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlsplit, urljoin

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from ri_lab_01.loaders import RiLab01Loader
from datetime import date


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
            data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        pag_ativa = response.css('.pg-ativa::text').get()
        last_news_links = [a.attrib['href'] for a in response.css('.ultimas-chamadas a') if self.is_valid_date(a.attrib['data-publication'])]
        for url in last_news_links:
            url = urljoin('https://www.gazetadopovo.com.br', url)
            yield scrapy.Request(url, callback=self.parse_news_page)

        if last_news_links:
            new_page = pag_ativa + 1
            updated_url = urlsplit(response.url)._replace(query='offset=${new_page}').geturl()
            yield scrapy.Request(updated_url, self.parse)

    def parse_news_page(self, response):
        loader = RiLab01Loader(item=RiLab01Item(), response=response)
        url = response.url

        loader.add_value('_id', '1')
        loader.add_css('title', '.c-titulo::text')
        loader.add_css('sub_title', '.c-sobretitulo span::text')
        loader.add_css('author', '.c-autor span::text')
        loader.add_css('date', '.data-publicacao time::text')
        loader.add_value('section', url.split('/')[3])
        loader.add_css('text', '.c-sumario::text')
        loader.add_value('url', url)

        return loader.load_item()

    def is_valid_date(self, value):
        # A data extraída está no seguinte formato: YYYY-MM-DD
        FROM_DATE = date(2018, 1, 1)
        year, month, day = value.split('-')
        pub_date = date(int(year), int(month), int(day))

        return pub_date > FROM_DATE


