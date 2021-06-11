'''
Flask web app to host college recommendation model
Takes in three colleges (Dream, Target, Safety)
Returns matches from rec model
'''

from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file, \
    get_template_attribute, session
#from flask_session import Session
from werkzeug.utils import secure_filename
#import numpy as np
#from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
#from keras.preprocessing import image
#from keras.models import load_model
#import os, io, sys, time
import random


#best_model = 'best_model.h5'
#model = load_model(best_model)  # college rec model

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def matches(colleges):
    return {'University of Michigan':100, 'University of Illinois':88, 'DePaul University':82}


if __name__ == '__main__':
    app.run()


