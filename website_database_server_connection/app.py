import requests
import pandas as pd
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///website_users.db', echo=True)
 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 
sessions = []
@app.route('/rating', methods=['GET', 'POST'])
def rating():
    filename = "/home/kainaat/Documents/PEC/Sem5/Minor_Project_on_github_repo/Minor-Project/ml-latest-small/moviesnew.csv"
    x = pd.read_csv(filename) 
    return render_template('star.html', name=filename, data=x.to_html())  


@app.route('/', methods=['GET', 'POST'])
def home():
    #return render_template('main2.html')
    return render_template('homepage.html')  

@app.route('/for_login', methods=['GET', 'POST'])
def home_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('cinephile.html')

@app.route('/redirect_for_signup', methods=['GET'])
def redirect_user():
    return render_template('signup.html')

@app.route('/recommendations', methods=['GET'])
def recommend():
    user_name = session['user_name']
    Session = sessionmaker(bind=engine)
    s = Session()
    user_name_query = s.query(User).filter(User.username.in_([user_name]))
    result = user_name_query.first()
    user_id_var = result.id
    url = 'http://127.0.0.1:9000/'
    url = url + str(user_id_var) + '/ratings/top/10'
    reco = requests.get(url)
    data = reco.json()
    list_of_movies = data
    return render_template('recommendation.html', movie_list = list_of_movies)

@app.route('/redirect_for_signup', methods=['POST'])
def register_user():
    #print("POST called")
    #return "hello from post"
    
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()
    if result:
        flash('User already exists')
        return home()
    else:
        user = User(POST_USERNAME, POST_PASSWORD)
        s.add(user)
        s.commit()
        return home() 

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    session['user_name'] = POST_USERNAME
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home_page()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home_page()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)

