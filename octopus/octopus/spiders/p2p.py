# -*- coding: utf-8 -*-
import scrapy
import json
import redis

from octopus.items import Item

r = redis.StrictRedis(host='localhost')

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

class Wsloan(scrapy.Spider):
    c_name = u'温商贷'
    name = 'wsloan'

    start_urls = (
        'https://www.wsloan.com/index.aspx',
    )

    def parse(self, res):
        #转贷宝
        r.hset('platforms', self.name, 1)
        node1 = res.xpath('/html/body/div[9]/div/div[2]/div[2]/div/ul') 
        for i in node1:
            item = Item(
                name = i.xpath('li[1]/h3/a/text()').extract()[0].strip(),
                apr = i.xpath('li[2]/span/text()').extract()[0].strip(),
                day = i.xpath('string(li[4])').extract()[0].strip(),
                progress = i.xpath('li[5]/font/text()').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
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
            r.hincrby('platforms', self.name)
            out(item)

class Wzdai(scrapy.Spider):
    c_name = u'温州贷'
    name = 'wzdai'

    start_urls = ('https://www.wzdai.com', )

    def parse(self, res):
        #短期宝
        r.hset('platforms', self.name, 1)
        node1 = res.xpath('/html/body/div[4]/div/div[1]/div[1]/ul')
        for i in node1:
            item = Item(
                name = i.xpath('p/a/text()').extract()[0].strip(),
                apr = i.xpath('string(li/span[3]/font)').extract()[0].strip(),
                day = i.xpath('string(li/span[2]/font)').extract()[0].strip(),
                progress = i.xpath('string(li/span[4]/div/font)').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

        #股盈宝专区
        node2 = res.xpath('/html/body/div[4]/div/div[1]/div[2]/ul')
        for i in node2:
            item = Item(
                name = i.xpath('p/a/text()').extract()[0].strip(),
                apr = i.xpath('string(li/span[3]/font)').extract()[0].strip(),
                day = i.xpath('string(li/span[2]/font)').extract()[0].strip(),
                progress = i.xpath('string(li/span[4]/div/font)').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

        #车宝宝
        node3 = res.xpath('/html/body/div[4]/div/div[1]/div[3]/ul')
        for i in node3:
            item = Item(
                name = i.xpath('p/a/text()').extract()[0].strip(),
                apr = i.xpath('string(li/span[3]/font)').extract()[0].strip(),
                day = i.xpath('string(li/span[2]/font)').extract()[0].strip(),
                progress = i.xpath('string(li/span[4]/div/font)').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

        #借款标列表
        node4 = res.xpath('/html/body/div[4]/div/div[1]/div[4]/ul')
        for i in node4:
            item = Item(
                name = i.xpath('p/a/text()').extract()[0].strip(),
                apr = i.xpath('string(li/span[3]/font)').extract()[0].strip(),
                day = i.xpath('string(li/span[2]/font)').extract()[0].strip(),
                progress = i.xpath('string(li/span[4]/div/font)').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)

class Zfxindai(scrapy.Spider):
    c_name = u'紫枫信贷'

    name = 'zfxindai'

    start_urls = ('http://www.zfxindai.cn', )

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        node = res.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/ul/li')
        menu = 1
        for i in node:
            if menu: 
                menu = 0
                continue
            item = Item(
                name = i.xpath('span[1]/a/text()').extract()[0].strip(),
                apr = i.xpath('string(span[3])').extract()[0].strip(),
                day = i.xpath('string(span[4])').extract()[0].strip(),
                progress = i.xpath('span[5]/span[2]/text()').extract()[0].strip(),
                platform = self.name
            )

            r.hincrby('platforms', self.name)
            out(item)

class Zhaoshangdai(scrapy.Spider):
    c_name = u'招商贷'

    name = 'zhaoshangdai'

    start_urls = ('http://www.zhaoshangdai.com/', )

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        node = res.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div[2]/div')
        menu = 1
        for i in node:
            if menu: 
                menu = 0
                continue
            item = Item(
                name = i.xpath('ul/li[2]/span/a/text()').extract()[0].strip(),
                apr = i.xpath('ul/li[4]/text()').extract()[0].strip(),
                day = i.xpath('string(ul/li[5])').extract()[0].strip(),
                progress = i.xpath('ul/li[7]/div[3]/text()').extract()[0].strip(),
                platform = self.name
            )

            r.hincrby('platforms', self.name)
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


class Sidatz(scrapy.Spider):
    c_name = u'四达投资'
    name = 'sidatz'

    start_urls = ('https://www.sidatz.com/', )

    def parse(self, res):
        #转贷宝
        r.hset('platforms', self.name, 1)
        node = res.xpath('//*[@id="aspnetForm"]/section/div[6]/table[2]/tr')
        menu = 0
        for i in node:
            if menu == 0 : 
                menu  = 1 
                continue
            item = Item(
                name = i.xpath('td[1]/a/text()').extract()[0].strip(),
                day = i.xpath('td[4]/text()').extract()[0].strip(),
                apr = i.xpath('td[5]/b/text()').extract()[0].strip(),
                progress = i.xpath('string(td[6]/span)').extract()[0].strip(),
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
        
class Zibenzaixian(scrapy.Spider):
    c_name = u'资本在线'
    name = 'zibenzaixian'

    start_urls = ('http://www.zibenzaixian.com/jd/want_invest/forwardInvest/borrowing.jd', )

    def parse(self, res):
        r.hset('platforms', self.name, 1)
        node = res.xpath('//*[@id="Tab3"]/div/div[1]/table/tbody')
        for i in node:
            item = Item(
                name = i.xpath('tr/td[1]/div/a/span[1]/text()').extract()[0],
                apr = i.xpath('tr/td[4]/text()').extract()[0].strip(),
                day = i.xpath('tr/td[6]/text()').extract()[0].strip(),
                progress = i.xpath('tr/td[7]/span/i[1]/text()').extract()[0].strip(),
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

class Yududai(scrapy.Spider):
    c_name = u'渝都贷'
    name = 'yududai'

    start_urls = ('http://www.yududai.com/invest/index.html', )


    def parse(self, res):
        r.hset('platforms', self.name, 1)
        node = res.xpath('//div[re:test(@class, "invest-box-list")]')

        for i in node:
            item = Item(
                name = i.xpath('ul/li/span[1]/a[1]/text()').extract()[0].strip(),
                apr = i.xpath('ul/li/span[3]/text()').extract()[0].strip(),
                day = u'%s个月' % (i.xpath('string(ul/li/span[4]/strong)').extract()[0]),
                progress = i.xpath('ul/li/span[6]/b/text()').extract()[0].strip(),
                platform = self.name
            )
            r.hincrby('platforms', self.name)
            out(item)
