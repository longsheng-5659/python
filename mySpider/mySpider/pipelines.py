# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import redis
# useful for handling different item types with a single interface
from twisted.enterprise import adbapi

from .items import MyItem, MyspiderItem


class PronHubMysqlPipeline(object):
    #     """
    #     异步操作，连接池
    #     """
    def __init__(self, dbpool):
        self.dbpool = dbpool

        pool = redis.ConnectionPool(host="120.25.161.159", port=6380, password="123456", db=1)
        self.red = redis.Redis(connection_pool=pool, decode_responses=True, max_connections=100)

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
            use_unicode=True,
            cp_max=50
        )
        # 连接数据池ConnectionPool，使用pymysql连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数

        return cls(dbpool)

    def process_item(self, item, spider):
        # 判断是否是MyspiderItem模型
        if isinstance(item, MyspiderItem):
            query = self.dbpool.runInteraction(self.insert_sql, item)
            # 判断是否是MyItem模型
        if isinstance(item, MyItem):
            # 先去查询数据库中是否存在vid,避免大量写操作
            self.dbpool.runInteraction(self.Select_sql_for_MyItem, item)
            # 下载文件地址存储到redis 中，下载文件的地址会有过期时间限制，下载的时候判断文件是否重复即可，不用判断redis中的数据是否重复
            # x = self.red.hset(item['video_vid'], item['file_name'], item['file_urls'])
            # y = self.red.sadd(item['video_vid'], item['file_urls'])
            # if x != 0:
            #     self.red.expire(item['video_vid'], 1000)
            # if y != 0:
            #     self.red.expire(item['video_vid'], 1000)

            # 将数据存储到redis队列中
            self.red.lpush("file_urls", item['file_urls'])

    def Select_sql_for_MyItem(self, cursor, item):
        sql = "select id from videohub.items where vid = \"%s\" " % (item['video_vid'])
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                print("查询数据为空，" + item['video_vid'] + "开始插入")
                # 文件数量个数存储到数据库中，可能会有部分数据下载失败，则需要二次判断文件夹内文件个数的完整性，否则需要二次下载
                self.dbpool.runInteraction(self.insert_sql_for_MyItem, item)
        except:
            print("失败")

    def insert_sql_for_MyItem(self, cursor, item):
        sql = "INSERT INTO videohub.items(`vid`, name, `path`, len)VALUES(\"%s\", \"%s\", \"%s\", \"%s\")" \
              % (item['video_vid'], item['file_name'], item['file_path'], item['video_file_len'])
        try:
            cursor.execute(sql)
            print("插入结束" + item['video_vid'])
        except:
            print("失败")

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

# class MyspiderPipeline:
#     def process_item(self, item, spider):
#         return item
#
#   不用原生的下载工具了，太慢了
# class VideoDownloadM3u8TsFilePiPline(FilesPipeline):
#     def get_media_requests(self, item, info):
#         # 重写文件下载,将迭代器生成的数据item拿到，并进行下载文件
#         yield scrapy.Request(url=item["file_urls"])
#
#     def file_path(self, request, response=None, info=None, *, item=None):
#         # 重写文件名称
#         return str(item['file_name'])
