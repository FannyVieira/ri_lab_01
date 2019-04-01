# -*- coding: utf-8 -*-
import scrapy
import json
import urllib.parse

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
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
        last_news_links = [a.attrib['href'] for a in response.css('.ultimas-chamadas a')]
        for url in last_news_links:
            url = urllib.parse.urljoin('https://www.gazetadopovo.com.br', url)
            yield scrapy.Request(url, callback=self.parse_news_page)

    def parse_news_page(self, response):
        item = RiLab01Item()
        pub_date_value = response.css('.data-publicacao time::text').get()
        if pub_date_value and self.is_valid_date(pub_date_value):
            item['_id'] = '1'
            item['title'] = response.css('.c-titulo::text').get()
            item['sub_title'] = response.css('.c-sobretitulo span::text').get()
            item['author'] = response.css('.c-autor span::text').get()
            item['date'] = pub_date_value
            item['section'] = response.xpath('/html/body/div[2]/section[2]/section[1]/ol/li[2]/a/span/text()').extract_first()
            item['text'] = response.css('.c-sumario::text').get()
            item['url'] = response.url

        yield item


    def is_valid_date(self, value):
        # A data extraída está no seguinte formato: [DD/MM/YYYY]
        FROM_DATE = date(2018, 1, 1)
        value = value.strip('[]')
        day, month, year = value.split('/')
        pub_date = date(int(year), int(month), int(day))

        return pub_date > FROM_DATE


