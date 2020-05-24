# -*- coding: utf-8 -*-

import sqlite3

class SQLiteController(object):

    def __init__(self):
        pass

    def clearSQL(self,table):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("delete from "+table)
        cursor = c.execute("update sqlite_sequence SET seq = 0 where name = '"+table+"'")
        print ("Operation done successfully")
        conn.commit()
        conn.close()
    #创建默认hotup表
    def createTable(self,table):
        conn = sqlite3.connect('test_bilibili.db')
        print ("Opened database successfully")
        c = conn.cursor()
        c.execute("CREATE TABLE "+table+"\
            (id integer primary key autoincrement,\
            avnumber       CHAR(50)  NOT NULL,\
            title         CHAR(50)   NOT NULL,\
            length       DATE        NOT NULL,\
            playtime        INT,\
            subtitle      INT,\
            date          DATE       NOT NULL,\
            upname      CHAR(50)     NOT NULL,\
            time         DOUBLE     NOT NULL);")
        print ("Table created successfully")
        conn.commit()
        conn.close()
    # 创建up信息表
    def createTable2(self,table):
        conn = sqlite3.connect('test_bilibili.db')
        print ("Opened database successfully")
        c = conn.cursor()
        c.execute("CREATE TABLE "+table+"\
            (id integer primary key autoincrement,\
            spaceid       int         NOT NULL,\
            upname         CHAR(50)   NOT NULL,\
            level          int        NOT NULL,\
            submitnum        INT,\
            fansnum        int,\
            desc          char(120),\
            latest        char(1024),\
            time         DOUBLE     NOT NULL);")
        print ("Table created successfully")
        conn.commit()
        conn.close()
    #默认表    
    def insertSQL(self,new_data):
        a = new_data
        title = ["AV号","标题","时长","播放次数","弹幕数","发布时间","UP名字","采集时间"]
        title_en = ['avnumber','title','length','playtime','subtitle','date','upname','time']
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        print ("Opened database successfully")
        for i in range(len(a)):
            row_a=a[i]
            temp_insert=[]
            for j in range(len(row_a)):
                #@tx检验通过
                # print(row_a[title_en[j]])
                # print(type(row_a[title_en[j]]))
                if type(row_a[title_en[j]])==str:
                    temp_insert.append(row_a[title_en[j]])
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])!=0:
                    temp_insert.append(row_a[title_en[j]][0])
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])==0:
                    temp_insert.append(' ')
                elif type(row_a[title_en[j]])==int:
                    temp_insert.append(row_a[title_en[j]])
            c.execute("INSERT INTO HOTUP (avnumber,title,length,playtime,subtitle,date,upname,time) \
                        VALUES (?,?,?,?,?,?,?,?)",temp_insert)    
        #select操作@cursorprint结果为<sqlite3.Cursor object at 0x000001ADA7F47500>
        # cursor = c.execute("SELECT *  from HOTWORD")  
        # print(cursor)  
        # print ("Operation done successfully")
        conn.commit()
        print ("Records created successfully")
        conn.close()

    #特定表    
    def insertSQL(self,table,new_data):
        a = new_data
        title = ["AV号","标题","时长","播放次数","弹幕数","发布时间","UP名字","采集时间"]
        title_en = ['avnumber','title','length','playtime','subtitle','date','upname','time']
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        print ("Opened database successfully")
        for i in range(len(a)):
            row_a=a[i]
            temp_insert=[]
            for j in range(len(row_a)):
                #@tx检验通过
                # print(row_a[title_en[j]])
                # print(type(row_a[title_en[j]]))
                if type(row_a[title_en[j]])==str:
                    temp=row_a[title_en[j]]
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])!=0:
                    temp=row_a[title_en[j]][0]
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])==0:
                    temp=' '
                elif type(row_a[title_en[j]])==int:
                    temp=row_a[title_en[j]]
                if j in range(3,5):
                    if str(temp).find("万") != -1:
                        temp=int(float(temp.split("万",1)[0])*10000)
                temp_insert.append(temp)
            c.execute("INSERT INTO "+table+" (avnumber,title,length,playtime,subtitle,date,upname,time) \
                        VALUES (?,?,?,?,?,?,?,?)",temp_insert)    
        #select操作@cursorprint结果为<sqlite3.Cursor object at 0x000001ADA7F47500>
        # cursor = c.execute("SELECT *  from HOTWORD")  
        # print(cursor)  
        # print ("Operation done successfully")
        conn.commit()
        print ("Records created successfully")
        conn.close()

    #特定表upname   
    def insertSQL2(self,table,new_data):
        a = new_data
        title_en = ['spaceid','upname','level','submitnum','fansnum','desc','latest','time']
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        print ("Opened database successfully")
        for i in range(len(a)):
            if i >0:#去掉搜索到的其他up
                break
            row_a=a[i]
            temp_insert=[]
            for j in range(len(row_a)):
                #@tx检验通过
                # print(row_a[title_en[j]])
                # print(type(row_a[title_en[j]]))
                if type(row_a[title_en[j]])==str:
                    temp=row_a[title_en[j]]
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])==1\
                    and type(row_a[title_en[j]][0])!=tuple:
                    temp=row_a[title_en[j]][0]
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])==1\
                    and type(row_a[title_en[j]][0])==tuple:
                    temp=str(row_a[title_en[j]][0])
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])>1:
                    temp=str(row_a[title_en[j]])
                elif type(row_a[title_en[j]])==list and len(row_a[title_en[j]])==0:
                    temp=' '
                elif type(row_a[title_en[j]])==int:
                    temp=row_a[title_en[j]]
                if j in range(3,5):
                    if str(temp).find("万") != -1:
                        temp=int(float(temp.split("万",1)[0])*10000)
                temp_insert.append(temp)
            c.execute("INSERT INTO "+table+" (spaceid,upname,level,submitnum,fansnum,desc,latest,time) \
                        VALUES (?,?,?,?,?,?,?,?)",temp_insert)    
        conn.commit()
        print ("[]~(￣▽￣)~*一个UP成功入水！！！")
        print ("Records created successfully")
        conn.close()

    def selectSQLALL(self, table):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("SELECT *  from "+table)  
        values = cursor.fetchall()
        print(values) 
        print ("Operation done successfully")
        conn.commit()
        conn.close()

    def selectSQL1(self):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("SELECT upname,playtime,subtitle,date  from WOW")  
        values = cursor.fetchall()
        conn.commit()
        conn.close()
        return values

    def selectSQL_upname(self, table):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("SELECT upname  from "+table)  
        values = cursor.fetchall()
        upname=[]
        for line_data in values:
            if line_data in upname:
                pass
            else:
                upname.append(line_data)
        conn.commit()
        conn.close()
        return upname

    def showtableinfo(self,name):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("PRAGMA table_info("+name+")")
        print(cursor.fetchall())
        conn.commit()
        conn.close()

    def showSTATISTIC(self,name):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("select * from "+name)
        values=cursor.fetchall()
        print("[+]该表共有行数："+str(len(values)))
        conn.commit()
        conn.close()
        return values

    def showSTATISTIC_sort(self,name):
        conn = sqlite3.connect('test_bilibili.db')
        c = conn.cursor()
        cursor = c.execute("select * from "+name+" order by fansnum")
        values=cursor.fetchall()
        print("[+]该表共有行数："+str(len(values)))
        conn.commit()
        conn.close()
        return values
