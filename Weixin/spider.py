# -*- coding: utf-8 -*-
# from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *
from db import RedisClient

# client = pymongo.MongoClient(MONGO_URI)
# db = client[MONGO_DB]

base_url = 'https://www.aliexpress.com/store/product/TACVASEN-Men-Camouflage-Tactical-T-shirts-Army-Green-Combat-T-Shirt-Men-Long-Sleeve-Military-T/1495459_32847819010.html?spm=2114.12010615.0.0.1efb9253Y0eUcd'

headers = {
    'Cookie': 'ali_apache_id=10.181.239.29.1497607529213.645931.2; cna=RcPLEZiDxnICAXTMZC1RjRsm; xman_t=PEf0SIyy/TDGnTH2orW45LcoJUiC/Pe/Zrss2+ZNSaNXpqnGSxYP+0eCcQaKPkLzWNcRIpCxSZjmn906R8bQu14gFRnIg+gF5c+gWltWSNk=; ali_beacon_id=10.181.239.29.1497607529213.645931.2; _umdata=535523100CBE37C39A531D812926A20B8D3EE61C518022CEC0D2A4B133D859D51B984989F44D4847CD43AD3E795C914C315C27BDEC3FC8D808AFCDB60D393BF0; _ym_uid=1516358004710639463; _ym_isad=2; xman_f=h9OLfEzHNtH+oDotFeLb7OwzkJhuBfmwSHVoAfdT/zT1/rf4pMY1BPvW3msjVvTzjcJXa8rJebj5quc62ln7lP4zbk4ZyqLBDEkmOibToK1h+FvmNdkxSw==; JSESSIONID=0BB7FBBC126B502E50AC5A53BF6EE00F; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSMnByMndzcnI2NDJzMjUwcjU1cHQ2dTQ1dnIzc3U1MHBT0kkusTI0NTQzNjMyMTQ2NzXSSUxGE8itsDKojQIAorwX5w%3D%3D; _ga=GA1.2.209782813.1515483044; _gid=GA1.2.1894914782.1516280850; _gat=1; xman_us_f=x_l=1&x_locale=en_US; intl_locale=en_US; intl_common_forever=j6Oc46aMwCT97Uv5G9N/6S9k2tvA1Rmh3/zPtdnPRaRlJ3sm8pbv/Q==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932515197626%0932762738557%0932828050789%0932838489116%0932753384222%0932844930933%0932850275270%0932847819010; acs_usuc_t=acs_rt=e6bd8a72f34c4db8a58f98740fe5a18b&x_csrf=1bbjwlury0ojn; aep_usuc_f=site=glo&region=US&b_locale=en_US&c_tp=USD; isg=BOXl0LZ004WMkTdsONhR75k79KHfipG4OkSayefKl5wr_gVwrnKphHM0jGCIfrFs; ali_apache_track=; ali_apache_tracktmp=',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'authority':'www.aliexpress.com',
    'method':'GET',
    'path':'/store/product/TACVASEN-Men-Camouflage-Tactical-T-shirts-Army-Green-Combat-T-Shirt-Men-Long-Sleeve-Military-T/1495459_32847819010.html?spm=2114.12010615.0.0.1efb9253Y0eUcd',
    'scheme':'https',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, sdch, br',
    'accept-language':'zh-CN,zh;q=0.8',
    'cache-control':'max-age=0',
}


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    conn = RedisClient()
    proxies = conn.randomChoic()
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxies:
            _proxies = {
                'http': 'http://' + proxies
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=_proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
                print('302')
                print('Using Proxy again....')
                return get_html(url)

    except ConnectionError as e:
        print('Error Occurred', e.args)
        count += 1
        return get_html(url, count)



def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = data
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None

# def save_to_mongo(data):
#     if db['articles'].update({'title': data['title']}, {'$set': data}, True):
#         print('Saved to Mongo', data['title'])
#     else:
#         print('Saved to Mongo Failed', data['title'])


def main():
    get_html(base_url)

    # for page in range(1, 101):
    #     html = get_index(KEYWORD, page)
    #     if html:
    #         article_urls = parse_index(html)
    #         for article_url in article_urls:
    #             article_html = get_detail(article_url)
    #             if article_html:
    #                 article_data = parse_detail(article_html)
    #                 print(article_data)
    #                 if article_data:
    #                     save_to_mongo(article_data)



if __name__ == '__main__':
    main()
