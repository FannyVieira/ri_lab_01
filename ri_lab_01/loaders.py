from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class RiLab01Loader(ItemLoader):

    default_output_processor = TakeFirst()