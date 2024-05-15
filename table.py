import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
import pandas as pd

# 配置 Chrome 驱动
service = ChromeService(executable_path='./chromedriver.exe')  # 替换为你的chromedriver路径
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 如果你希望在后台运行浏览器
options.add_argument('--disable-gpu')  # 防止一些系统上的问题
options.add_argument('--no-sandbox')  # 在 Docker 中运行时需要

# 启动浏览器
driver = webdriver.Chrome(service=service, options=options)

# 访问目标网址
url = 'https://news.zhibo8.com/nba/'
driver.get(url)

# 等待页面加载完成
time.sleep(5)  # 等待一段时间让页面加载完全，你可以根据需要调整时间

# 获取页面内容
html_content = driver.page_source

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())
tables = soup.find_all('div', id=lambda x: x and x.startswith('NBA-'))

for i, table_div in enumerate(tables):
    # 设置表格标题
    if i == 0:
        table_title = "西部比赛"
    elif i == 1:
        table_title = "东部赛区"
    else:
        table_title = f"表格_{i+1}"  # 如果有更多表格，以此类推

    # 提取表头
    headers = [th.text for th in table_div.find('tr', class_='colHeader').find_all('th')]

    # 提取表格数据
    data = []
    for row in table_div.find_all('tr')[1:]:
        data.append([td.text for td in row.find_all('td')])

    # 转换为DataFrame
    df = pd.DataFrame(data, columns=headers)

    # 保存为Excel
    filename = f'{table_title}.xlsx'
    df.to_excel(filename, index=False)

driver.quit()
