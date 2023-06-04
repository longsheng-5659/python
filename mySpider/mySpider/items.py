# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    # 标题
    video_title = scrapy.Field()
    # 视频id
    video_id = scrapy.Field()
    # 图片
    video_img = scrapy.Field()
    # 时长
    video_var = scrapy.Field()
    # 视频链接
    video_id_href = scrapy.Field()


class DownloadM3u8Ts(scrapy.Item):
    # index文件
    m3u8_Ts_url_index = scrapy.Field()
    m3u8_Ts_url_master = scrapy.Field()


class MyItem(scrapy.Item):
    # 其他字段
    file_urls = scrapy.Field()
    files = scrapy.Field()

