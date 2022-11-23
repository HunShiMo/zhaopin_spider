# -*- coding = utf-8 -*-
# @author: ray
# @date: 2022/11/2 19:48
# @file: demo.py
# @software: PyCharm
import json
from urllib.parse import urlencode

import scrapy

from mySpider.items import MyspiderItem


class HighpinSpider(scrapy.Spider):
    name = 'highpin'
    allowed_domains = ['zhaopin.com']

    def start_requests(self):
        for pageIndex in range(1, 151):
            thisBody = {
                "CID": "",
                "Q": "",
                "pageIndex": str(pageIndex),
                "pageSize": "20",
                "ReferrerType": "",
                "qTitle": "",
                "JobLocation": "",
                "CompanyIndustry": "",
                "JobType": "",
                "AnnualSalaryMin": "-1",
                "AnnualSalaryMax": "-1",
                "CompanyType": "",
                "ReleaseDate": "",
                "GID": "5446c6e5-ddfc-4d1b-a208-ba2e24f35059"
            }
            firstRequest = scrapy.http.Request(
                url='https://zpdata.zhaopin.com/api/JobSearch/Search?x-zp-client-id=f832fc86-0429-47c1-acd0-cc6fd2390f7c',
                body=urlencode(thisBody),
                method="POST",
                meta={"thisFileName": str(pageIndex)},
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "zpdata.zhaopin.com",
                    "Origin": "https://highpin.zhaopin.com",
                    "Pragma": "no-cache",
                    "Referer": "https://highpin.zhaopin.com/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/107.0.0.0 Safari/537.36",
                },
            )
            yield firstRequest

    # 第一次解析请求
    def parse(self, response, **kwargs):
        data_list = json.loads(response.body)
        # print("data_list-----", data_list)
        items = []
        thisFileName = response.meta["thisFileName"]
        for node in data_list["body"]["JobList"]:
            item = MyspiderItem()
            item["name"] = node["JobTitle"]
            item["link"] = "https://highpin.zhaopin.com/job/b{JobID}.html".format(JobID=node["JobID"])
            item["reqEdu"] = node["JobDegree"]
            item["address"] = node["JobLactionStr"]
            item["reqWorkYears"] = node["WorkExperience"]
            item["jobID"] = node["JobID"]
            item["referrerType"] = node["ReferrerType"]
            item["detailUrl"] = "https://highpin.zhaopin.com/api/job/GetPositionDetail?" \
                                "jobID={jobID}" \
                                "&referrerType={referrerType}" \
                .format(jobID=str(node["JobID"]), referrerType=str(node["ReferrerType"]))
            item["fileName"] = thisFileName
            item["salary"] = str(node["AnnualSalaryMin"]) + "-" + str(node["AnnualSalaryMax"])
            items.append(item)

        for item in items:
            secondRequest = scrapy.http.Request(
                url=item["detailUrl"],
                headers={
                    "content-type": "application/json",
                    "accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/106.0.0.0 Safari/537.36"
                },
                meta={"item": item},
                callback=self.detail_parse
            )
            yield secondRequest

    def detail_parse(self, response):
        item = response.meta["item"]
        detailInfo = json.loads(response.text)
        item["depart"] = None
        item["category"] = detailInfo["body"]["Type"]
        item["recruitNum"] = detailInfo["body"]["RecruitCount"]
        # print("detail_parse被调用了------{}".format(item["recruitNum"]))
        # 因为这个招聘网站将数据岗位描述和岗位要求保存在同一个字段了，所以我们需要将他拆开
        sumInfo = detailInfo["body"]["Responsibility"]
        listInfo = str(sumInfo).split("任职要求")

        if len(listInfo) >= 2:
            item["description"] = listInfo[0]
            item["requirement"] = "任职要求" + str(listInfo[1])
        else:
            item["description"] = listInfo[0]
            item["requirement"] = None

        yield item
