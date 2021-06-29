#import pandas as pd
from flask import Flask, jsonify, request, make_response
import json
import pickle
import scipy.spatial.distance as distance
import json
import flask_cors

# create app
app = Flask(__name__, static_folder='static')
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
#cors = flask_cors.CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


# load "model" data
df_final = pickle.load(open('static/df_final_names.pkl', 'rb'))
df_scaled = pickle.load(open('static/scaled_df.pkl', 'rb'))


# routes
@app.route('/model/', methods=['POST', 'OPTIONS'])
@flask_cors.cross_origin()
def predict():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    # get data
    data = request.get_json()[0]
    colleges = [data['dream'], data['target'], data['safety'] ]

    tops = []
    closest_list = []


    for i, college in enumerate(colleges):
        college_id = get_index(college)
        test_college = df_scaled.iloc[[college_id]]

        ary = distance.cdist(df_scaled, test_college, metric='minkowski')

        results = df_final.copy() # different results
        results['dist'] = ary
        closest = results.sort_values(by='dist')
        closest = list(closest['INSTNM'][1:5])
        closest_list += closest
        tops += closest[:2]

    tops = [x for x in tops if x not in colleges]
    result = dupes(closest_list, colleges)
    tops = [x for x in tops if x not in result]
    result = result + tops  # duplicates first, then top results starting with dream school
    result = result[:5]

    output = {}
    output['results'] = []

    for college in result:
        i = get_index(college)
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
                #'percent_match': results[results['INSTNM']==college]['dist']
                }

        output['results'].append(school)

    return corsify_response(jsonify(output))


@app.route('/colleges/', methods=['GET'])
def colleges():
    with open('static/colleges.txt') as json_file:
        data = json.load(json_file)
    return data


def dupes(all3, original):
    all3 = [x for x in all3 if x not in original]
    my_counts = sorted([[x, all3.count(x)] for x in set(all3)], key=lambda x: x[1])
    dupes = [x[0] for x in my_counts if x[1]>1]
    return dupes

def get_index(college):
    college_id = df_final[df_final['INSTNM'] == college]  # test it out
    college_id = college_id.index.to_list()[0]
    return int(college_id)

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"

if __name__ == '__main__':
    app.run(debug=True)
