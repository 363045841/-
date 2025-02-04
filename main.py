import requests
import re
import csv
from bs4 import BeautifulSoup
import time

# URL
urls = []
errorLog = []
tags_map:tuple = {}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'DNT': '1',
    'Host': 'www.zhongyoo.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}
def read_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            urls.append(line.strip())  # 去除每行末尾的换行符

# 从文件读取 URL
read_urls_from_file('urls.txt')
def getFromUrl(url,headers = headers):
    # 发送 GET 请求
    try:
        response = requests.get(url=url)
    except requests.exceptions.Timeout:
        errorLog.append("超时:" + url)
        return

    response_code = None
    try:
        response.encoding = 'gb18030'
        response_code = response.text
    except UnicodeDecodeError:
        errorLog.append("无法解码:" + url)
        return

    soup = BeautifulSoup(response_code, 'html.parser')

    # 找到所有 class 为 'text' 的元素
    text_elements = soup.find_all(class_='text')
    img_tags = soup.find_all('img', attrs={'src': lambda x: x and '/uploads/allimg' in x})
    img_srcs = [img['src'] for img in img_tags]
    # 将提取的数据组合起来
    if len(text_elements) != 0:
        extracted_text = extracted_text = text_elements[-1].get_text(strip=True)
    else:
        errorLog.append("未抓取到text class:" + url)


    pattern = r'【(.*?)】(.*?)(?=【|$)'  # 提取【】中的内容以及其后的描述，直到下一个【或文本结束
    matches = re.findall(pattern, extracted_text, re.S)  # re.S 让.匹配换行符
    for match in matches:
        match:tuple
        if(match[0] not in tags_map):
            tags_map[match[0]] = len(tags_map)

    print("正在爬取:"+matches[0][1]+"\n"+url)
    with open("./data.csv",mode='a',encoding='utf-8',newline='\n') as file:
        writer = csv.writer(file)
        add = [''] * len(tags_map)
        if(len(img_srcs) > 0):
            add.append(img_srcs[0])
        else:
            errorLog.append("未抓取到符合条件的img元素:" + url)
        
        now_ptr: int = 0
        """ while(now_ptr < len(tags_map)):
            if(now_ptr == tags_map[match[0]]):
                add.append(match[1])
            else:
                add.append("")
            now_ptr += 1 """

        add[0] = img_srcs[0]
        for match in matches:
            match: tuple
            add[tags_map[match[0]] + 1] = match[1]

        if(len(add) == 0):
            errorLog.append("写入结果为空,已拦截该次写入:" + url)
        else:
            writer.writerow(add)

for url in urls:
    getFromUrl(url)
    if(url != urls[-1]):
        time.sleep(10)

if(len(errorLog)>0):
    print("以下URL出现问题,请检查是否有元素未被获取:")
    index = 1
    for i in errorLog:
        print(str(index) + ":" + i)
        index += 1
else:
    print("全部URL解析成功")

    rows = []
    with open('data.csv', mode='r', encoding='utf-8') as file:  # 或者使用 'utf-8-sig'，'gbk'，根据文件实际编码
        reader = csv.reader(file)
        rows = list(reader)
    csv_header = ['img']
    for key in tags_map:
        csv_header.append(key)
    rows.insert(0, csv_header)
    with open('data_with_header.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

