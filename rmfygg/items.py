# -*- coding: utf-8 -*-
import scrapy


class RmfyggItem(scrapy.Item):
    cf_xzjg = scrapy.Field()
    ws_nr_txt = scrapy.Field()
    cf_cflb = scrapy.Field()
    fb_rq = scrapy.Field()
    xq_url = scrapy.Field()