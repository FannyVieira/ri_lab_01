# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = ['https://www.gazetadopovo.com.br/economia/como-esse-americano-conseguiu-desaparecer-da-web-em-15-passos-1xl7117h4actrfg3zbtqjittq/']

 #   def __init__(self, *a, **kw):
    #    super(GazetaDoPovoSpider, self).__init__(*a, **kw)
    #    with open('seeds/gazetadopovo.json') as json_file:
    #            data = json.load(json_file)
    #    self.start_urls = list(data.values())

    def parse(self, response):
        item = RiLab01Item()
        item['_id'] = '1'
        item['title'] = response.css('.c-titulo::text').get()
        item['sub_title'] = response.css('.c-sobretitulo span::text').get()
        item['author'] = response.css('.c-autor span::text').get()
        item['date'] = response.css('.data-publicacao time::text').get()
        item['section'] = response.xpath('/html/body/div[2]/section[2]/section[1]/ol/li[2]/a/span/text()').extract_first()
        item['text'] = response.css('.c-sumario::text').get()
        item['url'] = response.url

        yield item


