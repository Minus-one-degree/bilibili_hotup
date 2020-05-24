# -*- coding: utf-8 -*-
# Cronjob for Weibo's hotkey upload system.
# tongxinCode Test to Excel 20190721
# tongxinCode Test to sqlite 20190723
# new bilibili cronjob

from cronjob.crawler.hotkey_fetcher import HotkeyFetcher
#from cronjob.datacenter.excel.excel import ExcelController
from cronjob.datacenter.sqlite.sqlite import SQLiteController
from util.constant.enum import *
from util.base.time import Time


#根据关键字建表爬取数据-非模板化
def initcrawlkeyword(table):#table注意使用sqlite规范的表名
    # sqlite win10下运行正常
    sqlbox = SQLiteController()
    sqlbox.createTable(table)

#根据关键字爬取数据-非模板化
def crawlkeyword(table, keyword):
    # sqlite win10下运行正常
    sqlbox = SQLiteController()
    #i代表访问的页数，当实际页数小于50时会报错
    for i in range(1,51):
        print("[+]This is the "+str(i)+" page![=====]None==1page_end")
        fetcher = HotkeyFetcher(keyword=keyword,page_number=i,order_number=0,parse_func=0)
        data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=0)
        #excel win10下运行正常
        # 反复写入不合适，使用sqlite最后统一写入
        # excelbox = ExcelController()
        # excelbox.writeExcel(data)
        sqlbox.insertSQL(table,data)

#根据UP名字爬取用户的相关数据-非模板化
def initcrawupname(table):
    sqlbox = SQLiteController()
    sqlbox.createTable2(table)   

#根据UP名字爬取用户的相关数据-非模板化
def crawlupname(table, keyword):
    # sqlite win10下运行正常
    sqlbox = SQLiteController()
    fetcher = HotkeyFetcher(page_number=1,order_number=0,keyword=keyword,parse_func=1)
    data = fetcher.get_data(ENUM_DATATYPE_JSON, limit=0)
    sqlbox.insertSQL2(table,data)

def collect_wow_landscape():
    sqlbox = SQLiteController()
    initcrawlkeyword("WOW_landscape")
    crawlkeyword("WOW_landscape","魔兽世界 风景")
    initcrawupname("UP_landscape")
    upname_list=sqlbox.selectSQL_upname("WOW_landscape")
    for upname in upname_list:
        crawlupname("UP_landscape",upname[0])
    
def collect_hearthstone():
    sqlbox = SQLiteController()
    initcrawlkeyword("hearthstone")
    crawlkeyword("hearthstone","炉石传说")
    initcrawupname("UP_hearthstone")
    upname_list=sqlbox.selectSQL_upname("hearthstone")
    for upname in upname_list:
        crawlupname("UP_hearthstone",upname[0])

if __name__ == "__main__":
    # sqlbox.clearSQL("WOW")
    # sqlbox.clearSQL("UP")
    # # initcrawlkeyword("WOW")
    # crawlkeyword("WOW","魔兽世界")
    # crawlkeyword("WOW","WOW")
    # crawlkeyword("WOW","魔兽")
    collect_hearthstone()
    '''
    进行数据采集分析分离
    '''