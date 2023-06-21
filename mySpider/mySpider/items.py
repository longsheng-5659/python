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
    # 视频描述
    video_description = scrapy.Field()
    # 视频id
    video_vid = scrapy.Field()
    # 作者id
    video_uid = scrapy.Field()
    # 图片
    video_img = scrapy.Field()
    # 时长
    video_var = scrapy.Field()
    # 视频链接
    video_href = scrapy.Field()
    # 视频链接
    video_source = scrapy.Field()
    # 分类
    video_category = scrapy.Field()
    # 标签
    video_tag = scrapy.Field()
    # 观看人数
    video_visitor = scrapy.Field()
    # 创建时间
    video_create_time = scrapy.Field()
    # 更新时间
    video_update_time = scrapy.Field()
    # 版本
    video_version = scrapy.Field()
    # 是否下载
    video_deleted = scrapy.Field()


class DownloadM3u8Ts(scrapy.Item):
    # index文件
    m3u8_Ts_url_index = scrapy.Field()
    m3u8_Ts_url_master = scrapy.Field()


class MyItem(scrapy.Item):
    # 其他字段
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()
    file_path = scrapy.Field()
    video_file_len = scrapy.Field()
