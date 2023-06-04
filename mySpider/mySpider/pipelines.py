# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
from urllib.parse import urlparse

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class MyspiderPipeline:
    def process_item(self, item, spider):
        return item


class VideoDownloadM3u8TsFilePiPline(FilesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item["file_urls"])

    def file_path(self, request, response=None, info=None, *, item=None):
        # 返回的文件名称
        file_name = request.url.split('/')[-1].split('?')[0]
        # 获取视频文件id
        file_path = request.url.split('/')[-3]
        file_path_name = u'{0}/{1}'.format(file_path, file_name)
        print("开始下载文件---》" + file_path_name)
        return file_path_name

    # def item_completed(self, results, item, info):
    #     return item
