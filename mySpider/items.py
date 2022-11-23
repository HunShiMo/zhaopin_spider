# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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
