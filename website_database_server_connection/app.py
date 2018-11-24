import requests
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///website_users.db', echo=True)
 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user_id_var = 1
        Params = {'user_id' : user_id_var}
        reco = requests.get('http://0.0.0.0:5001/', params = Params)
        data = reco.json()
        list_of_movies = data['recommend']
        return render_template('recommendation.html', movie_list = list_of_movies)

@app.route('/signup', methods=['POST'])
def register_user():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)

