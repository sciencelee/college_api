#import pandas as pd
from flask import Flask, jsonify, request
import pandas as pd
import json

# load model
#model = ????
# dream = data['dream']

# convert data into dataframe
# data.update((x, [y]) for x, y in data.items())
# data_df = pd.DataFrame.from_dict(data)

# predictions
# result = model.predict(data_df)

# send back to browser




app = Flask(__name__)



# routes
@app.route('/model/', methods=['POST', 'GET'])
def predict():
    # get data
    data = request.get_json()[0]
    dream = data['dream']
    target = data['target']
    safety = data['safety']


    results = {'results': data}

    output = [{dream:97, target:80, 'Ohio State':68}]
    print(output)

    return jsonify(output)

@app.route('/colleges/', methods=['POST', 'GET'])
def colleges():
    return json.load('colleges.txt')



# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"

if __name__ == '__main__':
    app.run(debug=True)
