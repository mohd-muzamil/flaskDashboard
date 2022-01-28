from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from math import ceil
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, make_response
from matplotlib.pyplot import connect
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from sshtunnel import SSHTunnelForwarder
import pandas as pd
# from templates.Preprocessing_Scripts.fetch_data import *
import os
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import time
# import * from generate_data_circle_packing

featureDataFile = "dummyFeatureData"
personalityDataFile = "dummyPersonalityScores"

def getPCA(df, columns):
    df = df.groupby("participantId").mean().reset_index()
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df.loc[:,columns])
    pca_x = pca_result[:,0]
    pca_y = pca_result[:,1]
    return pca_x, pca_y

def getTSNE(df, columns):
    df = df.groupby("participantId").mean().reset_index()
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_result = tsne.fit_transform(df.loc[:,columns])
    tsne_x = tsne_result[:,0]
    tsne_y = tsne_result[:,1]
    return tsne_x, tsne_y

app = Flask(__name__, static_url_path='', static_folder='')

@app.route("/ping")
def hello_world():
    return jsonify("pong")

# @app.route('/login.html')
# def login():
#     return render_template('pages/login.html', title="Login")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title="Home", header="Home")


@app.route('/view2.html')


# @app.route("/participants", methods=["GET", "POST"])
# def participants():
#     if request.method == 'POST':
#         attributes = fetch_participants()

#         '''
#         tab1, just 2 containers, maybe 3 if some additional feature data is required.
#         I would like to call a script that fetches entire data and derives features from that data for all the participants,
#         and I would like to cluster those participants based on the extracted features.
#         This is where most of the Behaviorial analysis is required.
#         once clustered, it would be nice to have a parallel coordinates chart that shows the derived features values for all the participants.
#         when one of more participants are selected, features of only those participants needs to be displayed. (brain storming is required)
#         good to have this in tab 1 of the dashboard
#         '''

#         '''
#         Based on clustering done on tab1 data, fill colors in tab2 chart for the participant circles.
#         single/multiple selection (need a bit of thinking on this.)
#         Think about utility of haivng to compare the data between 2 or more participants.
#         based on selections, show charts of mobile screen usage, estimated sleep pattern, mobility, calling patterns, (lookg for other features that can be derived here.)
#         '''
#         return jsonify(attributes)


# @app.route("/fetch_data", methods=["GET", "POST"])
# def participant_data():
#     if request.method == 'POST':
#         participantId = request.form['participantId']
#         attribute = request.form['attribute']
#         print("from fetch data", participantId)
#         data = fetch_data(participantId=participantId,
#                           attribute=attribute, allparticipants=True)

    # Copy code from notebooks that analyse data and calculate sleep times.
    # Call scripts that make plots for screen usage time and sleep estimates and try to fill myViz2 and 3.
    # return jsonify(data)


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

@app.route('/dimReduceParticipants', methods=['GET', 'POST'])
def dimReduceParticipants():
    global featureData
    global personalityData

    featurefilename = os.path.join("data", featureDataFile)
    featureData = pd.read_csv(featurefilename)
    personalityfilename = os.path.join("data", personalityDataFile)
    personalityData = pd.read_csv(personalityfilename)
        
    if request.method == 'POST':
        content = request.get_json()
        columns = content['featureColumns']
        if len(columns) > 1:
             x , y = getPCA(featureData, columns)
             message = "status1:file updated"
        else:
            x, y = getPCA(featureData, featureData.columns.values[2:])
            message = "status2:single column"
    else:
        x, y = getPCA(featureData, featureData.columns.values[2:])
        message = "status3:file reset"
    personalityData["x"], personalityData["y"] = x, y
    personalityData.to_csv(personalityfilename, index=False, header=True)
    
    return jsonify(message)

@app.route('/fetchPersonalityScores', methods=['GET'])
def fetchPersonalityScores():
    """
    Return Data for Chart1: Personality scores that are used to make glyphs
    """
    if request.method == 'GET':
        print("Request recieved for fetching Personality scores")
        filename = os.path.join("data", "dummyPersonalityScores")
        data = pd.read_csv(filename)

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

@app.route('/filterParticipants', methods=['POST'])
def filterParticipants():
    """
    Returns Data for Chart2: Radial chart to visualize sleep/awake activity using 
    brightness, accelerometer and gyroscope data
    """
    if request.method == 'POST':
        content = request.get_json()
        # filename = content['filename']
        participantId = content['participantId']
        attributes = content["attributes"]

        print("request recieved", content)  #print statement
        
        strt = time.time()
        filenames = {"brt":"dummyBrightness", "acc":"dummyAccelerometer", "gyr":"dummyGyroscope"}
        data = pd.DataFrame()
        for attr,checkState in attributes.items():
            print("attr:", attr, "checkState:", checkState)
            if checkState:
                filename = os.path.join("data", filenames[attr])
                df = pd.read_csv(filename)
                df = df[df["participantId"]==participantId]#.sample(frac=0.001)

                #Randomly removing data for night time, this step wont be necessary once the proper synthetic data is made
                for i in range(ceil(df.shape[0]/1440)):
                    x = np.random.randint(0, 3*60)
                    sleepDur = np.random.randint(6,9)
                    startindex = i * 1440 + x
                    df.iloc[startindex:(startindex+sleepDur*60), -1] = 0
                    # data = data[data.iloc[:,-1] != 0]

                data = pd.concat([data, df])
    
        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredParticipants.csv"
        resp.headers["Content-Type"] = "text/csv"

        print("d3.js in Action",data)

        print(time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} participant:{participantId}")

    else:
        print("Snowwoman no post values")
        return jsonify("no post requests")


if __name__ == "__main__":
    app.run(port=5003, debug=True)