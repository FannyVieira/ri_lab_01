# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazetadopovo.json') as json_file:
            data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        item = RiLab01Item()
        item['_id'] = '1'
        item['title'] = response.css('h1.c-titulo::text').get()
        item['sub_title'] = response.css('h3.c-sobretitulo span::text').get()
        item['author'] = response.css('li.c-autor span::text').get()
        item['date'] = response.css('li.data-publicacao time::text').get()
        item['section'] = response.xpath('/html/body/div[2]/section[2]/section[1]/ol/li[2]/a/span/text()').extract_first()
        item['text'] = response.css('h2.c-sumario::text').get()
        item['url'] = response.url

        yield item


