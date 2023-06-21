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


# con = pymysql.Connect(
#     host="120.25.161.159",
#     port=3306,
#     user="dev",
#     password="dev",
#     database="videohub",
#     charset="utf8",
#     autocommit=True,
# )


class PronHubMysqlPipeline(object):
    #     """
    #     异步操作，连接池
    #     """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        # 连接数据池ConnectionPool，使用pymysql连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_sql, item)

    def insert_sql(self, cursor, item):
        sql = "insert into videohub.video(vid,uid,title,poster,description,sources,category,tag,visitor,create_time," \
              "update_time,version,deleted,href) " \
              "values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"," \
              "\"%s\")" % \
              (item['video_vid'], item['video_uid'], item['video_title'],
               item['video_img'], item['video_description'], item['video_source'],
               item['video_category'], item['video_tag'], item['video_visitor'],
               item['video_create_time'], item['video_update_time'],
               item['video_version'], item['video_deleted'], item['video_href'])
        try:
            cursor.execute(sql)
        except:
            print("添加重复------>" + item['video_vid'] + "------>" + item['video_href'])


class MyspiderPipeline:
    def process_item(self, item, spider):
        return item


class VideoDownloadM3u8TsFilePiPline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item["file_urls"])

    def file_path(self, request, response=None, info=None, *, item=None):
        return str(item['file_name'])

