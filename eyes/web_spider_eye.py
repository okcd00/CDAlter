# coding = utf8
# =====================================================
#   Copyright (C) 2016-2021 All rights reserved.
#
#   filename : SpiderEye.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2020-11-17
#   desc     : Spider as Eye, using dblp spider as an example.
# =====================================================
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from configparser import RawConfigParser


USER_AGENT_STORE = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
]


class SpiderEye(object):
    def __init__(self):
        cf = RawConfigParser()
        cf.read('config')

        self.runtime = cf.getint('info', 'runtime')
        self.debug = cf.getboolean('action', 'debug')

        self.headers = {
            'Host': 'www.baidu.com',
            'Connection': 'keep-alive',
            # 'Pragma': 'no-cache',
            # 'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': USER_AGENT_STORE[-4],
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        }
        self.s = requests.Session()

    def update_headers_with_cookie(self):
        self.headers.update({'Cookie': ';'.join(['{}={}'.format(k, v) for k, v in self.s.cookies.items()])})

    @staticmethod
    def show_http_request(url, data):
        request_str = '{}'.format(url)
        if data is not None:
            request_str += '?'
            request_str += '&'.join(['{}={}'.format(k, v) for k, v in data.items()])
        return request_str

    def show_response(self, response, url="", data=None, description=""):
        if 200 <= int(response.status_code) < 300:
            status_str = "Link Success"
        else:
            status_str = "Link failed with code {}".format(int(response.status_code))
        print('[{}] {}'.format(description, status_str))
        if self.debug:
            print("\tReq as {}".format(self.show_http_request(url, data)))
            print("\tView as {}".format(response.url))
            print("\tCookie: {}".format(self.s.cookies.get_dict()))

    def session_get(self, url, data=None, desc="GET"):
        response = self.s.get(
            url=url, data=data, headers=self.headers)
        self.show_response(
            response, url, data, description=desc)
        self.update_headers_with_cookie()
        return response

    def session_post(self, url, data=None, desc="POST"):
        response = self.s.post(
            url=url, data=data, headers=self.headers)
        self.show_response(
            response, url, data, description=desc)
        self.update_headers_with_cookie()
        return response

    def login(self, login_url, post_data):
        response = self.s.post(
            login_url, data=post_data, headers=self.headers)
        self.show_response(response, login_url, post_data, 'Login')

    @staticmethod
    def get_message(result_text):
        # override this function
        css_soup = BeautifulSoup(result_text, 'html.parser')

        # text = css_soup.select('#main-content > div > div.m-cbox.m-lgray > div.mc-body > div')[0].text
        text = css_soup.select('#conf\/acl\/2018-1 > cite')[0].text
        return "".join(line.strip() for line in text.split('\n'))

    def capture_dblp_list(self, url=None, response=None,
                          key_words=None, position='#main > ul'):
        results = []
        if response is None:
            # url = 'https://dblp.uni-trier.de/db/conf/acl/acl2018-1.html'
            response = self.session_get(url)
        css_soup = BeautifulSoup(response.text, 'html.parser')
        for ul in css_soup.select(position):
            for li in ul.find_all("li", recursive=False):
                title = li.select('> cite > span.title')
                if not title:
                    continue
                title = title[0].text
                if key_words:
                    if True not in [ts in title for ts in key_words]:
                        continue
                urls = [x.a['href'] for x in li.select('> nav > ul > li > div > ul > li.ee')]
                results.append({
                    'id': li['id'],
                    'url': urls,
                    'title': title,
                    'citation': li.select('> cite')[0].text,
                })
            # results.append(cite.text)
        return results

    def generate_dblp_page(self, key_words, venue=None):
        url = "https://dblp.uni-trier.de/search?q="
        url += "{}".format('+'.join(key_words))
        if venue:
            url += "+venue:{}:".format(venue)
        print("Generated Url: {}".format(url))
        return self.capture_dblp_list(
            url=url, position='#completesearch-publs > div > ul')

    def __call__(self, url):
        self.s.get(url, headers=self.headers)


if __name__ == "__main__":
    se = SpiderEye()
    target_list = se.generate_dblp_page(
        key_words=['entity', 'context'], venue='ACL')
    pprint(target_list)
