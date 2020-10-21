# -*- coding: utf-8 -*-
import scrapy
import execjs
import os
import json
import logging
from ..items import TtItem
import user_agent

class ToutiaospiderSpider(scrapy.Spider):
    name = 'toutiaoSpider'
    # allowed_domains = ['toutiao.com']
    # start_urls = ['http://toutiao.com/']
    max_behot_time = 0
    logger = logging.getLogger(__name__)
    # 获取_signature参数
    def get_signature(self,base_url):
        # 改成自己js文件的执行地址
        signature = os.popen('node C:/Users/Administrator/.WebStorm2019.3/config/scratches/test.js {url}'.format(url='"'+base_url+'"')).read()
        return "&_signature=" + signature.replace('\n','').replace(' ','')
    # 获取Cookie参数的s_v_web_id并添加到请求url中并且合并出请求url
    def start_requests(self):
        self.url_list = ['https://www.toutiao.com/c/user/token/MS4wLjABAAAAvazHMceCo3MeM9IJbll231AC8GkJDcrd__iZFw2hi4o/','https://www.toutiao.com/c/user/token/MS4wLjABAAAAHwU9c91tA2IbVqxMwI9Vz4mRO-XzfBUfH2qFSVmqRtTNjyzxIvqDKZKA72s7vPWP/',
                         'https://www.toutiao.com/c/user/token/MS4wLjABAAAAhAKK7LCl_xBflEJTPy1wesrlqc3Kha8jRxiU3-fIR4A/','https://www.toutiao.com/c/user/token/MS4wLjABAAAA9Lz0MeLdJDmqpU26Xi9O_M-cYI9z530wjM7eDKvzZTw/']
        # self.url = 'https://www.toutiao.com/c/user/token/MS4wLjABAAAAvazHMceCo3MeM9IJbll231AC8GkJDcrd__iZFw2hi4o/'
        for u in self.url_list:
            self.url = u
            ctx = execjs.compile("""
                    function to_base36() {
                        var t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("")
                          , e = t.length
                          , n = (new Date).getTime().toString(36)
                          , r = [];
                        r[8] = r[13] = r[18] = r[23] = "_",
                        r[14] = "4";
                        for (var o, i = 0; i < 36; i++)
                            r[i] || (o = 0 | Math.random() * e,
                            r[i] = t[19 == i ? 3 & o | 8 : o]);
                        console.log("verify_" + n + "_" + r.join(""));
                        return "verify_" + n + "_" + r.join("");
                    }
                    """)
            cookie =  ctx.call('to_base36')
            # cookie += 's_v_web_id=' + cookie
            token = self.url.split('/')[-2]
            base_url = 'https://www.toutiao.com/toutiao'
            path = '/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token={token}&max_behot_time={max_behot_time}'.format(
                token=token, max_behot_time=self.max_behot_time)
            base_url += path
            signature = self.get_signature(base_url)
            # path += signature
            base_url += signature
            headers = {
                'scheme': 'https',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'referer': self.url,
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'x-csrftoken': 'undefined'
            }
            cookies = {
                's_v_web_id': cookie
            }
            yield scrapy.Request(base_url.replace('/toutiao', ''),meta={'requests_url':self.url},cookies=cookies,headers=headers,callback=self.parse)
    def parse(self, response):
        # 实例化item
        item = TtItem()
        # response是byte格式
        content = json.loads(response.body.decode('utf-8'))
        titles = content['data']
        for t in titles:
            item['title'] = t['title']
            item['new_url'] = t['display_url']
            item['behot_time'] = t['behot_time']
            yield item
        self.max_behot_time = content['next']['max_behot_time']
        # self.logger.warning(content,'+++++666++++++')
        # 再次进行接口请求
        self.url = response.meta['requests_url']
        ctx = execjs.compile("""
            function to_base36() {
                var t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("")
                  , e = t.length
                  , n = (new Date).getTime().toString(36)
                  , r = [];
                r[8] = r[13] = r[18] = r[23] = "_",
                r[14] = "4";
                for (var o, i = 0; i < 36; i++)
                    r[i] || (o = 0 | Math.random() * e,
                    r[i] = t[19 == i ? 3 & o | 8 : o]);
                console.log("verify_" + n + "_" + r.join(""));
                return "verify_" + n + "_" + r.join("");
            }
            """)
        cookie = ctx.call('to_base36')
        # cookie += 's_v_web_id=' + cookie
        token = self.url.split('/')[-2]
        base_url = 'https://www.toutiao.com/toutiao'
        path = '/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token={token}&max_behot_time={max_behot_time}'.format(
            token=token, max_behot_time=self.max_behot_time)
        base_url += path
        signature = self.get_signature(base_url)
        # path += signature
        base_url += signature
        # 随机生成请求头
        new_user_agent = user_agent.generate_user_agent()
        headers = {
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': self.url,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': new_user_agent,
            'x-csrftoken': 'undefined'
        }
        cookies = {
            's_v_web_id': cookie
        }

        # 之后生成新请求，请求得到的response可以再回调这个parse函数（cookies要传入cookies的参数，写在headers里没用）
        yield scrapy.Request(base_url.replace('/toutiao', ''), meta={'requests_url': self.url,'download_timeout':20}, cookies=cookies,
                             headers=headers, callback=self.parse)




