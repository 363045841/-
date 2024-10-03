import requests
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

def getFromUrl(url, index):
    print("正在获取：" + url + "(" + str(index) + "/" + str(len(urls)) + ")")
    # 发送 GET 请求
    response = requests.get(url=url)

    # 使用 'iso-8859-1' 编码转换为 'gbk'
    response_code = response.text.encode('iso-8859-1').decode('gbk')

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response_code, 'html.parser')

    # 找到所有 class 为 r2-cons 的 <div> 标签
    divs = soup.find_all('div', {'class': 'r2-cons'})

    hrefs = []
    for div in divs:
        # 在每个 div 中查找 <a> 标签
        a_tags = div.find_all('a', href=lambda href: href and 'http://www.zhongyoo.com/name/' in href and href != 'http://www.zhongyoo.com/name/')
        for tag in a_tags:
            if(tag.string is not None):
                hrefs.append((tag['href'], tag.string))

    # 将结果写入 CSV 文件
    with open("test1.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(hrefs)  # 写入所有 href 和文本内容


# 调用函数

getFromUrl('http://www.zhongyoo.com/name/page_2.html', 0)