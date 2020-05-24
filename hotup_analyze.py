# -*- coding: utf-8 -*-
# tongxinCode for bilibili hot-up's analysis
# create time 20190731

import operator
import csv,codecs
import random

from example.commons import Collector, Faker
from pyecharts import options as opts
from pyecharts.charts import Bar3D, Page, Bar, WordCloud

from cronjob.datacenter.sqlite.sqlite import SQLiteController

C = Collector()


def data_write_csv(file_name, datas):#file_name为写入CSV文件的路径，datas为要写入数据列表
    file_csv = codecs.open(file_name,'w','utf-8')
    writer = csv.writer(file_csv, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['name','type','value','date'])
    upcount={}
    for data in datas:
        data_list=list(data)
        if data_list[0] in upcount:
            upcount[data_list[0]]=upcount[data_list[0]]+1
        else:
            upcount[data_list[0]]=1
        data_list[2]=upcount[data_list[0]]
        writer.writerow(data_list)
    print("保存文件成功，处理结束")

def sort_upcount(data):  
    line_number=0
    upcount={}
    for line_data in data:
        line_number=line_number+1
        if line_data[7] in upcount:
            upcount[line_data[7]]=upcount[line_data[7]]+1
        else:
            upcount[line_data[7]]=1
    sorted_upcount=sorted(upcount.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_upcount) 
   
def bar_plot(datas):
    line_number=0
    upcount={}
    xaxis_attr=[]
    yaxis_var1=[]
    yaxis_var2=[]
    yaxis_var3=[]
    for data in datas:
        data_list=list(data)
        line_number=line_number+1
        if data[7] in upcount:
            upcount[data[7]]=upcount[data[7]]+1
        else:
            upcount[data[7]]=1
        if line_number>1000:#一个关键词最多50页
            break
    sorted_upcount=sorted(upcount.items(), key=operator.itemgetter(1), reverse=True)
    line_number=0
    for sorted_item in sorted_upcount:        
        line_number=line_number+1
        xaxis_attr.append(sorted_item[0])
        yaxis_var3.append(sorted_item[1])
        if line_number >100:
            break
    c = (
        Bar(init_opts=opts.InitOpts(width="1300px", height="580px"))
        .add_xaxis(xaxis_attr)
        # .add_yaxis("播放量", yaxis_var1)
        # .add_yaxis("弹幕数", yaxis_var2)
        .add_yaxis("UP稿件数", yaxis_var3)
        .set_global_opts(title_opts=opts.TitleOpts(title="B站搜索UP统计", subtitle="综合搜索"),\
            datazoom_opts=[opts.DataZoomOpts(type_="slider",)],\
                toolbox_opts = opts.ToolboxOpts(is_show = True),\
                    visualmap_opts = opts.VisualMapOpts(is_show= True, max_=15))
    )
    c.render()
    return sorted_upcount

def bar_plot2(sorted_dic,datas):
    xaxis_attr=[]
    yaxis_var1=[]
    yaxis_var2=[]
    yaxis_var3=[]
    for data in datas:
        data_list=list(data)
        xaxis_attr.append(data_list[2])
        yaxis_var1.append(data_list[3])
        yaxis_var2.append(data_list[4])
        yaxis_var3.append(data_list[5])
    c = (
        Bar(init_opts=opts.InitOpts(width="1300px", height="580px"))
        .add_xaxis(xaxis_attr)
        .add_yaxis("UP等级", yaxis_var1)
        .add_yaxis("UP总稿件数", yaxis_var2)
        .add_yaxis("UP粉丝数", yaxis_var3)
        .set_global_opts(title_opts=opts.TitleOpts(title="B站搜索UP统计", subtitle="综合搜索"),\
            datazoom_opts=[opts.DataZoomOpts(type_="slider",)],\
                toolbox_opts = opts.ToolboxOpts(is_show = True))
    )
    c.render()   

def cloud_plot(datas):
    line_number=0
    upcount={}
    xaxis_attr=[]
    yaxis_var1=[]
    yaxis_var2=[]
    yaxis_var3=[]
    for data in datas:
        data_list=list(data)
        line_number=line_number+1
        if data[7] in upcount:
            upcount[data[7]]=upcount[data[7]]+1
        else:
            upcount[data[7]]=1
        if line_number>1000:
            break
    sorted_upcount=sorted(upcount.items(), key=operator.itemgetter(1), reverse=True)
    line_number=0
    for sorted_item in sorted_upcount:        
        line_number=line_number+1
        xaxis_attr.append(sorted_item[0])
        yaxis_var3.append(sorted_item[1])
        if line_number >100:
            break   
    c = (
        WordCloud(init_opts=opts.InitOpts(width="1300px", height="600px"))
        .add("", sorted_upcount, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"),\
                toolbox_opts = opts.ToolboxOpts(is_show = True))
    )
    c.render()

def cloud_plot2(sorted_dic,datas):
    dic_fans={}
    for data in datas:
        data_list=list(data)
        if data_list[5]<1000:
            continue
        dic_fans[data_list[2]]=data_list[5]
    sorted_dic=sorted(dic_fans.items(), key=operator.itemgetter(1), reverse=True)
    c = (
        WordCloud(init_opts=opts.InitOpts(width="1300px", height="600px"))
        .add("", sorted_dic, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"),\
                toolbox_opts = opts.ToolboxOpts(is_show = True))
    )
    c.render()

@C.funcs
def bar3d_base() -> Bar3D:
    data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
    c = (
        Bar3D()
        .add(
            "",
            [[d[1], d[0], d[2]] for d in data],
            xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="category"),
            yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="category"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=20),
            title_opts=opts.TitleOpts(title="Bar3D-基本示例"),
        )
    )
    return c

def test_example():
    #调用sqlite数据
    # sqlbox = SQLiteController()
    # sqlbox.showtableinfo("WOW")
    # data=sqlbox.showSTATISTIC("WOW")

    # 打印出up在搜索中的计数
    # sort_upcount(data)
    
    # pyecharts bar图绘制
    # bar_plot(data)
    
    # pyecharts wordcloud图绘制
    # cloud_plot(data)

    # 本用于用Janchie的d3做可视化不太好
    # data1=sqlbox.selectSQL1()
    # #csv存储
    # file_name='./data_csv/wow.csv'
    # data_write_csv(file_name,data1)

    #pyecharts的3D bar图实例
    #Page().add(*[fn() for fn, _ in C.charts]).render()
    pass

def test_wow_landscape():
    sqlbox = SQLiteController()
    data=sqlbox.showSTATISTIC("WOW_landscape")
    sorted_dic=bar_plot(data)
    data2=sqlbox.showSTATISTIC_sort("UP_landscape")
    bar_plot2(sorted_dic,data2)
    #cloud_plot2(sorted_dic,data2)


def test_hearthstone():
    sqlbox = SQLiteController()
    data=sqlbox.showSTATISTIC("hearthstone")
    sorted_dic=bar_plot(data)
    data2=sqlbox.showSTATISTIC_sort("UP_hearthstone")
    bar_plot2(sorted_dic,data2)
    #cloud_plot2(sorted_dic,data2)


'''title_en = ['id','avnumber','title','length','playtime','subtitle','date','upname','time']'''
'''title_en2 = ['id','spaceid','upname','level','submitnum','fansnum','desc','latest','time']'''
if __name__ == "__main__":
    test_hearthstone()
           

        