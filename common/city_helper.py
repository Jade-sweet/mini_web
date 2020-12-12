import requests
from lxml import etree
import pypinyin


# 爬虫获得数据
def get_page(url):
    url = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


# 获取区域，如龙泉驿区
def get_county_helper(url):
    data = get_page(url)
    html_data = etree.HTML(data)
    county_list = html_data.xpath('//ul[@data-target="area"]//li/a/text()')
    results = []
    for i, item in enumerate(county_list[1:]):
        results.append({'num': i, 'value': item})
    return results


# 获取街道，如十陵街道
def get_street_helper(url):
    data = get_page(url)
    html_data = etree.HTML(data)
    street_list = html_data.xpath('//ul[@data-target="area"][2]//li/a/text()')
    return street_list[1:]


def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s
