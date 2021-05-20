import requests
import math
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

web = Flask("NOAH_donga")


@web.route('/')
def main():
    return render_template('donga_ask.html')


@web.route('/donga_middle')
def mid():
    ask_news = request.args.get("keyword")
    html = requests.get(f'http://dongascience.donga.com/search.php?keyword={ask_news}&category=NEWS')
    bs = BeautifulSoup(html.text, 'html.parser')
    numbers = bs.select_one('#result_news > h3 > span').text.replace('(', '').replace(')', '').replace(',', '')
    return render_template('donga_middle.html', numbers=numbers, keyword=ask_news)


@web.route('/donga_result')
def show_result():
    lists = []
    ask_news = request.args.get('keyword')
    number = request.args.get('number')
    number = int(math.ceil((int(number)//10)))
    for n in range(number):
        # 검색어 가져오는 부분
        html = requests.get(f'http://dongascience.donga.com/search.php?keyword={ask_news}&category=NEWS&page={n}')
        bs = BeautifulSoup(html.text, 'html.parser')
        title = bs.select('#result_news > div.article-A2 > ul > li > a > dl > dd > span.tit')
        information = bs.select('#result_news > div.article-A2 > ul > li > a > dl > dd > span.cont > div')
        date = bs.select('#result_news > div.article-A2 > ul > li > a > dl > dd > span.date')
        news_link = bs.select('#result_news > div.article-A2 > ul > li > a')
        # image = bs.select('#result_news > div.article-A2 > ul > li > a > dl > dt > img')

        for i, j in enumerate(title):
            lists.append({'title': title[i].text, 'information': information[i].text, 'date': date[i].text,
                          'news_link': 'http://dongascience.donga.com' + news_link[i]['href'],
                          })
    # 'image': image[i]['src']
    return render_template('donga_result.html', lists=lists)


web.run()
