# -*- coding: utf-8 -*-

import re
import json
import urllib

from requests import get
from util.constant.enum import *
from lxml import etree

from util.base.time import Time

# Turn &#xxxx; to char.
def ascii_to_str(ascii_match):
    ascii_data = re.findall(r"[0-9]+", ascii_match.group())[0]
    return chr(int(ascii_data, 10))

def html_to_str(html):
    cpl = re.compile(r"&#[0-9]+;")
    html = re.sub(cpl, ascii_to_str, html)
    return html

class HotkeyFetcher(object):

    raw_url="https://search.bilibili.com/video?keyword="
    raw_url_user="https://search.bilibili.com/upuser?keyword="
    keyword=""
    order=["totalrank","click","pubdate","dm","stow"]
    duration={"all":0,"10less":1,"10to30":2,"30to60":3,"60more":4}
    tids_1={"all":0,"cartoon":1,"anime":13,"nat_inno":167,"music":3,\
        "dance":129,"game":4,"tech":36,"digital":188,"life":160,"ghost":119,\
            "fashion":155,"adver":165,"entertain":5,"movie_tel":181,"documen":177,\
                "film":23,"tv_play":11}
    page_number=0

    def __init__(self, **kwargs):
        self.data = None
        self.parse_func=0
        #TODO
        #Get extra args from `kwargs`. Example: headers.
        self.kwargs = kwargs
        self.keyword=kwargs["keyword"]
        self.page_number=kwargs["page_number"]
        self.order_number=kwargs["order_number"]
        self.parse_func=kwargs["parse_func"]
        self.url=self.raw_url+urllib.parse.quote(self.keyword)+\
            "&order="+urllib.parse.quote(str(self.order[self.order_number]))+\
                "&duration=0"+"&tids_1=0"+\
                    "&page="+urllib.parse.quote(str(self.page_number))
        self.url_user=self.raw_url_user+urllib.parse.quote(self.keyword)+\
            "&user_type=1&page=1"
    @property
    def __get_data__(self):
        html_data = self.__fetch_html__
        if self.parse_func == 0:
            parsed_data = self.__parse_html__(html_data)
        elif self.parse_func == 1:
            parsed_data = self.__parse_html_user__(html_data)
        self.data = parsed_data

    def get_data(self, datatype=ENUM_DATATYPE_JSON, limit=0):
        self.__get_data__
        if limit != 0:
            self.data = self.data[:limit]

        if datatype == ENUM_DATATYPE_JSON:
            return self.data

        elif datatype == ENUM_DATATYPE_STRING:
            return json.dumps(self.data)
        else:
            return None

    @property
    def __fetch_html__(self):
        try:
            if self.parse_func == 0:
                req = get(self.url)
            elif self.parse_func == 1:
                req = get(self.url_user)
            # req = get(self.url, **self.kwargs)
            html = req.text
            # html = req.content
        except Exception:
            raise("Bad requests.")
        finally:
            return html

    def __xml_data_iter__(self, html_data):
        if self.parse_func == 0:    
            xpath = """//*[@class=\"video-contain clearfix\"]/li[*]"""
        elif self.parse_func == 1:
            xpath = """//*[@class=\"user-list\"]/li[*]"""
        xml_data = etree.HTML(html_data)
        # xml_data_list=list()
        for data in xml_data.xpath(xpath):
            # xml_data_list.append(data)
            yield data
        # print(len(xml_data_list))
        # return xml_data_list

    def __html_data_iter__(self, html_data):
        xml_data_iter = self.__xml_data_iter__(html_data)
        # data_list = list()
        for xml_data in xml_data_iter:
            # data_list.append(html_to_str(etree.tostring(xml_data).decode("utf-8")))
            yield html_to_str(etree.tostring(xml_data).decode("utf-8"))
        # print(len(data_list))
        # return data_list    

    def __parse_html__(self, html_data):
        html_data_iter = self.__html_data_iter__(html_data)

        dict_data_list = list()
        for html_data in html_data_iter:
            avnumber = re.findall("""<span class=\"type avid\">(.+?)<\/span>""",html_data)
            title = re.findall("""<a title=\"(.+)\" href""", html_data)
            length = re.findall("""<span class=\"so-imgTag_rb\">(.+?)</span>""", html_data)
            playtime = re.findall("""<i class=\"icon-playtime\"/>\s*(.+)\s*""", html_data)
            subtitle =  re.findall("""<i class=\"icon-subtitle\"/>\s*(.+)\s*""",html_data)
            date =  re.findall("""<i class=\"icon-date\"/>\s*(.+)\s*""",html_data)
            upname = re.findall("""class=\"up-name\">(.+)</a>""",html_data)
            
            dict_data_list.append(dict(avnumber=avnumber, title=title, length=length, \
                playtime=playtime, subtitle=subtitle, date=date, upname=upname, time=Time.now_timestamp()))
        try:
            html_data_temp=next(html_data_iter)
        except StopIteration as e:
            print('Generrator return value:', e.value)

        return dict_data_list
    
    def __parse_html_user__(self,html_data):
        html_data_iter = self.__html_data_iter__(html_data)

        dict_data_list = list()
        for html_data in html_data_iter:
            spaceid = re.findall("""<a href=\"//space.bilibili.com/(.+?)\?from.+class=\"face-img\">""",html_data)
            upname = re.findall("""<a href=\"//space.bilibili.com/.+?\?from.+title=\"(.+)\" target=\"_blank\" class=\"face-img\">""", html_data)
            level = re.findall("""<i class=\"lv icon-lv(.+?)\"/>""", html_data)
            submitnum = re.findall("""<span>稿件：([0-9]+)</span>""", html_data)
            fansnum =  re.findall("""<span>粉丝：(.+)</span>""",html_data)
            desc =  re.findall("""<div class=\"desc\">\s*(.+)\s*</div>""",html_data)
            html_data = re.sub("""\r|\n""",'',html_data)
            latest = re.findall("""<a href=\"//www.bilibili.com/video/(.+?)\?.+?class=\"video-desc\">(.+?)</a><span class=\"ptime\">(.+?)</span>""",html_data)
            
            dict_data_list.append(dict(spaceid=spaceid, upname=upname, level=level, \
                submitnum=submitnum, fansnum=fansnum, desc=desc, latest=latest, time=Time.now_timestamp()))
        try:
            html_data_temp=next(html_data_iter)
        except StopIteration as e:
            print('Generrator return value:', e.value)

        return dict_data_list
