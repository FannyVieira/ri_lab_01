from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join


class RiLab01Loader(ItemLoader):

    default_output_processor = TakeFirst()
    text_out = Join()
