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
    text_elements = soup.find_all(class_='text')

    # 将提取的数据组合起来
    extracted_text = extracted_text = text_elements[-1].get_text(strip=True)


    pattern = r'【(.*?)】(.*?)(?=【|$)'  # 提取【】中的内容以及其后的描述，直到下一个【或文本结束
    matches = re.findall(pattern, extracted_text, re.S)  # re.S 让.匹配换行符
    print("正在爬取:"+matches[0][1]+"\n"+url)
    with open("./data.csv",mode='a',encoding='utf-8') as file:
        writer = csv.writer(file)
        add = []
        for match in matches:
            add.append(match[1])
        writer.writerow(add)

for url in urls:
    getFromUrl(url)
    time.sleep(5)
