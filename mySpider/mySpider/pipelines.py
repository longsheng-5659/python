# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import os.path
import time
from urllib.parse import urlparse

import pymysql
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from twisted.enterprise import adbapi

con = pymysql.Connect(
    host="120.25.161.159",
    port=3306,
    user="dev",
    password="dev",
    database="videohub",
    charset="utf8"
)


class PronHubMysqlPipeline(object):

    def process_item(self, item, spider):
        # sql = "insert into video values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = "insert into videohub.video(vid,href,title) values(%s,\"%s\",\"%s\")" % \
              (item['video_vid'], item['video_href'],item['video_title'])
        print(sql)

        con.cursor().execute(sql)
        # con.cursor().execute(sql, (item['video_vid'], item['video_uid'], item['video_title'],
        #                            item['video_img'], item['video_description'], item['video_source'],
        #                            item['video_category'], item['video_tag'], item['video_visitor'],
        #                            item['video_create_time'], item['video_update_time'],
        #                            item['video_version'], item['video_deleted'], item['video_href']
        #                            ))

    # def insert_sql(self, item):
    #     sql = """ insert into videohub.video values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    #     self.cursor.execute(sql, (item['video_id'], item['video_vid'], item['video_title'],
    #                               item['video_img'], item['video_description'], item['video_source'],
    #                               item['video_category'], item['video_tag'], item['video_visitor'],
    #                               item['video_create_time'], item['video_update_time'],
    #                               item['video_version'], item['video_deleted'], item['video_href']
    #                               ))


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
        if not os.path.exists(file_path_name):
            print("开始下载文件---》" + file_path_name)
            return file_path_name
        else:
            print(file_path_name + "文件已经下载")

    # def item_completed(self, results, item, info):
    #     return item
