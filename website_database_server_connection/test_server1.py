#export FLASK_APP=test_server1.py
#flask run --host 0.0.0.0 --port 5000

import requests
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    user_id_var = 1
    Params = {'user_id' : user_id_var}
    reco = requests.get('http://0.0.0.0:5001/', params = Params)
    data = reco.json()
    list_of_movies = data['recommend']
    return render_template('recommendation.html', movie_list = list_of_movies)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
