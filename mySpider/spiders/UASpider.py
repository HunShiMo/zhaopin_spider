# -*- coding = utf-8 -*-
# @author: ray
# @date: 2022/11/4 17:24
# @file: UASpider.py
# @software: PyCharm
import pandas as pd
import requests
from lxml import etree


def get():
    url = 'http://useragentstring.com/pages/useragentstring.php?typ=Browser'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)'
    }

    response = requests.get(url, headers=header, timeout=60)
    tree = etree.HTML(response.text)
    browsers = tree.xpath('//ul/li/a/text()')
    # 过滤，长度小于80的不要
    browsers = [browser for browser in browsers if len(browser) > 80]

    # print(browsers)
    print(len(browsers))

    df = pd.DataFrame({'id': range(1, len(browsers) + 1), 'ua': browsers})
    # print(df)

    df.to_csv('../../dataSet/user_agents.csv', index=False)
