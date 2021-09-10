import sys, cv2,csv
import numpy as np
import pandas as pd
import csv,random
from pathlib import Path
from recog import rec
from flask import Blueprint, render_template
from csv import reader
import calendar
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, request, flash
#credentials for admin login
data={'komal':'1234','archana': 'archana@1234','nikita':'1234','kritika':'1234'}


auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/home')
def home():
    return render_template('home.html')



@auth.route('/admin')
def admin():
    return render_template('admin.html')

@auth.route('/admin',methods=['POST'])
def login_post():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in data:
        flash('Username doesn\'t exist')
        return redirect(url_for('auth.admin'))
    else:
        if data[name1]!=pwd:
            flash('Password incorrect')
            return redirect(url_for('auth.admin'))
        else:
            return render_template("adlogin.html")


@auth.route('/recog')
def recog():
    c=rec()
    if c=="Nope":
        flash("Already marked attendance")
        return render_template('home.html')
    else:
        flash("Attendance marked successfully")
        return render_template('home.html',value=c)
    
@auth.route('/attdownload')
def download_att():
    return render_template("download.html")



@auth.route('/att',methods=['POST'])
def att():
    empid=request.form['empid']
    flag=0
    with open('test.csv') as csv_file:
        data=csv.reader(csv_file,delimiter=',')
        first_line = True
        places = []
        for row in data:
            if not first_line:
                if row[0]==empid:
                    flag=1
                    places.append({
                    "e_id": row[0],
                    "date": row[1],
                    "time": row[2],
                    "day": row[3],
                    "leave_t":row[4]
                    })
            else:
                first_line = False
    if flag==0:
        flash('Incorrect Employee-ID.')
        return render_template('download.html')
    else:
        return render_template("tabledesign.html", places=places, value=empid)

@auth.route('/log_out')
def log_out():
    flash('Logged-out successfully')
    return render_template("home.html")

@auth.route('/about')
def about():
    return render_template("about.html")

@auth.route('/ad_view')
def ad_view():
    with open('test.csv') as csv_file:
        data=csv.reader(csv_file,delimiter=',')
        first_line = True
        places = []
        for row in data:
            if not first_line:
                    places.append({
                    "e_id": row[0],
                    "date": row[1],
                    "time": row[2],
                    "day": row[3],
                    "leave_t":row[4]
                    })
            else:
                first_line = False
    return render_template("tabledesign2.html", places=places)

@auth.route('/ad_today')
def ad_today():
    with open('test.csv') as csv_file:
        data=csv.reader(csv_file,delimiter=',')
        first_line = True
        places = []
        today=str(date.today())
        for row in data:
            if not first_line:
                if row[1]==today:
                    places.append({
                    "e_id": row[0],
                    "date": row[1],
                    "time": row[2],
                    "day": row[3],
                    "leave_t":row[4]
                    })
            else:
                first_line = False
    return render_template("tabledesign2.html", places=places)
