from flask import Flask
from flask import request
import requests

import pandas as pd 

import json
import os,time

from src.data.read_json import parse_json
from src.data.make_dataset import process_incoming_data

from src.models.predict_model import load_model, predict


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
    csv_file_path  = str.format("data/external/users/{0}/{1}_{2}.csv",user_id,user_id, int(time.time()))
    with open(user_file_path, 'w') as outfile:
      json.dump(content, outfile)
    parse_json(user_file_path,csv_file_path)
    incoming_df = pd.read_csv(csv_file_path)
    processed_df = process_incoming_data(incoming_df)
    print(processed_df.columns)
    ml_model = load_model()
    output = predict(ml_model,processed_df)
    print(output)
    return output[0]
 

if __name__ == '__main__':
    app.run(debug=True, port= 5000)
    

