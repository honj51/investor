#-*- coding:utf-8 -*-
import redis
import subprocess
import json
import time

from datetime import datetime

import kaptan

def crawl():
    crawl_list = subprocess.Popen(['scrapy', 'list'], stdout=subprocess.PIPE).communicate()[0]
    for crawl in crawl_list.split():
        if len(crawl) < 12:  # 正确的爬虫name
            subprocess.Popen(['scrapy','crawl', crawl], stdout=subprocess.PIPE).communicate()[0]

if __name__ == '__main__':
    # redis 是否有 starttime ，如果有，不运行，直接获取redis 的 List 和 Hash 数据
    config = kaptan.Kaptan(handler='json')
    config.import_config('../config.json')

    r = redis.StrictRedis(host=config.get('redis_host', 'localhost'), port=config.get('redis_port', 6379), db=config.get('redis_db', 7) )

    if r.get('starttime') is None:
        r.set('starttime', datetime.now(), ex=300) # 5分钟的生命周期
        r.delete('application_data')
        r.delete('platforms')
        crawl()

    r.publish('platforms', json.dumps(r.hgetall('platforms')))
    application_data = r.lrange('application_data', 0, -1)
    for i in application_data:
        r.publish('application_data', i)
