from flask import Flask,render_template,request,redirect,url_for
from public import public
from admin import admin 
from staff import staff
from users import users
from api import api

app=Flask(__name__)
app.secret_key="AG"

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(staff,url_prefix='/staff')
app.register_blueprint(users,url_prefix='/users')
app.register_blueprint(api,url_prefix='/api') 

app.run(debug=True,port=5030)   