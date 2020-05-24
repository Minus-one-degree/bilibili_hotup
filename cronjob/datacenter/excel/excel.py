# -*- coding: utf-8 -*-
import sys
sys.path.append("..") #把上级目录加入到变量中
import json,xlwt
from util.base.time import TimeTranslator, Time

class ExcelController(object):

    def __init__(self):
        self.year, self.month, self.day = Time.now_ymd()
        self.hour, self.minute, self.second = Time.now_hms()
        self.number = self.year + self.month + self.day + self.hour + self.minute + self.second

    def writeExcel(self,new_data):
        a = new_data
        title = ["AV号","标题","时长","播放次数","弹幕数","发布时间","UP名字","采集时间"]
        title_en = ['avnumber','title','length','playtime','subtitle','date','upname','time']
        book = xlwt.Workbook() # 创建一个excel对象
        sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True) # 添加一个sheet页
        for i in range(len(title)): # 循环列
            sheet.write(0,i,title[i]) # 将title数组中的字段写入到0行i列中
        for i in range(len(a)):
            row_a=a[i]
            for j in range(len(title)):
               sheet.write(i+1,j,row_a[title_en[j]])        
        #没有加相对路径
        book.save('F:/2019interval/bilibili_hotup-master/data_excel/'+self.number+'_hotword.xls')
