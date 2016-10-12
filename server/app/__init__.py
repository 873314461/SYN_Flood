# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yu/tmp/SYN_Flood/server/database.db'
db = SQLAlchemy(app)

from app import views