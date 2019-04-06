# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlsplit, urljoin

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from ri_lab_01.loaders import RiLab01Loader, RiLab01CommentLoader
from ri_lab_01.util.date import is_valid_date
from ri_lab_01.util.file import write_in_frontier
from ri_lab_01.util.seletor import get_value_by_selector


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []
    page_request_count = 0

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
            data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        """Get the list of urls from sections of the Gazeta's site(e.g 'ultimas-noticias', 'populares', etc)

        :param response: the html response from scrapy download
        :return scrapy.Item: a iterable list of items extracted
        """
        urls_sections = [a.attrib['href'] for a in get_value_by_selector(response,'.c-noticias-rapidas a')]
        for url in urls_sections:
            yield scrapy.Request(url, callback=self.parse_pagination_page)

    def parse_pagination_page(self, response):
        """Get a list of news URL and set pagination logic to get more, see this page
        to understand better(https://www.gazetadopovo.com.br/ultimas-noticias/)

        :param response: the html response from scrapy download
        :return scrapy.Item: a iterable list of items extracted
        """
        news_links = [a.attrib['href'] for a in get_value_by_selector(response,'.c-chamada a')]

        for url in news_links:
            self.page_request_count += 1
            url = urljoin('https://www.gazetadopovo.com.br', url)
            # for get comments section use "callback=self.parse_comments_section"
            yield scrapy.Request(url, callback=self.parse_news_page, meta={'page_count': self.page_request_count})

        # for limit the count of requests, i set 'CLOSESPIDER_PAGECOUNT= 200' on settings file.
        if news_links:
            updated_url = self.get_new_url_by_pagination(response)
            yield scrapy.Request(updated_url, self.parse_pagination_page)

    def parse_news_page(self, response):
        """Parse the news page and extract text, title, subtitle, author,
        section(the section is part of url), date and url data using loader object,
        check more in documentation(https://docs.scrapy.org/en/latest/topics/loaders.html)

        :param response: the html response from scrapy download
        :return scrapy.Item: a iterable list of items extracted
        """
        loader = RiLab01Loader(item=RiLab01Item(), response=response)
        url = response.url

        loader.add_value('_id', response.meta.get('page_count'))
        loader.add_css('title', '.c-titulo::text')
        loader.add_css('title', '.c-title::text')
        loader.add_css('sub_title', '.c-sobretitulo span::text')
        loader.add_css('sub_title', 'c-overhead span::text')
        loader.add_css('author', '[class*="autor"] span::text')
        loader.add_css('author', '.item-agency::text')
        loader.add_css('author', '.item-name span::text')
        loader.add_css('date', '.data-publicacao time::text')
        loader.add_value('section', url.split('/')[3])
        loader.add_css('text', '.paywall-google > p::text')
        loader.add_value('url', url)
        write_in_frontier(loader)

        return loader.load_item()

    def parse_comments_section(self, response):
        """Parse the news page and extract data about comments as author, date, text,
        using loader object, check more in documentation
        (https://docs.scrapy.org/en/latest/topics/loaders.html)

        :param response: the html response from scrapy download
        :return scrapy.Item: a iterable list of items extracted
        """
        loader = RiLab01CommentLoader(item=RiLab01CommentItem(), response=response)
        loader.add_value('id_article', '')
        loader.add_css('author', '.user-name::text')
        loader.add_css('date', '.age::text')
        loader.add_css('text', '.comment::text')

        return loader.load_item()


    def get_new_url_by_pagination(self, response):
        """Get a new url through pagination, the difference necessary is change a
        'offset' atributte in query URL incrementing the number of current page.

        :param response: the html response from scrapy download
        :return str: a new url result of pagination
        """
        active_page = int(get_value_by_selector(response,'.pg-ativa::text').get())
        new_page = active_page + 1
        updated_url = urlsplit(response.url)._replace(query='offset={new_page}'.format(new_page=new_page)).geturl()

        return updated_url


