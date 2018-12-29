# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import sys
import requests

sys.path.append('..')

from Util.WebRequest import WebRequest
from Util.utilFunction import getHtmlTree

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

"""
   
"""


class GetFreeProxy(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxyFirst(area=33, page=1):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        :param page: 翻页
        :return:
        """
        area = 33 if area > 33 else area
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                break

    @staticmethod
    def freeProxySecond(page_count=3):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'https://www.xicidaili.com/nn/',  # 高匿
            'https://www.xicidaili.com/nt/',  # 透明
            'https://www.xicidaili.com/wt/',  # 国内http代理
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[1:3])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxyWallFirst():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)



if __name__ == '__main__':
    from CheckProxy import CheckProxy

    CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFirst)
    CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxySecond)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyWallFirst)

    # CheckProxy.checkAllGetProxyFunc()
