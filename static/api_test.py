import requests
import json
import pandas
from bs4 import BeautifulSoup #Import stuff
import requests
from flask import request
import pickle


school_data = [
    {
        #"dream":"Loyola University Chicago",
        "target":"DePaul University",
        #"safety":"University of Illinois at Urbana-Champaign"
    },
]

#url = 'https://college-rec-system.herokuapp.com/model/'
url = 'http://127.0.0.1:5000/model/'

data = requests.post(url, json=school_data)
print(data.text)

#url2 = 'https://college-rec-system.herokuapp.com/colleges/'
#url2 = 'http://127.0.0.1:5000/colleges/'
#colleges = requests.get(url2)
#print(colleges.text)
#
# url3 = 'https://college-rec-system.herokuapp.com/'
# url3 = 'http://127.0.0.1:5000/'
# home = requests.get(url3)
# print(home.text)






#####
# TEST code
####

# with open('static/card_info.txt') as f:
#     card_dict = json.load(f)

# print(card_dict)

# count = 0
# for college in card_dict.keys():
#     if card_dict[college].get('description'): count += 1
#
# print(count)

# print(card_dict['The University of Alabama'].get('image'))
#

# print('Trying combo school')
# df_scaled = pickle.load(open('static/scaled_df.pkl', 'rb'))
# print('single school')
# print(df_scaled.iloc[[1]])
#
# print()
# print('three schools')
# print(df_scaled.iloc[[1,2,3]])
#
# print()
# print('combo schools')
# mean_row = list(df_scaled.iloc[[1,2,3]].mean())
# print(pandas.DataFrame([mean_row], columns=df_scaled.columns))

# df_final = pickle.load(open('static/df_final_names.pkl', 'rb'))
# df_scaled = pickle.load(open('static/scaled_df.pkl', 'rb'))
#
# print(df_final.head())
# print(df_final.columns)
# print(df_final['CONTROL'].info())
# print(df_final['RELAFFIL'].unique())
