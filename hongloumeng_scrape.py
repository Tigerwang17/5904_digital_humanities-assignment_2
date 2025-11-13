import requests
from bs4 import BeautifulSoup
import re
import time

url_lists = [
    'https://ctext.org/hongloumeng/ch1/zhs',
    'https://ctext.org/hongloumeng/ch2/zhs',
    'https://ctext.org/hongloumeng/ch3/zhs',
    'https://ctext.org/hongloumeng/ch4/zhs',
    'https://ctext.org/hongloumeng/ch5/zhs',
    'https://ctext.org/hongloumeng/ch6/zhs',
    'https://ctext.org/hongloumeng/ch7/zhs',
    'https://ctext.org/hongloumeng/ch8/zhs',
    'https://ctext.org/hongloumeng/ch9/zhs',
    'https://ctext.org/hongloumeng/ch10/zhs',
    'https://ctext.org/hongloumeng/ch11/zhs',
    'https://ctext.org/hongloumeng/ch12/zhs',
    'https://ctext.org/hongloumeng/ch13/zhs',
    'https://ctext.org/hongloumeng/ch14/zhs',
    'https://ctext.org/hongloumeng/ch15/zhs'
]


def scrape_hongloumeng(url):
    try:
        # 发送HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        time.sleep(2)

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 确保正确编码

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None

        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有包含道德经文本的td元素
        text_tds = soup.find_all('td', class_='ctext')

        hongloumeng_text = []

        for text_td in text_tds:

            if 'opt' not in text_td.get('class', []):  # 确保不是标题行
                text = text_td.get_text(strip=True)
                if text and len(text) > 5 :  # 确保是实质性的文本
                    # 移除可能的注释引用（如[1]、[2]等）
                    text = re.sub(r'\[\d+\]', '', text)
                    hongloumeng_text.append(text)
        chapter_match = re.search(r'/ch(\d+)', url)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
        else:
            chapter_num = 1
        return hongloumeng_text,chapter_num

    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return [], 0

def save_to_file(text_list,chapter_num):
    filename = 'hongloumeng.txt'
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n\n 第{chapter_num}章 \n")
            for i, text in enumerate(text_list, 1):
                f.write(f"{text}\n")
        print(f"内容已保存到 {filename}")
        return True
    except Exception as e:
        print(f"保存文件时出现错误: {e}")
        return False

for url in url_lists:
    hongloumeng_text,chapter_num= scrape_hongloumeng(url)
    print(f'开始爬取第{chapter_num}章')

    if hongloumeng_text:
        # 保存到文件
        if save_to_file(hongloumeng_text,chapter_num):
            print("爬取完成！")
        else:
            print("保存文件失败")
    else:
        print("爬取失败")
