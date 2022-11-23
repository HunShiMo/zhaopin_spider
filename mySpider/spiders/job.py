import json

import scrapy

from mySpider.items import MyspiderItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['163.com']

    def __init__(self):
        super(JobSpider, self).__init__()
        self.url = 'https://hr.163.com/api/hr163/position/queryPage'
        self.count = 2

    def start_requests(self):
        # FormRequest 更适合Scrapy发送POST请求的方法
        yield scrapy.Request(
            url=self.url,
            body=json.dumps({"currentPage": "1", "pageSize": "10"}),
            method="POST",
            headers={
                "Referer": "https://hr.163.com/api/hr163/position/queryPage",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/106.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json"
            },
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        data_list = json.loads(response.text)
        for node in data_list["data"]["list"]:
            item = MyspiderItem()
            item["name"] = node["name"]
            item["link"] = "https://hr.163.com/job-detail.html?id=" + str(node["id"]) + "&lang=zh"
            item["depart"] = node["firstDepName"]
            item["category"] = node["firstPostTypeName"]
            item["reqEdu"] = node["reqEducationName"]
            item["address"] = node["workPlaceNameList"][0]
            item["recruitNum"] = node["recruitNum"]
            item["reqWorkYears"] = node["reqWorkYearsName"]
            item["description"] = node["description"]
            item["requirement"] = node["requirement"]
            item["fileName"] = None
            yield item

        if not data_list["data"]["lastPage"]:
            # 说明还有数据
            yield scrapy.Request(
                url=self.url,
                body=json.dumps({"currentPage": str(self.count), "pageSize": "10"}),
                method="POST",
                headers={
                    "Referer": "https://hr.163.com/api/hr163/position/queryPage",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json"
                },
                callback=self.parse
            )
            self.count += 1
