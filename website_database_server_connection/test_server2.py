#export FLASK_APP=test_server2.py
#flask run --host 0.0.0.0 --port 5000

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    recommendation = [["Argo (2012)", 5.367495246894928, 28], ["\"Shawshank Redemption", 5.251700803345418, 317]]
    return jsonify({"recommend" : recommendation})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
