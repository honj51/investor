#-*- coding:utf-8 -*-
import redis
import subprocess
import time

import json
import time
from datetime import datetime

DEBUG = True

r = redis.StrictRedis(host='localhost')


def crawl():
    crawl_list = subprocess.Popen(['scrapy', 'list'], stdout=subprocess.PIPE).communicate()[0]
    for crawl in crawl_list.split():
        subprocess.Popen(['scrapy','crawl', crawl], stdout=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
    # redis 是否有 starttime ，如果有，不运行，直接获取redis 的 List 和 Hash 数据

    # if r.get('starttime') is None or DEBUG:
    #     r.set('starttime', datetime.now(), ex=300) # 5分钟的生命周期
    #     r.delete('application_data')
    #     r.delete('platforms')
    #     crawl()
    print json.dumps(r.hgetall('platforms'))
    r.publish('platforms', json.dumps(r.hgetall('platforms')))
    # application_data = r.lrange('application_data', 0, -1)
    # for i in application_data:
    #     r.publish('application_data', i)







# # r.publish('infos', '{name:"海波是个逗逼2"}')

# print r.hgetall('website')


# a = {'name': 'mingiz', 'platform':'platform'}
# a = json.dumps(a)
# print a 

# x = '{"platform": "platform", "name": "mingiz"}'

# r.lpush('x', a)

# b = r.lpop('x')
# print b
# print type(b)
# t = json.loads(b)
# print t['name']

# r.hset('p', 'wzdai', '1')
# r.hincrby('p', 'wzdai')

# r.set('a', 'b', ex=5)