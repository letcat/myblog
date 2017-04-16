import sqlite3
import os
import time


class DbHandle():

    def __init__(self,databaseUri):

        self.conn = sqlite3.connect(databaseUri)
        self.cur = self.conn.cursor()
        
    def execute(self,sql,param=()):

        return self.cur.execute(sql,param)
    
    def getData(self,sql,param=()):

        data = self.execute(sql,param).fetchall()
        #self.close()
        return data

    def getPageCount(self,tableName,pageSize=5):

        values = self.getData("select count(*) from "+str(tableName))
        counts = values[0][0]
        if(counts%pageSize) == 0:
            pageCount = counts/pageSize
        else:
            pageCount = counts/pageSize+1
        return pageCount

    def getPageData(self,tableName,pageNum,pageSize=5):

        sql = "select * from "+tableName+" order by date desc limit ?,?"
        pageCount = self.getPageCount(tableName, pageSize)
        if pageNum > pageCount:
            pageNum = pageCount
        param = ((pageNum -1)* pageSize, pageSize)
        return self.getData(sql, param)

    def close(self):

        self.cur.close()
        self.conn.commit()
        self.conn.close()


class Blog():

    def __init__(self,databaseUri):

        self.databaseUri = databaseUri
        self.db = DbHandle(self.databaseUri)

    def addBlog(self,title,summary,label,text):

        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = "insert into blogs (title,summary,label,text,date) values (?,?,?,?,?)"
        param = (title,summary,label,text,datetime)
        self.db.execute(sql,param)
        self.db.close()

    def getBlog(self,id):

        sql = "select * from blogs where id = ?"
        param = (id,)
        blog = self.db.getData(sql,param)
        self.db.close()
        return blog

    def listBlogs(self,pageNum,blogsNum):
        blogs = self.db.getPageData("blogs",pageNum,blogsNum)
        self.db.close()
        return blogs

    def editBlog(self,id,title,summary,label,text):

        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = "update blogs set title = ?,summary = ?,label = ?,text = ?,date =? where id =?"
        param = (title,summary,label,text,datetime,id)
        self.db.execute(sql,param)
        self.db.close()

    def delBlog(self,id):

        sql = "delete from blogs where id =?"
        param = (id,)
        self.db.execute(sql,param)
        self.db.close()

    def findBlog(self, info):

        sql = "select * from blogs where text like '%"+info+"%' or title like '%"+info+"%'"
        blogs = self.db.getData(sql)
        return blogs


if __name__ == '__main__':

    basedir = os.path.abspath(os.path.dirname(__file__))
    #DATABASE_URI = os.path.join(basedir, 'blogs.db')
    #creat_sql = "create table result( id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(20),t1 varchar(20),t2 varchar(20),t3 varchar(20),t4 varchar(20),t5 varchar(20),date datetime)"

    #list = db.execute(blog_sql,())
    #print list
    '''
    dorp_sql = "drop table if exists blogs"
    blog_sql = "create table blogs ( id integer primary key autoincrement,title string not null,summary string not null,label string,text string not null,date datetime)"
    select_sql = "select * from blogs"
    db = DbHandle(os.path.join(basedir, 'blogs.db'))
    db.execute(blog_sql)
    #print db.getData(select_sql)[0]
    db.close()
    '''
    uri = os.path.join(basedir, 'blogs.db')
    b = Blog(uri)

    #b.addBlog()
    #b.editBlog(1,'test','cats','zoo','hello world')
    #b.delBlog(6)
    #blog = b.getBlog(3)
    print b.listBlogs(1,3)