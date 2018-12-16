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
    pattern = re.compile('<td .*?>(\d+)</td>.*?<td .*?>(\S+)</td>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'value':item[0],
            'name':item[1]
        }

def write_to_file(content):
    print(content)
    with open('result.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+ ',')

def write_header():
    with open('result.json','w',encoding='utf-8') as f:
        f.write('[')

def write_footer():
    with open('result.json','a',encoding='utf-8') as f:
        f.write('{"name":"市辖区","value":"110100","parent":"110000"},{"name":"市辖区","value":"120100","parent":"120000"},{"name":"市辖区","value":"310100","parent":"310000"},{"name":"市辖区","value":"500100","parent":"500000"}]')

url = 'http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20181011221630.html'

html = fetch_page(url)
province = re.compile('0{4}$')
city = re.compile('[1-9]0{2}$')
write_header()
for item in parse_page(html):
    if re.search(province,item.get('value')):
        pass
    elif re.search(city,item.get('value')):
        item['parent'] = re.sub(r'\d{4}$','0000',item.get('value'))
    else:
        item['parent'] = re.sub(r'\d{2}$','00',item.get('value'))
    write_to_file(item)

write_footer()
