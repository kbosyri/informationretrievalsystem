from flask import Flask,request
from ranking import CalculateSimilarity,SortResults

app = Flask(__name__)

@app.route('/rank',methods=['GET','POST'])
def RankingServer():
    ranks = CalculateSimilarity(request.json.get('query'), request.json.get('docs'),request.json.get('dataset'))
    results = SortResults(ranks,request.json.get('dataset'))
    response = {"results":results}
    return response