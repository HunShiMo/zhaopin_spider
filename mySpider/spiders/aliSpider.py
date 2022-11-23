# -*- coding = utf-8 -*-
# @author: ray
# @date: 2022/11/2 19:48
# @file: demo.py
# @software: PyCharm
import json
import scrapy
from mySpider.items import MyspiderItem


class AliSpider(scrapy.Spider):
    name = 'alispider'
    allowed_domains = ['alibaba.com']

    def __init__(self, **kwargs):
        super(AliSpider, self).__init__()
        self.index = 1

    def start_requests(self):
        this_body = {
            "channel": "group_official_site",
            "language": "zh",
            "batchId": "",
            "categories": "",
            "deptCodes": [],
            "key": "",
            "pageIndex": self.index,
            "pageSize": 10,
            "regions": "",
            "subCategories": ""
        }
        this_cookies = "cna=xb/sGwgjJgUCATo5G/QmT6Uj; " \
                       "xlly_s=1; " \
                       "prefered-lang=zh; " \
                       "XSRF-TOKEN=e8f67d91-5c61-4d45-bf74-a01e243f51e7; " \
                       "SESSION=NUVFNTJCOEM2MjQ5QzNDMEI2MkNGQzZBNkNGMUZDRDI=; " \
                       "tfstk=cfjPBNj23uEzkxbobnKFb_nyBgGRCq6lKmJ6rWvvFFt-kbP26T5mGXp0U492dxlHr; " \
                       "isg=BKGhnbk3Zhbpm8rhYL7Z__PPsG27ThVAIePw2QNCsKqMas08SJxEEvtrzJ5soq14; " \
                       "l=eBOcBPeITJJD88mGBO5wlurza77ONGAXGsPzaNbMiIncC6eP9zpOfE-QmbOiHdKRR8XVMsYe4oV4bMJtLFw45PBZndLHR5jqq0OMuFLC."
        this_cookies = this_cookies.split(";")
        keys = (str(item.split("=")[0]).strip() for item in this_cookies)
        values = (str(item.split("=")[1]).strip() for item in this_cookies)
        dict_cookies = dict(zip(keys, values))
        yield scrapy.Request(
            url="https://talent.alibaba.com/position/search?_csrf=e8f67d91-5c61-4d45-bf74-a01e243f51e7",
            body=json.dumps(this_body),
            method="POST",
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "Origin": "https://talent.alibaba.com",
                "Pragma": "no-cache",
                "Referer": "https://talent.alibaba.com/off-campus/position-list?lang=zh",
                "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0; rv:1.9.1b4pre) Gecko/20090419 SeaMonkey/2.0b1pre",
                "Host": "talent.alibaba.com",
            },
            cookies=dict_cookies,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        data_list = json.loads(response.text)
        if data_list["success"]:
            for node in data_list["content"]["datas"]:
                item = MyspiderItem()
                item["name"] = node["name"]
                item["link"] = "https://talent.alibaba.com/" + node["positionUrl"]
                item["depart"] = node["department"]
                if node["categories"] is not None:
                    item["category"] = " ".join(node["categories"])
                else:
                    item["category"] = None
                item["reqEdu"] = node["degree"]
                if node["workLocations"] is not None:
                    item["address"] = node["workLocations"][0]
                else:
                    item["address"] = None
                item["recruitNum"] = None
                item["reqWorkYears"] = node["experience"]["from"]
                item["description"] = node["description"]
                item["requirement"] = node["requirement"]
                item["requirement"] = node["requirement"]
                item["jobID"] = None
                item["referrerType"] = None
                item["detailUrl"] = None
                item["fileName"] = None
                yield item

            if int(data_list["content"]["currentPage"]) * int(data_list["content"]["pageSize"]) \
                    < int(data_list["content"]["totalCount"]):
                self.index += 1
                this_body = {
                    "channel": "group_official_site",
                    "language": "zh",
                    "batchId": "",
                    "categories": "",
                    "deptCodes": [],
                    "key": "",
                    "pageIndex": self.index,
                    "pageSize": 10,
                    "regions": "",
                    "subCategories": ""
                }
                this_cookies = "cna=xb/sGwgjJgUCATo5G/QmT6Uj; " \
                               "xlly_s=1; " \
                               "prefered-lang=zh; " \
                               "XSRF-TOKEN=e8f67d91-5c61-4d45-bf74-a01e243f51e7; " \
                               "SESSION=NUVFNTJCOEM2MjQ5QzNDMEI2MkNGQzZBNkNGMUZDRDI=; " \
                               "tfstk=cfjPBNj23uEzkxbobnKFb_nyBgGRCq6lKmJ6rWvvFFt-kbP26T5mGXp0U492dxlHr; " \
                               "isg=BKGhnbk3Zhbpm8rhYL7Z__PPsG27ThVAIePw2QNCsKqMas08SJxEEvtrzJ5soq14; " \
                               "l=eBOcBPeITJJD88mGBO5wlurza77ONGAXGsPzaNbMiIncC6eP9zpOfE-QmbOiHdKRR8XVMsYe4oV4bMJtLFw45PBZndLHR5jqq0OMuFLC."
                this_cookies = this_cookies.split(";")
                keys = (str(item.split("=")[0]).strip() for item in this_cookies)
                values = (str(item.split("=")[1]).strip() for item in this_cookies)
                dict_cookies = dict(zip(keys, values))
                yield scrapy.Request(
                    url="https://talent.alibaba.com/position/search?_csrf=e8f67d91-5c61-4d45-bf74-a01e243f51e7",
                    body=json.dumps(this_body),
                    method="POST",
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cache-Control": "no-cache",
                        "Content-Type": "application/json",
                        "Origin": "https://talent.alibaba.com",
                        "Pragma": "no-cache",
                        "Referer": "https://talent.alibaba.com/off-campus/position-list?lang=zh",
                        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0; rv:1.9.1b4pre) Gecko/20090419 SeaMonkey/2.0b1pre",
                        "Host": "talent.alibaba.com",
                    },
                    cookies=dict_cookies,
                    callback=self.parse
                )
