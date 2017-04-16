from flask import Flask,render_template,jsonify,request,redirect
import sqlite3,time
from db import DbHandle,Blog


app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page=1):
    blogsNum2Show = 5
    blog = Blog(app.config.get('DATABASE_URI'))
    blogs = blog.listBlogs(page,blogsNum2Show)
    return render_template('index.html',blogs=blogs,page=page)

@app.route('/time.html')
def time():
    return render_template('time.html')

@app.route('/save',methods = ['post'])
def save():

    datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    form = request.form
    sql = "insert into result (name,t1,t2,t3,t4,t5,date) values ('spy',?,?,?,?,?,?)"
    record = (form['time1'],form['time2'],form['time3'],form['time4'],form['time5'],datetime)
    db = DbHandle(app.config.get('DATABASE_URI'))
    db.execute(sql,record)
    db.close()
    return ''
'''
@app.route('/view',methods = ['post'])
def viewResult():

    db_Addr = app.config.get('DATABASE_URI')
    db = DbHandle(db_Addr)
    sql = "select * from result order by id desc limit ?,?"
    pageNow = int(request.form['pageNow'])
    pageSize = 5
    pageCount = db.getPageCount("select count(*) from result",pageSize)
    if pageNow > pageCount:
        pageNow = pageCount   
    param = (pageNow*pageSize,pageSize)

    values = db.getData(sql,param)
    return jsonify({'result':values})
'''
@app.route('/addBlog.html')
def addBlog():

    return render_template('addBlog.html')

@app.route('/saveBlog',methods = ['post'])
def saveBlog():

    form = request.form
    b = Blog(app.config.get('DATABASE_URI'))
    b.addBlog(form['title'],form['summary'],'test',form['content'])
    blogs = b.listBlogs()
    return render_template('index.html',blogs=blogs)

@app.route('/viewBlog/<id>')
def viewBlog(id):

    #print id
    b = Blog(app.config.get('DATABASE_URI'))
    blog = b.getBlog(int(id))
    return render_template('viewBlog.html',blog=blog,id=id)

@app.route('/search',methods = ['post'])
def search():
    form = request.form
    b = Blog(app.config.get('DATABASE_URI'))
    blogs = b.findBlog(form['search'])
    return render_template('index.html',blogs=blogs)




if __name__ == '__main__':

    app.run()

    '''
    dorp_sql = "drop table if exists blogs"
    blog_sql = "create table blogs ( id integer primary key autoincrement,title string not null,summary string not null,text string not null,date datetime)"

    select_sql = "select * from blogs"
    db = DbHandle(app.config.get('DATABASE_URI'))
    #db.execute(blog_sql)
    print db.getData(select_sql)[0]
    #db.close()
   '''
