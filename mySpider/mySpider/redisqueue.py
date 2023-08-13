import os
import time
from queue import Queue  # 用于创建队列任务
import threading  # 多线程
import redis  # redis 模块
import requests

q = Queue()  # 队列列表

pool = redis.ConnectionPool(host="120.25.161.159", port=6380, password="123456", db=1)  # redis 连接池
red = redis.Redis(connection_pool=pool, decode_responses=True, max_connections=100)  # redis 连接池实例


# def gup():  # 生产者，产生任务丢到远程redis 维护一个队列，用于替代queue
#     for x in range(100):
#         r.lpush("list", x)


def gget():
    while True:  # 进来首先判断一次列表长度，度过为0表示队列空了，退出
        ll = red.llen("file_urls")
        print(ll)
        if ll != 0:
            try:  # 增加代码健壮性
                a = red.lpop("file_urls")  # 维护的list 栈中弹出左侧的key
                # print(a)
                # decode()  byte 转字符串方法
                run(a.decode())
            except Exception as e:
                print(e)
                continue


def ma():
    for x in range(400):  # 创建100个线程 ，充当线程池作用
        th = threading.Thread(target=gget)
        th.start()
    th.join()


def run(file_url):
    video_vid = file_url.split('/')[-3]
    file_path = u'/Volumes/videoHD/{0}'.format(video_vid)
    # file_path_name = file_path + '/' + file_url.split('/')[-1].split('?')[0]
    file_path_name = file_url.split('/')[-1].split('?')[0]
    try:
        if not os.path.exists('{}/{}'.format(file_path, file_path_name)):
            if not os.path.exists('{}'.format(file_path, )):
                os.makedirs(file_path)
            r = requests.get(file_url, timeout=(5, 10))
            with open('{}/{}'.format(file_path, file_path_name), 'wb') as f:
                f.write(r.content)
            print("{}/{}已下载".format(file_path, file_path_name))
        else:
            print("{}/{}已存在".format(file_path, file_path_name))

    except Exception as e:
        print(str(e))
        # print("出现异常，正在自动重新下载！")
        # run(file_url)


if __name__ == '__main__':
    ma()
