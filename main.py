import json
import re

import requests
from requests import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.162 Safari/537.36 '
        }

        response = requests.get(url, headers=headers, timeout=1000)
        if response.status_code == 200:
            return response.text

    except RequestException:
        pass


def parse_one_page(html):
    pattern = re.compile(
        '<em class="">(\d+)</em>.*?<a href="(.*?)">.*?' +
        '<img width="100" alt=".*?" src="(.*?)" class=""' +
        '>.*?<span class="title">(.*?)</span>.*?<span ' +
        'class="other">&nbsp;/&nbsp;(.*?)</span>.*?<div ' +
        'class="bd">.*?<p class="">.*?导演: (.*?)&nbsp.*?<br>' +
        '.*?(\d{4})&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)\n' +
        '.*?</p>.*?<span class="rating_num" property="v:' +
        'average">(.*?)</span>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'page_src': item[1],
            'img_src': item[2],
            'title': item[3],
            'other_title': item[4],
            'director': item[5],
            'release_date': item[6],
            'country': item[7],
            'type': item[8],
            'rate': item[9],
        }


def write_to_file(content):
    with open('douban_movie_rankings.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    for offset in range(10):
        url = f'https://movie.douban.com/top250?start={offset * 25}&filter='
        html = get_one_page(url)
        for item in parse_one_page(html):
            print(item)
            write_to_file(item)


if __name__ == '__main__':
    main()
