# -*- coding: utf-8 -*-
import scrapy
import json
import redis



from octopus.items import Item

import kaptan
config = kaptan.Kaptan(handler='json')
config.import_config('../config.json')

p2p = kaptan.Kaptan(handler='json')
p2p.import_config('./p2p.json')


r = redis.StrictRedis(host=config.get('redis_host', 'localhost'), port=config.get('redis_port', 6379), db=config.get('redis_db', 7) )



"""
1、wsloan 温商贷
2、wzdai 温州贷
3、zfxindai 紫枫信贷
4、zhaoshangdai 招商贷
5、itouzi 爱投资
6、nobank 诺诺磅客
7、翼龙贷 (Pause)
8、sidatz 四达投资
9、zhongbaodai 中宝财富
10、zibenzaixian 资本在线
11、yiqihao 一起好
12、yududai 渝都贷
13、
"""

def out(item):
        data = {'platform': item['platform'], 'name': item['name'], 'apr': item['apr'], 'day': item['day'], 'progress': item['progress']}
        # print json.dumps(data)
        r.lpush('application_data', json.dumps(data))

        # print u'---------%s------' % item['platform']
        # print u'标题: %s' % item['name']
        # print u'年利率: %s' % item['apr']
        # print u'期限: %s' % item['day']
        # print u'进度: %s' % item['progress']
        # print 

class P2PSpider(scrapy.Spider):
    def __init__(self):
        self.data = p2p.get(self.name)
        self.start_urls = self.data['start_urls']

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        nodes = self.data['nodes']
        for node in nodes:
            have_title = node['have_title'] or 0
            for i in res.xpath(node['root']):
                if have_title: 
                    have_title = 0
                    continue
                item = Item(
                    name = self.format_name(i.xpath(node['name']).extract()[0].strip()),
                    apr = self.format_apr(i.xpath(node['apr']).extract()[0].strip()),
                    day = self.format_day(i.xpath(node['day']).extract()[0].strip()),
                    progress = self.format_progress(i.xpath(node['progress']).extract()[0].strip()),
                    platform = self.name
                )
                r.hincrby('platforms', self.name)
                out(item)

    def format_name(self, name):
        return name

    def format_apr(self, apr):
        return apr

    def format_day(self, day):
        return day

    def format_progress(self, progress):
        return progress

class Wzdai(P2PSpider):
    name = 'wzdai'


class Zfxindai(P2PSpider):
    name = 'zfxindai'

class Zhaoshangdai(P2PSpider):

    name = 'zhaoshangdai'
class Sidatz(P2PSpider):

    name = 'sidatz'

class Zibenzaixian(P2PSpider):
    name = 'zibenzaixian'

class Yududai(P2PSpider):

    name = 'yududai'

class Wsloan(scrapy.Spider):
    c_name = u'温商贷'
    name = 'wsloan'

    start_urls = (
        'https://www.wsloan.com/index.aspx',
    )

    def parse(self, res):
        #转贷宝

        node1 = res.xpath('/html/body/div[9]/div/div[2]/div[2]/div/ul') 
        for i in node1:
            item = Item(
                name = i.xpath('li[1]/h3/a/text()').extract()[0].strip(),
                apr = i.xpath('li[2]/span/text()').extract()[0].strip(),
                day = i.xpath('string(li[4])').extract()[0].strip(),
                progress = i.xpath('li[5]/font/text()').extract()[0].strip(),
                platform = self.name
            )
            
            out(item)

        #温商宝
        node2 = res.xpath('/html/body/div[9]/div/div[3]/div[2]/div/ul') 
        for i in node2:
            item = Item(
                name = i.xpath('li[1]/h3/a/text()').extract()[0].strip(),
                apr = i.xpath('li[2]/span/text()').extract()[0].strip(),
                day = i.xpath('string(li[4])').extract()[0].strip(),
                progress = i.xpath('li[5]/font/text()').extract()[0].strip(),
                platform = self.name
            )

            out(item)



class Itouzi(scrapy.Spider):
    """ 通过 GET ，获取标的JSON格式数据 """
    c_name = u'爱投资'

    name = 'itouzi'

    start_urls = ('http://www.itouzi.com/dinvest/ajax/list?type=2', )

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        node = json.loads(res.body)
        for i in node['data']['borrows']:
            item = Item(
                name = i['name'],
                apr = i['apr'],
                day = i['timeLimit'],
                progress = i['scale'],
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

class Nonobank(scrapy.Spider):
    """ 通过 POST ，获取标的JSON格式数据 """
    c_name = u'诺诺磅客'

    name = 'nonobank'

    start_urls = ('https://www.nonobank.com/Licai/FinancePlanList', )

    def parse(self, res):
        return scrapy.Request(url='https://www.nonobank.com/Licai/GetLicaiList/8/1/', method='POST', callback=self.deal_list)

    def deal_list(self, res):
        r.hset('platforms', self.name, 1)
        node = json.loads(res.body)
        for i in node['members']:
            item = Item(
                name = i['fp_title'],
                apr = '%s ~ %s' % (i['fp_rate_min'], i['fp_rate_max']) ,
                day = i['fp_expect'],
                progress = i['fp_percent'],
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)


class Zhongbaodai(scrapy.Spider):
    c_name = u'中宝贷'
    name = 'zhongbaodai'

    start_urls = ('http://www.zhongbaodai.com/#!/invest', )

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        return scrapy.Request(url='http://www.zhongbaodai.com/service/lending/public_project?limit=10&sort=status+asc%7Cid+desc',  method='GET', callback=self.deal_list)

    def deal_list(self, res):
        node = json.loads(res.body)
        for i in node:
            item = Item(
                name = i['controls'],
                apr = '%s%%' % (float(i['rate']) * 12) ,
                day = u'%s个月' % i['periods'] ,
                progress = float(i['progress']) * 100,
                platform = self.name
            )

            r.hincrby('platforms', self.name)
            out(item)
        



class Yiqihao(scrapy.Spider):
    c_name = u'一起好'
    name = 'yiqihao'

    start_urls = ('https://www.yiqihao.com/loan/list', )

    def parse(self, res):
        return scrapy.Request('https://www.yiqihao.com/loan/list', method='POST', callback=self.deal_list)

    def deal_list(self, res):
        r.hset('platforms', self.name, 1)
        node = json.loads(res.body)
        for i in node['data']['list']:
            item = Item(
                name = i['title'],
                apr = i['apr'],
                day = '%s%s' % (i['deadline'], i['deadline_type']),
                progress = '%s%%' % ( (float(i['remain_amount']) / float(i['amount'])) * 100 ),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

