import logging
import re

import execjs
import scrapy
from redis import Redis
from scrapy.http import HtmlResponse

from ..items import MyspiderItem, DownloadM3u8Ts, MyItem

red = Redis(host="120.25.161.159", port=6380, password="123456")


class PronhubSpider(scrapy.Spider):
    name = "pronhub"
    base_url = ["https://jp.pornhub.com/"]
    allowed_domains = ["jp.pronhub.com"]

    def start_requests(self):
        # start_requests_url_list = []
        for i in self.base_url:
            for x in range(1, 100):
                start_requests_url = i + "video?page=" + str(x)
                yield scrapy.Request(start_requests_url)

    def parse(self, response, **kwargs):
        sel = response.css('.pcVideoListItem.js-pop.videoblock.videoBox ')
        # sel = response.css('.wrap ')
        video_temp = {}

        for x in sel:
            # 创建items 对象
            Movie_item = MyspiderItem()

            # 视频id
            sel_video_id = x.css('li::attr(data-video-id)').get()
            video_temp["sel_video_id"] = sel_video_id
            Movie_item["video_id"] = sel_video_id

            # 视频链接
            sel_href = x.css('a::attr(href)').get()
            sel_id_href = response.urljoin(sel_href)
            video_temp['sel_href'] = sel_id_href
            Movie_item['video_id_href'] = sel_id_href

            # 存入redis 数据库
            result = red.sadd("pronHub:start:requests:url", sel_id_href)
            # Movie_item['video_href'] = sel_href
            # 完整视频链接

            # 视频id地址
            sel_img = x.css('img::attr(src)').get()
            video_temp['sel_img'] = sel_img
            Movie_item['video_img'] = sel_img
            # 视频 标题
            sel_title = x.css('img::attr(alt)').get()
            video_temp['video_title'] = sel_title
            Movie_item['video_title'] = sel_title

            # 视频时长
            sel_var = x.css('var::text').get()
            video_temp['sel_var'] = sel_var
            Movie_item['video_var'] = sel_var
            # print(video_temp)
            # dont_filter = True  是表示不进行域名过滤
            if result:
                yield scrapy.Request(sel_id_href, callback=self.video_page, dont_filter=True)
            else:
                print("已经重复插入了数据"+str(sel_id_href))
            # yield scrapy.Request(sel_id_href, callback=self.video_page, dont_filter=True)

    def video_page(self, response: HtmlResponse):

        js = response.css('div.video-wrapper').css('#player').css('script').get()
        prepare_js = js.split('<script type="text/javascript">')[1].split('var nextVideoPlaylistObject')[0]
        # 编译js片段
        js_compiled = execjs.compile(prepare_js)
        videoQuality = ["1080P_4000K", "720P_4000K", "480P_2000K", "240P_1000K"]
        # 找到画质最高的视频链接
        media_url = ''
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

        m3u8_Ts_url_index = media_url.replace("master.m3u8", 'index-v1-a1.m3u8')
        downloadM3u8Ts['m3u8_Ts_url_index'] = m3u8_Ts_url_index
        response_meta = scrapy.Request(m3u8_Ts_url_index, callback=self.download_m3u8, dont_filter=True)
        # response_meta = scrapy.Request(m3u8_Ts_url_index, dont_filter=True)
        response_meta.meta['downloadM3u8Ts'] = downloadM3u8Ts
        # response_meta.meta = self.proxy
        yield response_meta

    def download_m3u8(self, response):
        m3u8_url_ts_list = []
        m3u8_list = response.text.splitlines()
        # response.meta 是进行函数间参数传递
        m3u8_Ts_url_index = response.meta['downloadM3u8Ts']['m3u8_Ts_url_index']
        m3u8_url_ts_list.append(m3u8_Ts_url_index)
        # 遍历所有Ts文件数据
        myItem = MyItem()
        print("遍历所有的TS文件----->")
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
            myItem['file_urls'] = m3u8_url_ts_list_set[x]
            yield myItem
