from flask import Flask,request,render_template
import requests
import ir_datasets
import json
from pathlib import Path

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
        
def Calculate_Recall(query):
    relevants = 0
    caught = 0
    recalls = []
    for result in query['results']:
        if result['relevance'] != None:
            relevants = relevants + 1
        
    for result in query['results']:
        if result['relevance'] != None:
            caught = caught + 1

        if relevants == 0:
            recalls.append(0.0)

        else:
            recalls.append(caught/relevants)

    return recalls

def Calculate_Reciprocal(query):
    position = 1
    for result in query['results']:
        if result['relevance'] != None:
            break

        position = position + 1

    return 1/position

def Calculate_MRR(result,count):
    reciprocals = 0

    for query in result['queries']:
        reciprocals = reciprocals + query['reciprocal']

    return reciprocals/count

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

def average_precision(result,count):
    precisions = 0
    for query in result['queries']:
        precisions = precisions + query['precision@10']

    return precisions/count

def average_recalls(result,count):
    recalls = 0
    for query in result['queries']:
        recalls = recalls + query['recall@10']

    return recalls/count

@app.route("/",methods=["GET","POST"])
def Serve():
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
            final['recalls'] = Calculate_Recall(final)
            final['reciprocal'] = Calculate_Reciprocal(final)
            print("Len P:")
            print(len(final['precisions']))
            print("Len R:")
            print(len(final['recalls']))
            if len(final['precisions']) >= 10:
                final['precision@10'] = final['precisions'][9]
            elif len(final['precisions']) == 0:
                final['precision@10'] = 0.0
            else:
                final['precision@10'] = final['precisions'][len(final['precisions'])-1]

            if len(final['recalls']) >= 10:
                final['recall@10'] = final['recalls'][9]
            elif len(final['recalls']) == 0:
                final['recall@10'] = 0.0
            else:
                final['recall@10'] = final['recalls'][len(final['recalls'])-1]

            final['AP'] = Calculate_AP(final)
            
            results['queries'].append(final)
        
        results['MAP'] = Calculate_MAP(results, count)
        results['MRR'] = Calculate_MRR(results, count)
        results['ap@10'] = average_precision(results, count)
        results['ar@10'] = average_recalls(results, count)

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

