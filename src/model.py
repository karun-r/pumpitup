from flask import Flask
from flask import request
import requests

import pandas as pd 

import json
import os,time

from data.read_json import parse_json
from data.make_dataset import process_incoming_data



app = Flask(__name__)
app.config['TESTING'] = True

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/postdata", methods = ['POST'])
def postJsonHandler():
    content = request.get_json()
    user_id = "karunr" #tmp fix
    user_folder = str.format("data/external/users/{0}",user_id)
    if not os.path.isdir(user_folder):
      os.makedirs(user_folder)
    user_file_path = str.format("data/external/users/{0}/{1}_{2}.json",user_id,user_id, int(time.time()))
    with open(user_file_path, 'w') as outfile:
      json.dump(content, outfile)
    #inc_df = parse_json()
    return "JSON Receieved"
 

if __name__ == '__main__':
    app.run(debug=True, port= 5000)
    

