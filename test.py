
import requests
import re
import csv
from bs4 import BeautifulSoup
import time

# URL
urls = []
def read_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            urls.append(line.strip())  # 去除每行末尾的换行符

# 从文件读取 URL
read_urls_from_file('urlsFather.txt')
def getFromUrl(url):
    # 发送 GET 请求
    response = requests.get(url=url)

    # 使用 'iso-8859-1' 编码转换为 'gbk'
    response_code = response.text.encode('iso-8859-1').decode('gbk')

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response_code, 'html.parser')

# 查找所有 href 属性包含但不等于指定字符串的 <a> 标签
    a_tags = soup.find_all('a', href=lambda href: href and 'http://www.zhongyoo.com/name/' in href and href != 'http://www.zhongyoo.com/name/')

    # 提取这些标签的 href 属性
    hrefs = [a['href'] for a in a_tags]
    with open("test.csv", "w", newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        for tag in a_tags:
            writer.writerow([tag['href'], tag.string])
    print(a_tags)

""" for url in urls:
    getFromUrl(url)
    time.sleep(5)
 """

getFromUrl(urls[0])