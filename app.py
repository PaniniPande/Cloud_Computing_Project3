from math import radians,sin,cos,asin,sqrt
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
import time
import pyodbc
import redis
import hashlib
import pickle
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Panini_driver = '{ODBC Driver 18 for SQL Server}'
Panini_database = 'ADB'
Panini_server = 'tcp:adbassignments15.database.windows.net,1433'
Panini_username = "pxp4144"
Panini_password = "Paridhi@15"
Panini_conn= pyodbc.connect('DRIVER='+Panini_driver+';SERVER='+Panini_server+';DATABASE='+Panini_database+';UID='+Panini_username+';PWD='+ Panini_password)
Panini_cursor = Panini_conn.cursor() 

r = redis.Redis(host='PaniniPande.redis.cache.windows.net',
                port=6379, db=0, password='5WApE6QzgHMvxogCa16VcGuKNallV6AT5AzCaPq1Urk=',ssl=False)

@app.route('/redis', methods=['POST','GET'])
def redismag():
    Panini_mag1=request.form['m1']
    Panini_mag2=request.form['m2']
    n=int(request.form['input'])
    Panini_query="Select  id,time,latitude,longitude,depth,mag,place,magType from data WHERE mag  between '"+Panini_mag1+"' and '"+Panini_mag2+"'"
    Panini_hash = hashlib.sha224(Panini_query.encode('utf-8')).hexdigest()
    Panini_key = "redis_cache:" + Panini_hash
    Panini_t1 = time.time()
    for i in range(1,n):
        if(r.get(Panini_key)):
            pass
        else:
            Panini_cursor.execute(Panini_query)
            data = Panini_cursor.fetchall()
            r.set(Panini_key, pickle.dumps(data))
            r.expire(Panini_key,36)
    Panini_t2 = time.time()
    total=Panini_t2-Panini_t1
    return render_template("display.html",time1 = total,n=n)  

@app.route('/withoutredis', methods=['POST','GET'])
def withoutredis():
    Panini_mag1=request.form['m1']
    Panini_mag2=request.form['m2']
    n=int(request.form['input'])
    Panini_query="Select  id,latitude,longitude,depth,mag,place,magType from data WHERE mag  between '"+Panini_mag1+"' and '"+Panini_mag2+"' "
    Panini_t1 = time.time()
    for i in range(1,n):
            Panini_cursor.execute(Panini_query)
            # data = Panini_cursor.fetchall()
    Panini_t2  = time.time()
    total=Panini_t2 -Panini_t1
    return render_template("display2.html",time2 = total,n=n)               


@app.route('/redis2', methods=['POST','GET'])
def redissimple():
    rows=[]
    n=int(request.form['input'])
    Panini_query="Select id,time,latitude,longitude,depth,mag,place from data"
    Panini_hash = hashlib.sha224(Panini_query.encode('utf-8')).hexdigest()
    Panini_key = "redis_cache:" + Panini_hash
    Panini_t1 = time.time()
    for i in range(1,n):
        if(r.get(Panini_key)):
            pass
        else:
            Panini_cursor.execute(Panini_query)
            rows = Panini_cursor.fetchall()
            r.set(Panini_key, pickle.dumps(rows))
            r.expire(Panini_key,36)
    Panini_t2 = time.time()
    total=Panini_t2-Panini_t1
    return render_template("display3.html",time1 = total, rows =rows, n=n) 

@app.route('/withoutredis2', methods=['POST','GET'])
def without():
    rows=[]
    n=int(request.form['input'])
    Panini_query="Select  id,time,latitude,longitude,depth,mag,place from data "
    Panini_t1 = time.time()
    for i in range(1,n):
            Panini_cursor.execute(Panini_query)
            rows = Panini_cursor.fetchall()
    Panini_t2 = time.time()
    total=Panini_t2-Panini_t1
    return render_template("display4.html",time2 = total, rows=rows, n=n)






# root 
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/task1')
def task1():
   return render_template('task1.html')    

@app.route('/task2')
def task2():
   return render_template('task2.html')   
 
@app.route('/task3')
def task3():
   return render_template('task3.html')   
@app.route('/task4')
def task4():
   return render_template('task4.html')     


if __name__ == '__main__':
    app.run(port=5001)
