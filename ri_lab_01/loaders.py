# -*- coding: utf-8 -*-

# Define here the models for extract your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/loaders.html

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join


class RiLab01Loader(ItemLoader):

    default_output_processor = TakeFirst()
    text_out = Join()
