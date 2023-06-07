from flask import Flask,request
from matching import match
import requests

app = Flask(__name__)

@app.route("/match",methods=["GET","POST"])
def matchquery():
    result = match(request.json.get("query"),request.json.get('dataset'))

    response = requests.post('http://localhost:5005/rank'
        ,json={"query":request.json.get("query"),"docs":result,"dataset":request.json.get('dataset')}).json().get('results')
    response = {"results":response}
    return response