'''
Scrapes the meta data of websites of all colleges to get
- description
- image
'''


import requests
import json
import pandas
from bs4 import BeautifulSoup #Import stuff
import requests
from flask import request
import pickle
from selenium import webdriver

import time
from selenium import webdriver
from bs4 import BeautifulSoup

df = pickle.load(open('static/df_final_names.pkl', 'rb'))
urls = list(df['INSTURL'])
names = list(df['INSTNM'])

# Create a new Firefox browser object
browser = webdriver.Chrome('/Users/aaronlee/PycharmProjects/college_api/chromedriver')

def which_url(base_url):
    url = base_url

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except:
        pass

    try:
        url = 'https://' + base_url
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except:
        pass

    try:
        url = 'http://' + base_url
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except:
        pass

    try:
        url = base_url['https//' + base_url[4:]]
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except:
        pass

    return base_url


def get_image(base_url):
    # og:title - The title of your object as it should appear within the graph, e.g., "The Rock".
    # og:type - The type of your object, e.g., "video.movie". Depending on the type you specify, other properties may also be required.
    # og:image - An image URL which should represent your object within the graph.
    # og:url - The canonical URL of your object that will be used as its permanent ID in the graph, e.g., "https://www.imdb.com/title/tt0117500/".
    # response = requests.get(url)
    # if response.status_code == 200:
    #     return good_response(response)
    url = which_url(base_url)

    try:
        # Go to a website, click the element with the id 'show-data' and wait 2 secs
        browser.get(url)
        time.sleep(10)
        # Create BeautifulSoup object from page source.
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        return(good_response(soup, url))

    except Exception as e:
        print(e)

    return({'url': url})


def good_response(soup, url):
    info = {}
    info['url'] = url
    info['title'] = soup.find("title").text

    for tag in soup.find_all("meta"):
        if tag.get("property", None) == "og:title":
            info['title'] = tag.get("content", None)
        elif tag.get("property", None) == "og:image":
            info['image'] = tag.get("content", None)
        elif tag.get("property", None) == "title" and not info.get('title'):
            info['title'] = tag.get("content", None)
        elif tag.get("name", None) == "description":
            info['description'] = tag.get("content", None)

    # biggest = 0
    # if not info.get('image'):
    #     for pic in soup.find_all('img'):
    #         width = float(pic.get('height'))
    #         if width >= biggest:
    #             if pic.has_attr('src'):
    #                 print(pic['src'])
    #                 biggest = width
    #                 info['image'] = pic.get('src')

    return info




all_cards = {}
for url, name in zip(urls, names):
    info = get_image(url)
    info['INSTNM'] = name
    print(info)
    all_cards[name] = info



with open('card_info.txt', 'w') as f:
    f.write(json.dumps(all_cards))