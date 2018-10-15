from flask import Flask

import pandas as pd 

import json

from data.read_json import parse_json
from data.make_dataset import process_incoming_data



app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/postdata", methods = ['POST'])
def postJsonHandler():
    if request.is_json:
        content = request.get_json()
        print (content)
    return 'JSON received'

if __name__ == '__main__':
    app.run(debug=True, port= 5000)
    

