from flask import Flask

from data.make_dataset import process_incoming_data
import pandas as pd 

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
    

