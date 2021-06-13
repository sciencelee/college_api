#import pandas as pd
from flask import Flask, jsonify, request
import json
import pickle
import scipy.spatial.distance as distance
from collections import Counter
import sys
from flask_cors import CORS, cross_origin



# create app
app = Flask(__name__, static_folder='static')
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app, resources={r"/api/": {"origins": ""}})
#CORS(app)


# load "model" data
import pandas as pd
import json
df_final = pickle.load(open('static/df_final_names.pkl', 'rb'))
df_scaled = pickle.load(open('static/scaled_df.pkl', 'rb'))

#app.logger.warning('testing warning log')


# routes
@app.route('/model/', methods=['POST', 'GET'])
def predict():
    # get data
    data = request.get_json()[0]
    colleges = [data['dream'], data['target'], data['safety'] ]

    closest_list = []
    for i, college in enumerate(colleges):
        college_id = get_index(college)
        test_college = df_scaled.iloc[[college_id]]

        ary = distance.cdist(df_scaled, test_college, metric='minkowski')

        results = df_final.copy() # different results
        results['dist'] = ary
        closest = results.sort_values(by='dist')
        closest = list(closest['INSTNM'][1:4])
        closest_list += closest

    result = top_five(closest_list, colleges)

    output = {}
    output['results'] = []

    for college in result:
        i = get_index(college)
        school = {}
        stats = df_final.iloc[i]
        school = {
                'schoolname': stats['INSTNM'],
                'url': stats['INSTURL'],
                'city': stats['CITY'],
                'state': stats['STABBR'],
                'student_pop': stats['UGDS'],
                #'control': stats['CONTROL'],
                'avg_tuition': stats['COSTT4_A'],
                'admission_rate': stats['ADM_RATE'],
                }

        output['results'].append(school)

    return jsonify(output)


@app.route('/colleges/', methods=['GET'])
def colleges():
    with open('static/colleges.txt') as json_file:
        data = json.load(json_file)
    return data


def top_five(all3, original):
    all3 = [x for x in all3 if x not in original]
    my_counts = sorted([[x, all3.count(x)] for x in set(all3)], key=lambda x: x[1])
    top_five = [x[0] for x in my_counts][:5]
    return top_five

def get_index(college):
    college_id = df_final[df_final['INSTNM'] == college]  # test it out
    college_id = college_id.index.to_list()[0]
    return int(college_id)








# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"

if __name__ == '__main__':
    app.run(debug=True)
