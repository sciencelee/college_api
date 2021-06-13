#import pandas as pd
from flask import Flask, jsonify, request
import json

app = Flask(__name__, static_folder='static')


# routes
@app.route('/model/', methods=['POST', 'GET'])
def predict():
    # get data
    data = request.get_json()[0]
    dream = data['dream']
    target = data['target']
    safety = data['safety']


    results = {'results': data}

    output = [{dream:97, target:80, 'Ohio State University':68}]
    print(output)

    return jsonify(output)

@app.route('/colleges/', methods=['GET'])
def colleges():
    with open('static/colleges.txt') as json_file:
        data = json.load(json_file)
    return data



# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"

if __name__ == '__main__':
    app.run(debug=True)
