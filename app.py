from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from sshtunnel import SSHTunnelForwarder
from data_reformat import handle_recursive_dict
from fetch_data import *
import os
# import * from generate_data_circle_packing

app = Flask(__name__, static_url_path='', static_folder='')


# @app.route('/login.html')
# def login():
#     return render_template('pages/login.html', title="Login")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title="Home", header="Home")


@app.route('/view2.html')


@app.route("/participants", methods=["GET", "POST"])
def participants():
    if request.method == 'POST':
        attributes = fetch_participants()

        '''
        tab1, just 2 containers, maybe 3 if some additional feature data is required.
        I would like to call a script that fetches entire data and derives features from that data for all the participants,
        and I would like to cluster those participants based on the extracted features.
        This is where most of the Behaviorial analysis is required.
        once clustered, it would be nice to have a parallel coordinates chart that shows the derived features values for all the participants.
        when one of more participants are selected, features of only those participants needs to be displayed. (brain storming is required)
        good to have this in tab 1 of the dashboard
        '''

        '''
        Based on clustering done on tab1 data, fill colors in tab2 chart for the participant circles.
        single/multiple selection (need a bit of thinking on this.)
        Think about utility of haivng to compare the data between 2 or more participants.
        based on selections, show charts of mobile screen usage, estimated sleep pattern, mobility, calling patterns, (lookg for other features that can be derived here.)
        '''
        return jsonify(attributes)


@app.route("/fetch_data", methods=["GET", "POST"])
def participant_data():
    if request.method == 'POST':
        participantId = request.form['participantId']
        attribute = request.form['attribute']
        print("from fetch data", participantId)
        data = fetch_data(participantId=participantId,
                          attribute=attribute, allparticipants=True)

    # Copy code from notebooks that analyse data and calculate sleep times.
    # Call scripts that make plots for screen usage time and sleep estimates and try to fill myViz2 and 3.
    return jsonify(data)


# routine to generate the data required to make a circle packing chart.
# @app.route("/circle_packing_data_gen")
# def circle_packing_data_gen():
#     generate_data_circle_packing()
#     return None

@app.route("/circle_packing")
def circle_packing():
    return render_template('circle_packing.html', title="Jeni", header="Home")


@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/test1")
def test1():
    return render_template('test1.html')

@app.route("/test2")
def test2():
    print("inside approute test2", os.getcwd())
    data_path = "/home/mmh/initial_analysis/all_data"
    #preprocessing combine ios android data and put it in a single file, add a column for device
    df_accelerometer = None #pd.read_csv(os.path.join(data_path), "Acceleromter")
    df_gyroscope = None
    df_brightness = None
    


    return render_template('test2.html')


@app.route('/test3/')
def test3():
     return render_template('test3.html')

if __name__ == "__main__":
    app.run(port=5003, debug=True)
