# -*- coding = utf-8 -*-
# @author: ray
# @date: 2022/10/5 16:21
# @file: yanTaiWeather.py
# @software: PyCharm
import json
import re
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup


# import mySpider.items


def requestUrl(headers=None, method="GET", url=None):
    if headers is None or url is None:
        print("headers或url为None，请求终止")
        return
    req = urllib.request.Request(url=url, headers=headers, method=method)
    response = urllib.request.urlopen(req)
    rowData = response.read().decode("utf-8")
    return rowData


def parseDataWithBeautifulSoup(rowdata):
    """
    class MyspiderItem(scrapy.Item):
        name = scrapy.Field()               # 工作名称
        link = scrapy.Field()               # 链接
        depart = scrapy.Field()             # 部门
        category = scrapy.Field()           # 分类
        reqEdu = scrapy.Field()             # 学历
        address = scrapy.Field()            # 位置
        recruitNum = scrapy.Field()         # 人数
        reqWorkYears = scrapy.Field()       # 经验
        description = scrapy.Field()        # 描述
        requirement = scrapy.Field()        # 要求
        jobID = scrapy.Field()              # 工作id
        referrerType = scrapy.Field()       # referrer（不是很懂是什么，组成url的一部分）
        detailUrl = scrapy.Field()          # 详情的URL
        fileName = scrapy.item.Field()      # 文件名
        salary = scrapy.item.Field()        # 薪水
    :param rowdata:
    :return:
    """
    bs = BeautifulSoup(rowdata, 'html.parser')
    res = bs.find(id="__NEXT_DATA__")
    json_data = json.loads(res.text)
    positionList = json_data["props"]["pageProps"]["initData"]["content"]["positionResult"]["result"]
    items = []
    for node in positionList:
        item = {}
        item["name"] = node["positionName"]
        item["link"] = "https://www.lagou.com/wn/jobs/{jobId}.html".format(jobId=node["positionId"])
        item["depart"] = node["companyShortName"]
        item["category"] = node["industryField"]
        item["reqEdu"] = node["education"]
        item["address"] = node["city"]
        item["recruitNum"] = 1
        item["reqWorkYears"] = node["workYear"]
        sumInfo = node["positionDetail"]
        listInfo = str(sumInfo).split("要求")
        if len(listInfo) >= 2:
            item["description"] = listInfo[0]
            item["requirement"] = "要求：" + str(listInfo[1])
        else:
            item["description"] = listInfo[0]
            item["requirement"] = None
        item["jobID"] = node["positionId"]
        item["referrerType"] = None
        item["detailUrl"] = None
        item["fileName"] = None
        item["salary"] = node["salary"]
        items.append(item)

    return items


def saveData(filePath, data):
    if filePath is None:
        print("filePath为None，操作终止")
        return
    file = open(filePath, "a", encoding="utf-8")
    for item in data:
        file.write(json.dumps(item) + "\n")
    file.flush()
    file.close()
    print("数据获取成功，并保存在此位置：{}".format(filePath))


def main():
    url = "https://www.lagou.com/wn/zhaopin?pn={pageIndex}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    filename = "../../dataSet/lagou.json"
    for i in range(1, 31):
        print("第{}次操作".format(i))
        url = url.format(pageIndex=str(i))
        rowData = requestUrl(headers=headers, url=url)
        processedData = parseDataWithBeautifulSoup(rowData)
        saveData(filename, processedData)


if __name__ == '__main__':
    main()
