# coding=utf-8
#设置编码为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import app, db
from flask import render_template, flash, redirect, request, url_for
from module import Request as Req
import json

@app.route('/')
@app.route('/index')
def index():
	return 'Hello world!'

@app.route('/query')
def query():
	page = request.args.get('page')
	if page is None:
		page = 1
	else:
		page = int(page)
	requests = Req.query.order_by(db.desc('time')).offset((page-1)*30).limit(30).all()
	rest = []
	for req in requests:
		temp = {
			"id":str(req.ID),
			"src_mac":str(req.src_mac),
			"dst_mac":str(req.dst_mac),
			"src_ip":str(req.src_ip),
			"dst_ip":str(req.dst_ip),
			"is_syn":False if req.is_syn == 0 else True,
			"prot_ip":str(req.prot_ip),
			"time":str(req.time)
		}
		rest.append(temp)
	return json.dumps(rest), 200, {"Access-Control-Allow-Origin": "http://localhost:3000"}