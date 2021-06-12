#import pandas as pd
from flask import Flask, jsonify, request

# load model
#model = ????

app = Flask(__name__)

# routes
@app.route('/model/', methods=['POST', 'GET'])
def predict():
    # get data
    data = request.get_json()
    dream = data['dream']

    # convert data into dataframe
    # data.update((x, [y]) for x, y in data.items())
    # data_df = pd.DataFrame.from_dict(data)

    # predictions
    # result = model.predict(data_df)

    # send back to browser
    output = {'results': data, 'dream':dream}

    return jsonify(output)
    #return jsonify({'University of Michigan':90, 'University of Illinois':80, 'DePaul University': 70})

# def add_message(uuid):
#     content = request.json
#     print content['mytext']
#     return jsonify({"uuid":uuid})


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"

if __name__ == '__main__':
    app.run(debug=True)
