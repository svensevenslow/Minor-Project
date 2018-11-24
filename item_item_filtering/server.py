from flask import Flask, render_template
from subprocess import call
import subprocess
import item_item

app = Flask(__name__)

@app.route("/")
def recommend():
    movie, recos = item_item.recommender()
    print(recos)
    return render_template('recommendation.html', movie=movie, recos=recos)

    
