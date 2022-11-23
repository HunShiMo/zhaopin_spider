# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os.path

baseDir = "d:/pythonProject/mySpider/dataSet/"


class WangYiSpiderPipeline(object):
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if not os.path.exists(baseDir):
            os.mkdir(baseDir)
            if not os.path.exists(baseDir):
                raise RuntimeError("不可能，绝对不可能看到这个异常。ps：{}目录不存在".format(baseDir))
        if spider.name == "job":
            self.file = open(baseDir + "wangYi" + ".json", "w")

    def process_item(self, item, spider):
        if spider.name == "job":
            item = dict(item)
            str_data = json.dumps(item) + '\n'
            self.file.write(str_data)
            self.file.flush()

        return item

    def close_spider(self, spider):
        if spider.name == "job":
            if self.file is not None:
                self.file.flush()
                self.file.close()


class HighPinSpiderPipeline(object):

    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if not os.path.exists(baseDir):
            os.mkdir(baseDir)
            if not os.path.exists(baseDir):
                raise RuntimeError("不可能，绝对不可能看到这个异常。ps：{}目录不存在".format(baseDir))
        if spider.name == "highpin":
            self.file = open(baseDir + "highPin" + ".json", "w")

    def process_item(self, item, spider):
        if spider.name == "highpin":
            item = dict(item)
            str_data = json.dumps(item) + '\n'
            self.file.write(str_data)
            self.file.flush()

        return item

    def close_spider(self, spider):
        if spider.name == "highpin":
            if self.file is not None:
                self.file.flush()
                self.file.close()

class AliSpiderPipeline(object):

    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if not os.path.exists(baseDir):
            os.mkdir(baseDir)
            if not os.path.exists(baseDir):
                raise RuntimeError("不可能，绝对不可能看到这个异常。ps：{}目录不存在".format(baseDir))
        if spider.name == "alispider":
            self.file = open(baseDir + "ali" + ".json", "w")

    def process_item(self, item, spider):
        if spider.name == "alispider":
            item = dict(item)
            str_data = json.dumps(item) + '\n'
            self.file.write(str_data)
            self.file.flush()

        return item

    def close_spider(self, spider):
        if spider.name == "alispider":
            if self.file is not None:
                self.file.flush()
                self.file.close()

