# Scrapy settings for mySpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "mySpider"

SPIDER_MODULES = ["mySpider.spiders"]
NEWSPIDER_MODULE = "mySpider.spiders"

# 文件下载地址
# FILES_STORE = "/Volumes/videoHD"
# FILES_STORE = "/Volumes/videoHD"
FILES_STORE = "/"


# minio 文件存储地址
AWS_ENDPOINT_URL = 'http://45.130.147.98:9000'
# 文件存储策略
IMAGES_STORE_S3_ACL = 'public-read'
# 对于自托管，您可能觉得不需要使用SSL，也不需要验证SSL连接
AWS_USE_SSL = False # or True (None by default)
AWS_VERIFY = False # or True (None by default)



# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "mySpider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# ROBOTSTXT_OBEY = True

# 日志等级
LOG_LEVEL = 'INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# 设置延迟
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# 默认并发数量
CONCURRENT_REQUESTS_PER_DOMAIN = 300
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36",
    "Cookie": "accessAgeDisclaimerPH=1"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "mySpider.middlewares.MyspiderSpiderMiddleware": 100,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "mySpider.middlewares.MyspiderDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # "mySpider.pipelines.MyspiderPipeline": 300,
    # "mySpider.pipelines.VideoDownloadM3u8TsFilePiPline": 1,
    "mySpider.pipelines.PronHubMysqlPipeline": 2,
    # "scrapy.pipelines.files.FilesPipeline": 1
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# con = pymysql.Connect(
#     host="120.25.161.159",
#     port=3306,
#     user="dev",
#     password="dev",
#     database="videohub",
#     charset="utf8",
#     autocommit=True,
# )
# 数据库链接信息
# Mysql数据库的配置信息
MYSQL_HOST = '120.25.161.159'  # 主机IP
MYSQL_PORT = 3306  # 数据库端口
MYSQL_DBNAME = 'videohub'  # 数据库名字
MYSQL_USER = 'dev'  # 数据库账号
MYSQL_PASSWD = 'dev'  # 数据库密码

# 增加线程池大小
# REACTOR_THREADPOOL_MAXSIZE = 100
