from flask import Flask,request,render_template
import requests
import ir_datasets
import json
from pathlib import Path

queries = {}
dataset = ir_datasets.load('antique/train')

for query in dataset.queries_iter():
    queries[query.query_id] = query.text

app = Flask(__name__)

def Calculate_Precisions(query):
    relevants = 0
    position = 1
    precisions = []
    for result in query['results']:
        print(result['relevance'])
        if result['relevance'] != None:
            relevants = relevants + 1

        precisions.append(relevants/position)
        position = position + 1

    return precisions
        

def Calculate_AP(query):
    relevants = 0
    precision = 0
    index = 0

    for result in query['results']:
        if result['relevance'] != None:
            relevants = relevants + 1
            precision = precision + query['precisions'][index]

        index = index + 1

    if relevants == 0:
        return 0
    
    return precision/relevants


def Calculate_MAP(result,count):
    APs = 0

    for query in result['queries']:
        APs = APs + query['AP']

    return APs/count

@app.route("/",methods=["GET","POST"])
def helloworld():
    if request.method == "GET":
        return render_template("temp.html")

    elif request.method == "POST":
        print(request.form.get('dataset'))
        response = requests.post("http://localhost:5003/query",json={"input":request.form.get("input"),'dataset':request.form.get('dataset')})

        result = requests.post("http://localhost:5004/match",json={'query':response.json().get('query'),'dataset':request.form.get('dataset')})

        #result = requests.post("http://localhost:5006/evaluate",json={'result':result.json().get('results')})

        return render_template("temp.html",results=result.json().get('results'),query=request.form.get("input"),count=len(result.json().get('results')))

@app.route('/evaluate/<dataset_value>',methods=["GET"])
def Evalute(dataset_value):
    results = {"queries":[]}
    count = 0
    dataset = {}
    if dataset_value == "1":
        dataset = ir_datasets.load('antique/train')
        check = Path("eval.json")
    else:
        dataset = ir_datasets.load('wikir/en1k/training')
        check = Path("eval2.json")

    if not check.is_file():

        for query in dataset.queries_iter():
            if count == 50:
                break

            count = count + 1
            print("Count: "+str(count))
            temp = requests.post("http://localhost:5003/query",json={"input":query.text,'dataset':dataset_value})

            temp = requests.post("http://localhost:5004/match",json={'query':temp.json().get('query'),'dataset':dataset_value})
            temp = requests.post("http://localhost:5006/evaluate",json={'result':temp.json().get('results')
                                                                ,'query':{'id':query.query_id,'text':query.text
                                                                },'dataset':dataset_value})

            final = {}
            final['results'] = temp.json().get('results')
            final['query'] = query.text
            final['query_id'] = query.query_id
            final['count'] = len(temp.json().get('results'))
            final['precisions'] = Calculate_Precisions(final)
            final['AP'] = Calculate_AP(final)
            results['queries'].append(final)
        
        results['MAP'] = Calculate_MAP(results, count)

        if dataset_value == "1":
            with open("eval.json",'w') as eval:
                json.dump(results, eval)
        else:
            with open("eval2.json",'w') as eval:
                json.dump(results, eval)

    else:
        
        if dataset_value == "1":
            print("eval.json Exists")
            with open("eval.json",'r') as eval:
                results = json.load(eval)
        
        else:
            print("eval2.json Exists")
            with open("eval2.json",'r') as eval:
                results = json.load(eval)
        

    return render_template("eval.html",results = results)

