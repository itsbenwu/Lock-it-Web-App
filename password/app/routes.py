import os 
import time
from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener
from flask_pymongo import PyMongo

# from flask.ext.session import Session
# app = Flask(__name__)
# Check Configuration section for more details
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)



app.config['MONGO_DBNAME'] = 'database' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:orangemango11@cluster0-hnatc.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")



    
@app.route('/register', methods = ['GET','POST'])
def register():
    return render_template("register.html", username_exists = False, strong_pass = True)
    
@app.route('/newUser', methods = ['GET', 'POST'])
def newUser():
    passwords = mongo.db.passwords
    if request.method == 'GET':
        return redirect('/')
    user_data = request.form
    print(passwords.find({'username':user_data['username'].lower()}))
    
    if len(list(passwords.find({'username':user_data['username'].lower()}))) > 0:
         return render_template('register.html', username_exists = True)
    if not model.check_password(user_data['password']):
        return render_template("register.html", strong_pass = False)
    passwords.insert({"username": user_data['username'].lower(), "password":user_data['password']})
    
    session['username'] = user_data['username'].lower()
    return render_template("user.html", username = session['username'])
    
@app.route('/login')
def login():
    return render_template("login.html", user_not_found = False)
    
@app.route('/User', methods = ['GET', 'POST'])
def user():
    passwords = mongo.db.passwords
    user_data = request.form
    if request.method == 'GET':
        allPassword = list(mongo.db.allPasswords.find({"username":session['username']}))
        return render_template("user.html", events = allPassword, username = session['username'])
    
    password = list(passwords.find({"username":user_data['username'].lower(), "password":user_data['password']}))
    print(password)
    if len(password) == 0:
        return render_template("login.html", user_not_found = True)
    
    session['username'] = user_data['username'].lower()
    allPassword = list(mongo.db.allPasswords.find({"username":session['username']}))
    return render_template("user.html", events = allPassword, username = session['username'])
   
    
# username# # 
    

@app.route('/add', methods = ['GET', 'POST'])
def add():
    return render_template("add.html", strong_pass = 2)
    
@app.route('/adding', methods = ['POST'])
def adding():
    user_data = request.form
    if not model.check_password(user_data['pass_company']):
        return render_template("add.html", strong_pass = 0)
    
    mongo.db.allPasswords.insert({'username': session['username'], 'company' : user_data['company'], 'user_company' : user_data['user_company'], 'pass_company' : user_data['pass_company']})
    
    allPassword = list(mongo.db.allPasswords.find({"username":session['username']}))
    return render_template("add.html", strong_pass = 1)
    
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/deleted', methods = ['POST'])
def deleted():
    user_data = request.form
    print(session['username'])
    print(list(mongo.db.allPasswords.find({'username' : session['username'], 'company' : user_data['deleted_company']})))
    mongo.db.allPasswords.remove({'username' : session['username'], 'company' : user_data['deleted_company'], 'user_company': user_data['user_company']})
    allPassword = list(mongo.db.allPasswords.find({"username":session['username']}))
    return render_template("user.html", events = allPassword, username = session['username'])
    
@app.route('/update')
def update():
    return render_template('update.html', company_not_exist = False, strong_pass = True)
@app.route('/updated',methods=['POST'])
def updated():
    user_data = request.form
    
    
    password = list(mongo.db.allPasswords.find({'company':user_data['company'], 'username':session['username'], 'user_company':user_data['user_company']}))
    if len(password) == 0:
        print("yes")
        return render_template('update.html', company_not_exist = True) 
    if not model.check_password(user_data['pass_company']):
        return render_template("update.html", strong_pass = False)
    print(password)
    mongo.db.allPasswords.update({'pass_company': password[0]['pass_company']},  {'$set':{'pass_company': user_data['pass_company']}})
    
    allPassword = (mongo.db.allPasswords.find({"username":session['username']}))
    return render_template("user.html", events = allPassword, username = session['username'])

@app.route('/checkpassword')
def check_pass():
    user_data = request.form
    if not model.check_password(user_data['pass_company']):
        return render_template("add.html", strong_pass = False)
    return render_template("add.html", strong_pass = True)
    
@app.route('/back')
def back():
    allPassword = (mongo.db.allPasswords.find({"username":session['username']}))
    return render_template("user.html", events = allPassword, username = session['username'])
    
    