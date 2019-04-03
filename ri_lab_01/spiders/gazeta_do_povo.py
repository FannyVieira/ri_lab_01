# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlsplit, urljoin

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from ri_lab_01.loaders import RiLab01Loader
from ri_lab_01.settings import DEADLINE
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
        active_page = int(response.css('.pg-ativa::text').get())
        last_news_links = [a.attrib['href'] for a in response.css('.ultimas-chamadas a') if self.is_valid_date(a.attrib['data-publication'])]
        for url in last_news_links:
            url = urljoin('https://www.gazetadopovo.com.br', url)
            yield scrapy.Request(url, callback=self.parse_news_page, meta={'page_count': self.crawler.stats.get_value('request_count')})

        if last_news_links:
            new_page = active_page + 1
            updated_url = urlsplit(response.url)._replace(query='offset={new_page}'.format(new_page=new_page)).geturl()
            yield scrapy.Request(updated_url, self.parse)

    def parse_news_page(self, response):
        loader = RiLab01Loader(item=RiLab01Item(), response=response)
        url = response.url

        loader.add_value('_id', response.meta.get('page_count'))
        loader.add_css('title', '.c-titulo::text')
        loader.add_css('title', '.c-title::text')
        loader.add_css('sub_title', '.c-sobretitulo span::text')
        loader.add_css('sub_title', 'c-overhead span::text')
        loader.add_css('author', '.c-autor span::text')
        loader.add_css('author', '.item-agency::text')
        loader.add_css('author', '.item-name span::text')
        loader.add_css('date', '.data-publicacao time::text')
        loader.add_value('section', url.split('/')[3])
        loader.add_css('text', '.c-sumario::text')
        loader.add_css('text', '.c-summary::text')
        loader.add_value('url', url)

        self.write_in_frontier(loader)

        return loader.load_item()

    def write_in_frontier(self, loader):
        with open('frontier/gazeta_do_povo.json', 'a') as json_file:
            title = loader.get_output_value('_id')
            url = loader.get_output_value('url')
            data = {title: url}
            print(title, url)
            print("=======\n\n\n")
            json.dump(data, json_file)

    def is_valid_date(self, value):
        DAY_DEADLINE, MONTH_DEADLINE, YEAR_DEADLINE = DEADLINE.split('.')
        DEADLINE_DATE = date(int(YEAR_DEADLINE), int(MONTH_DEADLINE), int(DAY_DEADLINE))

        # A data extraída está no seguinte formato: YYYY-MM-DD
        year, month, day = value.split('-')
        pub_date = date(int(year), int(month), int(day))

        return pub_date > DEADLINE_DATE


