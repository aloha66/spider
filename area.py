import json
import requests
from requests.exceptions import RequestException
import re
import time


def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    # print(html)
    pattern = re.compile('<td .*?>(\d+)</td>.*?<td .*?>(\S+)</td>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'value':item[0],
            'name':item[1]
        }

def write_to_file(content):
    with open('result.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')


url = 'http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20181011221630.html'

html = fetch_page(url)
for item in parse_page(html):
    write_to_file(item)

