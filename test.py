
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
read_urls_from_file('urls.txt')
def getFromUrl(url):
    # 发送 GET 请求
    response = requests.get(url=url)

    # 使用 'iso-8859-1' 编码转换为 'gbk'
    response_code = response.text.encode('iso-8859-1').decode('gbk')

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response_code, 'lxml')

    # 找到所有 class 为 'text' 的元素

    img_tags = soup.find_all('img', alt=lambda x: x and '功效与作用' in x)
    img_srcs = [img['src'] for img in img_tags]
    print(img_srcs)

for url in urls:
    getFromUrl(url)
    time.sleep(5)
