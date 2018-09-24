from flask import render_template, request, jsonify
import flask
import requests
import json
from werkzeug.contrib.fixers import ProxyFix

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

url  =  "https://api.dialogflow.com/v1/query"
headers = {
    "Authorization": "Bearer 61382eb602db42258d37046eafabf841",
    "Content-Type": "application/json"
}


qnas = [
	{
		'id':1,
		'question': u'',
		'answer' : u''
	}
	]


@app.route('/question/',methods=['POST'])
def ans():
	query = request.json['question']
	data  =  {
       		 "query":query,
   		 "sessionId" : 2,
   		 "lang": "hi"
		}
	r = requests.post(url, headers = headers, data = json.dumps(data))
	answer = json.loads(r.content.decode('UTF-8'))['result']['speech']
	qna = {
		'id':qnas[-1]['id'] + 1,
		'question':query,
		'answer':answer
	}
	qnas.append(qna)
	return jsonify({'qna':qna}), 201


@app.route('/',methods=['GET'])
def home():
	return render_template('index.html', variable = {'qnas':qnas})
	#return jsonify({'qnas': qnas})

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run()
