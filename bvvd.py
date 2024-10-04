from bs4 import BeautifulSoup
import csv
import re

# 读取文件中的HTML内容
with open('input.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有的<td>标签
td_tags = soup.find_all('td')

# 匹配中文的正则表达式
chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

# 打开一个CSV文件来写入数据
with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 遍历所有<td>标签，检查内容中是否包含中文
    for td in td_tags:
        if chinese_pattern.search(td.text):  # 如果包含中文
            writer.writerow([td.text])

print("包含中文的数据已写入 CSV 文件")
