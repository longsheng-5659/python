import logging
import os
import random
import re
import time

import execjs
import scrapy
from redis import Redis
from scrapy.http import HtmlResponse
from ..items import MyspiderItem, DownloadM3u8Ts, MyItem

red = Redis(host="120.25.161.159", port=6380, password="123456")


class PronhubSpider(scrapy.Spider):
    name = "pronhub"
    base_url = ["https://jp.pornhub.com/"]
    # base_url = ["https://jp.pornhub.com/"]
    allowed_domains = ["cn.pronhub.com"]

    # allowed_domains = ["jp.pronhub.com"]

    def start_requests(self):

        # start_requests_url_list = []
        for i in self.base_url:
            for x in range(1, 5):
                start_requests_url = i + "video?page=" + str(x)
                # 开始的url 并生产迭代器，其中的数据给到parse 函数
                yield scrapy.Request(start_requests_url)

    def parse(self, response, **kwargs):
        # 拿到response数据进行请求
        sel = response.css('.pcVideoListItem.js-pop.videoblock.videoBox ')
        # sel = response.css('.wrap ')
        for x in sel:
            # 创建items 对象
            Movie_item = MyspiderItem()
            # 视频id
            sel_video_id = x.css('li::attr(data-video-id)').get()
            Movie_item["video_vid"] = sel_video_id
            # 作者id随便取
            Movie_item["video_uid"] = 24531
            # 视频链接
            sel_id_href = x.css('a::attr(href)').get()
            sel_href = response.urljoin(sel_id_href)
            # 时间链接
            Movie_item['video_href'] = sel_href
            # 视频地址json
            Movie_item['video_source'] = {}
            # 分类
            Movie_item['video_category'] = "分类"
            # 标签
            Movie_item['video_tag'] = "标签"
            # 作者
            Movie_item['video_visitor'] = random.randint(int(time.time() * 10000), int(time.time() * 100000))
            # 创建时间
            Movie_item['video_create_time'] = int(time.time() * 10000)
            # 更新时间
            Movie_item['video_update_time'] = int(time.time() * 10000)
            # 版本号
            Movie_item['video_version'] = 1
            # 是否删除
            Movie_item['video_deleted'] = 0
            # 图片
            sel_img = x.css('img::attr(src)').get()
            Movie_item['video_img'] = sel_img
            # 视频 标题
            sel_title = x.css('img::attr(alt)').get()
            Movie_item['video_title'] = str(sel_title)
            # 视频描述（取值标题）
            Movie_item['video_description'] = str(sel_title)

            # 视频时长
            sel_var = x.css('var::text').get()
            Movie_item['video_var'] = sel_var
            # print(Movie_item)
            # yield Movie_item

            # callback 函数回调video_page函数
            yield scrapy.Request(sel_href, callback=self.video_page, dont_filter=True)

    def video_page(self, response: HtmlResponse):
        # 拿到response数据进行解析
        js = response.css('div.video-wrapper').css('#player').css('script').get()
        prepare_js = js.split('<script type="text/javascript">')[1].split('var nextVideoPlaylistObject')[0]
        # 编译js片段
        js_compiled = execjs.compile(prepare_js)
        videoQuality = ["1080P_4000K", "720P_4000K", "480P_2000K", "240P_1000K"]
        # 找到画质最高的视频链接
        # media_url = ''
        downloadM3u8Ts = DownloadM3u8Ts()
        for x in range(len(videoQuality)):
            for i in range(0, 4):
                # 获取js代码的变量
                media_url = js_compiled.eval('media_' + str(i))
                if len(re.findall(videoQuality[x], media_url)) != 0:
                    print("找到media_url----->" + media_url + 'videoQuality[x]-->' + videoQuality[x])
                    downloadM3u8Ts['m3u8_Ts_url_master'] = media_url
                    break
            else:
                continue
            break

        m3u8_Ts_url_index = downloadM3u8Ts['m3u8_Ts_url_master'].replace("master.m3u8", 'index-v1-a1.m3u8')
        downloadM3u8Ts['m3u8_Ts_url_index'] = m3u8_Ts_url_index

        # 回调donload_m3u8函数
        response_meta = scrapy.Request(m3u8_Ts_url_index, callback=self.download_m3u8, dont_filter=True)
        response_meta.meta['downloadM3u8Ts'] = downloadM3u8Ts
        # meta 函数是将数据进行函数间的传递，
        yield response_meta

    def download_m3u8(self, response):
        m3u8_url_ts_list = []
        m3u8_list = response.text.splitlines()
        # response.meta 是进行函数间参数传递
        m3u8_Ts_url_index = response.meta['downloadM3u8Ts']['m3u8_Ts_url_index']
        m3u8_url_ts_list.append(m3u8_Ts_url_index)
        # 遍历所有Ts文件数据
        myItem = MyItem()
        # print("遍历所有的TS文件----->")
        for i in range(0, len(m3u8_list)):
            m3u8_file_name_list = re.findall(r'(.*?)\?', m3u8_list[i], re.S)
            if len(m3u8_file_name_list) != 0:
                m3u8_url_ts = m3u8_Ts_url_index.replace("index-v1-a1.m3u8", m3u8_file_name_list[0])
                # myItem['file_urls'] = m3u8_url_ts
                # 返回的是所有的所有数据的Ts文件
                m3u8_url_ts_list.append(m3u8_url_ts)
                # yield myItem
        m3u8_url_ts_list_set = list(set(m3u8_url_ts_list))
        for x in range(1, len(m3u8_url_ts_list_set)):
            #     myItem = MyItem()
            myItem["file_urls"] = m3u8_url_ts_list_set[x]
            myItem["video_file_len"] = len(m3u8_url_ts_list_set)
            # 视频id作为文件夹
            file_path = u'/Volumes/videoHD/{0}'.format(m3u8_url_ts_list_set[x].split('/')[-3])
            file_path_name = file_path + '/' + m3u8_url_ts_list_set[x].split('/')[-1].split('?')[0]
            myItem["file_name"] = file_path_name
            myItem["file_path"] = file_path
            if not os.path.exists(file_path):
                print(u"文件夹{0}不存在开始创建".format(file_path))
                os.makedirs(file_path)
            # if len(os.listdir(file_path)) != len(m3u8_url_ts_list_set):
            if not os.path.exists(file_path_name):
                # 如果文件不存在则返回迭代器给文件下载器下载
                yield myItem
            else:
                print(file_path_name + "已经下载")
            # else:
            #     print(file_path + "文件已经全部下载")
