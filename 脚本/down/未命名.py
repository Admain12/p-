import requests
from bs4 import BeautifulSoup

# 1. 发送请求
url = "https://example.com"  # 目标网页
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}  # 伪装浏览器，避免被反爬
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding  # 解决编码问题

# 2. 解析页面
soup = BeautifulSoup(response.text, "lxml")

# 3. 提取数据
title = soup.title.string  # 提取标题
content = soup.find("div", class_="content").get_text()  # 提取class为content的div标签文本

# 4. 存储数据
with open("data.txt", "w", encoding="utf-8") as f:
    f.write(f"标题：{title}\n正文：{content}")

print("爬取完成！")

