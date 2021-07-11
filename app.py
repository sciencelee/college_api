#import pandas as pd
from flask import Flask, jsonify, request, make_response
import json
import pickle
import scipy.spatial.distance as distance
import json
import flask_cors
import pandas as pd

religious_affil = {
    -1:	'Not reported',
    -2:	'Not applicable',
    22:	'American Evangelical Lutheran Church',
    24:	'African Methodist Episcopal Zion Church',
    27:	'Assemblies of God Church',
    28:	'Brethren Church',
    30:	'Roman Catholic',
    33:	'Wisconsin Evangelical Lutheran Synod',
    34:	'Christ and Missionary Alliance Church',
    35:	'Christian Reformed Church',
    36:	'Evangelical Congregational Church',
    37:	'Evangelical Covenant Church of America',
    38:	'Evangelical Free Church of America',
    39:	'Evangelical Lutheran Church',
    40:	'International United Pentecostal Church',
    41:	'Free Will Baptist Church',
    42:	'Interdenominational',
    43:	'Mennonite Brethren Church',
    44:	'Moravian Church',
    45:	'North American Baptist',
    47:	'Pentecostal Holiness Church',
    48:	'Christian Churches and Churches of Christ',
    49:	'Reformed Church in America',
    50:	'Episcopal Church, Reformed',
    51:	'African Methodist Episcopal',
    52:	'American Baptist',
    53:	'American Lutheran',
    54:	'Baptist',
    55:	'Christian Methodist Episcopal',
    57:	'Church of God',
    58:	'Church of Brethren',
    59:	'Church of the Nazarene',
    60:	'Cumberland Presbyterian',
    61:	'Christian Church (Disciples of Christ)',
    64:	'Free Methodist',
    65:	'Friends',
    66:	'Presbyterian Church (USA)',
    67:	'Lutheran Church in America',
    68:	'Lutheran Church - Missouri Synod',
    69:	'Mennonite Church',
    71:	'United Methodist',
    73:	'Protestant Episcopal',
    74:	'Churches of Christ',
    75:	'Southern Baptist',
    76:	'United Church of Christ',
    77:	'Protestant, not specified',
    78:	'Multiple Protestant Denomination',
    79:	'Other Protestant',
    80:	'Jewish',
    81:	'Reformed Presbyterian Church',
    84:	'United Brethren Church',
    87:	'Missionary Church Inc',
    88:	'Undenominational',
    89:	'Wesleyan',
    91:	'Greek Orthodox',
    92:	'Russian Orthodox',
    93:	'Unitarian Universalist',
    94:	'Latter Day Saints (Mormon Church)',
    95:	'Seventh Day Adventists',
    97:	'The Presbyterian Church in America',
    99:	'Other',
    100: 'Original Free Will Baptist',
    101:'Ecumenical Christian',
    102:'Evangelical Christian',
    103:'Presbyterian',
    105:'General Baptist',
    106:'Muslim',
    107: 'Plymouth Brethren',
}



# create app
app = Flask(__name__, static_folder='static')
#cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = flask_cors.CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


# load "model" data
df_final = pickle.load(open('static/df_final_names.pkl', 'rb'))
df_final = df_final.loc[:,~df_final.columns.duplicated()]


df_scaled = pickle.load(open('static/scaled_df.pkl', 'rb'))

with open('static/card_info_google.txt') as f:
    card_dict = json.load(f)

with open('static/states.txt') as f:
    states_dict = json.load(f)


# routes
@app.route('/model/', methods=['POST', 'OPTIONS'])
@flask_cors.cross_origin()
def predict():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    # get data
    data = request.get_json()[0]
    colleges = [data['dream'], data['target'], data['safety']]

    tops = []
    closest_list = []
    ids = []

    for i, college in enumerate(colleges):
        college_id = get_index(college)

        # get scaled data for this college
        test_college = df_scaled.iloc[[college_id]]
        ids.append(college_id)

        # get scaled distance from every other college (manhattan or minkowski seem best)
        ary = distance.cdist(df_scaled, test_college, metric='cityblock')

        # make a df with distances to manipulate for this school
        results = df_final.copy() # different results
        results['dist'] = ary

        # sort them so we can examine top matches
        closest = results.sort_values(by='dist')
        closest = list(closest['INSTNM'])[1:8]
        closest_list += closest

        tops = tops + [closest[0]]


    # now check out a combo of all three schools
    mean_school = list(df_scaled.iloc[ids].mean())
    combo_school = pd.DataFrame([mean_school], columns=df_scaled.columns)
    ary = distance.cdist(df_scaled, combo_school, metric='cityblock')
    results = df_final.copy()
    results['dist'] = ary
    closest = results.sort_values(by='dist')
    closest = list(closest['INSTNM'])[1:10]
    closest_list += closest
    tops = closest[:2] + tops


    tops = [x for x in tops if x not in colleges]
    result = dupes(closest_list, colleges)
    tops = [x for x in tops if x not in result]
    result = result + tops  # duplicates first, then top results starting with dream school #1

    output = {}
    output['results'] = []

    for college in result:
        i = get_index(college)
        stats = df_final.iloc[i]

        control = 'Public'
        if stats['CONTROL'] == 1:
            control = 'Public'
        else:
            control = 'Private'

        school = {
                'schoolname': stats['INSTNM'],
                'url': stats['INSTURL'],
                'city': stats['CITY'],
                'stabbr': stats['STABBR'],
                'state': states_dict[stats['STABBR']],
                'student_pop': stats['UGDS'],
                'control': control,
                'avg_tuition': stats['COSTT4_A'],
                'admission_rate': stats['ADM_RATE'],
                'avg_ACT': stats['ACTCMMID'],  # not in the df_final_names unfortunately.  Need to redo
                'avg_SAT': stats['SAT_AVG'],
                #'religious_affil': religious_affil[stats['RELAFFIL']],
                'HBCU': stats['HBCU'],
                'WOMENONLY': stats['WOMENONLY'],
                'MENONLY': stats['MENONLY'],

                #'percent_match': results[results['INSTNM']==college]['dist']
                }
        image = card_dict[college].get('image')
        desc = card_dict[college].get('description')
        if image: school['image'] = image
        if desc: school['description'] = desc

        output['results'].append(school)

    # output['results'] = sorted(output['results'], lambda x: x['student_pop'])
    #cors_response = corsify_response(jsonify(output))
    return jsonify(output)


@app.route('/colleges/', methods=['GET'])
def colleges():
    with open('static/colleges.txt') as json_file:
        data = json.load(json_file)
    return data


def dupes(all, original):
    # returns list of schools found in closest matches for multiple input schools
    # all is a list of schools that were matches
    # original is a list of the schools that were original inputs from user
    all = [x for x in all if x not in original]  # dump any that are part of original list (there is better way to do this)
    my_counts = sorted([[x, all.count(x)] for x in set(all)], key=lambda x: x[1])  # get sorted list by number of times they occur in list
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

# def corsify_response(response):
#     #response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>College rec server</h1>"


if __name__ == '__main__':
    app.run(debug=True)
