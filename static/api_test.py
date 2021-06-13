import requests
import json



school_data = [
    {
        'dream':'Loyola University Chicago',
        'target':'DePaul University',
        'safety':'University of Illinois at Urbana-Champaign'
    },
]

url = 'https://college-rec-system.herokuapp.com/model/'
#url = 'http://127.0.0.1:5000/model/'

data = requests.post(url, json=school_data)
print(data.text)

# url2 = 'https://college-rec-system.herokuapp.com/colleges/'
# url2 = 'http://127.0.0.1:5000/colleges/'
# colleges = requests.get(url2)
# print(colleges.text)
#
# url3 = 'https://college-rec-system.herokuapp.com/'
# url3 = 'http://127.0.0.1:5000/'
# home = requests.get(url3)
# print(home.text)

# with open('static/colleges.txt') as json_file:
#     data = json.load(json_file)


