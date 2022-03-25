from crypt import methods
from email.header import Header
from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from math import ceil
from timeit import repeat
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, make_response
from matplotlib.pyplot import connect
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import csv
# from templates.Preprocessing_Scripts.fetch_data import *
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn import preprocessing
import time
from removeOverlap.dgrid import *
# from removeOverlap.force_scheme import *
# import * from generate_data_circle_packing

# personalityFile = "dummyPersonalityScores"
# featureFile = "dummyFeatureData"
# brightnessFile = "dummyBrightness"
# accelerometerFile = "dummyAccelerometer"
# gyroscopeFIle = "dummyGyroscope"

personalityFile = "PersonalityScores.csv"
featureFile = "featureData.csv"
brightnessFile = "brightness_processed.csv"
accelerometerFile = "accelerometer_processed.csv"
gyroscopeFile = "gyroscope_processed.csv"
lockStateFile = "lockstate_processed.csv"


def getPCA(df, columns, width, height):
    df = df.groupby("participantId").mean().reset_index()
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df.loc[:,columns])

    pca_result_overlap_removed = pca_result

    x = np.expand_dims(pca_result[:,0], axis=1)
    y = np.expand_dims(pca_result[:,1], axis=1)

    if width is not None and height is not None:
        x = np.interp(x, (x.min(), x.max()), (20, width-20))
        y = np.interp(y, (y.min(), y.max()), (height-20, 20))
        cords = np.concatenate((x,y), axis=1)
        pca_result_overlap_removed = DGrid(icon_width=1, icon_height=1, delta=2).fit_transform(cords)
    else:
        pca_result_overlap_removed = pca_result

    pca_x = pca_result_overlap_removed[:,0]
    pca_y = pca_result_overlap_removed[:,1]
    return pca_x, pca_y

def getTSNE(df, columns, width, height):
    # df = df.groupby("participantId").mean().reset_index()
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300, init='pca')
    tsne_result = tsne.fit_transform(df.loc[:,columns])
    
    tsne_result_overlap_removed = tsne_result

    # comment this section to remove Dgrid
    x = np.expand_dims(tsne_result[:,0], axis=1)
    y = np.expand_dims(tsne_result[:,1], axis=1)

    if width is not None and height is not None:
        x = np.interp(x, (x.min(), x.max()), (20, width-20))
        y = np.interp(y, (y.min(), y.max()), (height-20, 20))
        cords = np.concatenate((x,y), axis=1)
        cords = preprocessing.StandardScaler().fit_transform(cords)
        cords = ForceScheme().fit_transform(cords)
        tsne_result_overlap_removed = DGrid(icon_width=1/3, icon_height=1/3, delta=10).fit_transform(cords)
    else:
        tsne_result_overlap_removed = tsne_result

    tsne_x = tsne_result_overlap_removed[:,0]
    tsne_y = tsne_result_overlap_removed[:,1]
    return tsne_x, tsne_y

def getClusters(df, columns, clusteringMethod="kmeans"):
    print("clustering begin" + '*'*100)
    X = df.loc[:, columns]
    clusters = []
    # kmeans clustering
    if clusteringMethod == "kmeans":
        clustering = KMeans(n_clusters=2, random_state=0).fit(X)
        clusters = clustering.labels_
    elif clusteringMethod == "spectral":
        clustering = SpectralClustering(n_clusters=2, assign_labels='discretize', random_state=0).fit(X)
        clusters = clustering.labels_
    print("clusters", clusters)
    return clusters


app = Flask(__name__, static_url_path='', static_folder='')

@app.route("/ping")
def hello_world():
    return jsonify("Apple")

# @app.route('/login.html')
# def login():
#     return render_template('pages/login.html', title="Login")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title="Home", header="Home")

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

    featureData = pd.read_csv(os.path.join("data/processedData", featureFile)).groupby("participantId").mean().reset_index()
    personalityData = pd.read_csv(os.path.join("data/processedData", personalityFile))
    # print("featureData:", featureData.shape, "personalityData", personalityData.shape)
    # print("featureData['participantId']", featureData["participantId"].tolist())
    # personalityData = personalityData[personalityData['participantId'].isin(featureData["participantId"].tolist())]
    # personalityData.to_csv(os.path.join("data/processedData", personalityFile), header=True, index=False)

    columns = featureData.columns.values[2:]    #get all the feature columns
    width = None
    height = None

    if request.method == 'POST':
        content = request.get_json()
        width = content['width']
        height = content['height']

        if len(columns) > 1:   #in case of feature columns are selected in dropdown, consider only those
            columns = content['featureColumns']    
            message = "status1:file updated"
        else:
            message = "status2:single column"
    else:
        message = "status3:file reset"
    
    x, y = getTSNE(featureData, columns, width, height)     #dim reduction
    # x, y = getPCA(featureData, columns, width, height)     #dim reduction
    # clusters = getClusters(featureData, columns, clusteringMethod="spectral")    #spectralClustering
    # clusters = getClusters(featureData, columns, clusteringMethod="kmeans")    #k-means clustering
    personalityData["x"], personalityData["y"] = x, y
    # personalityData["clusters"] = clusters
    
    personalityData.to_csv(os.path.join("data/processedData", personalityFile), index=False, header=True)
    return jsonify(message)

@app.route('/fetchPersonalityScores', methods=['GET'])
def fetchPersonalityScores():
    """
    Return Data for Chart1: Personality scores that are used to make glyphs
    """
    if request.method == 'GET':
        print("Request recieved for fetching Personality scores")
        data = pd.read_csv(os.path.join("data/processedData", personalityFile))

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

@app.route('/filterParticipants', methods=['POST'])
def filterParticipantsDummy():
    """
    Returns Data for Chart2: Radial chart to visualize sleep/awake activity using 
    brightness, accelerometer and gyroscope data
    dummy data
    """
    if request.method == 'POST':
        content = request.get_json()
        
        # filename = content['filename']
        participantId = content['participantId']
        attributes = content["attributes"]
        print("request recieved", content)  #print statement
        
        strt = time.time()
        filenames = {"brt":brightnessFile, "acc":accelerometerFile, "gyr":gyroscopeFile}
        data = pd.DataFrame()
        for attr,checkState in attributes.items():
            if checkState:
                df = pd.read_csv(os.path.join("data/processedData", filenames[attr]))
                df = df[df["participantId"] == participantId]#.sample(frac=0.001)

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
        print(time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} participant:{participantId}")

    else:
        return jsonify("no post requests")

@app.route('/filterParticipantsNew', methods=['POST'])
def filterParticipantsNew():
    """
    Returns Data for Chart2: Radial chart to visualize sleep/awake activity using 
    brightness, accelerometer and gyroscope data
    Real data
    """
    if request.method == 'POST':
        content = request.get_json()
        # filename = content['filename']
        participantId = content['participantId']
        attributes = content["attributes"]

        print("request recieved", content)  #print statement
        
        strt = time.time()
        filenames = {"brt":brightnessFile, "acc":accelerometerFile, "gyr":gyroscopeFile, "lck":lockStateFile}
        data = pd.DataFrame()
        for attr,checkState in attributes.items():
            print("attr:", attr, "checkState:", checkState)
            if checkState:
                print(participantId)
                df = pd.read_csv(os.path.join("data", filenames[attr]))
                df = df[df["participantId"]==participantId]#.sample(frac=0.001)
                dfImputed = pd.DataFrame()
                
                #addind -1 values for minutesOfTheDay where data is not present
                #creating df with all mins to impute missing values
                mins = [i for i in range(0,1440)]
                allMinutes = pd.DataFrame({"minuteOfTheDay":mins})
                
                for date in df.date.unique():
                    dfDate = df[df.date == date].copy()
                    dfDate = pd.merge(dfDate, allMinutes, how="right", on="minuteOfTheDay")
                
                # df_call["MinuteOfTheDay"] = (df_call.timestamp - df_call.timestamp.dt.floor('d')).astype('timedelta64[m]')
                    
                    if attr == "lck":
                        dfDate.loc[0,attr]=0
                    else:
                        # dfDate.loc[0,attr]=0
                        dfDate[attr].fillna(0, inplace=True)
                    dfDate.ffill(inplace=True)
                    dfDate.bfill(inplace=True)
                    dfImputed = pd.concat([dfImputed, dfDate], axis=0)

                    # if attr=="brt":
                    #     temp = pd.read_csv(os.path.join("data", filenames['lck']))
                    #     temp = temp[(temp["participantId"]==participantId) & (temp.date == date)].copy()
                    #     temp = temp.merge(dfImputed, on=["participantId", "device", "date", "minuteOfTheDay"], how="inner")
                    #     dfImputed = temp[temp.lck==1]
                    #     dfImputed.drop("lck", axis=1, inplace=True)

                data = pd.concat([data, dfImputed])
        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredParticipants.csv"
        resp.headers["Content-Type"] = "text/csv"
        print("Execution Time", time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} participant:{participantId}")

    else:
        return jsonify("no post requests")

@app.route('/fetchAggFeatures', methods=['GET', 'POST'])
def fetchAggFeatures():
    """
    Returns Data for Chart3: Parallel cordinate chart to visualize extracted features
    """
    print("Request recieved for fetching Aggregated feature data")
    data = pd.read_csv(os.path.join("data/processedData", featureFile))
    # Aggregating based on participantId
    data = data.groupby("participantId").mean().reset_index()
    #getting cluster id for participants form personality file
    df = pd.read_csv(os.path.join("data/processedData", personalityFile)).loc[:, ["participantId", "clusters"]]
    data = pd.merge(data, df, how="left")
    resp = make_response(data.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/fetchIndividualFeatures', methods=['POST'])
def fetchIndividualFeatures():
    """
    Returns Data for Chart3: Parallel cordinate chart to visualize extracted features - This will return the feature of single participant.
    """
    if request.method == 'POST':
        content = request.get_json()
        # filename = content['filename']
        participantId = content['participantId']

        print("Request recieved for fetching individual feature data")
        data = pd.read_csv(os.path.join("data/processedData", featureFile))
        # Fetching data for selected participant
        data = data[data["participantId"]==participantId].copy()
        print('INDIVIDUAL'*10,"\n", data.info(memory_usage='deep'))

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=individualFeatureData.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

# test code
@app.route('/dataTable', methods=['GET', 'POST'])
def dataTable(): 
    if request.method == 'GET':
        df = pd.read_csv(os.path.join("data/processedData", featureFile))
        fieldnames = df.columns
        # len = df.shape[0]
        # resp = make_response(df.to_csv())
        # resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        # resp.headers["Content-Type"] = "text/csv"

        results = df.to_dict('records')
        # results = []
        # user_csv = request.form.get('user_csv').split('\n')
        # reader = csv.DictReader(user_csv)
        
        # for row in reader:
        #     results.append(dict(row))

        # fieldnames = [key for key in results[0].keys()]
        # print(list(results))
        # return render_template('test3.html', results=results, fieldnames=fieldnames, len=len)
        return jsonify(results)
    
    if request.method == 'POST':
        content = request.get_json()

        data = content.split("\r\n")[1:]
        data1 = []
        [data1.append(d.replace("\"", "").split(",")) for d in data]
        df = pd.read_csv(os.path.join("data/processedData", featureFile))
        df.drop(df.index, inplace=True)
        df = pd.DataFrame(data1[1:], columns=df.columns)
        os.remove(os.path.join("data/processedData", featureFile))
        df.to_csv(os.path.join("data/processedData", featureFile), index=False, header=True)

        print("File updated")

        message = "Feature file updated by the user"
        return jsonify(message)
        # test code ends


# Get a random patritipant that can be used to have a selection when page is refreshed
@app.route('/getRandomParticipant', methods=['GET'])
def getRandomParticipant():
    df = pd.read_csv(os.path.join("data/processedData", personalityFile))
    participants = df.participantId.unique()
    participant = [(np.random.choice(participants, replace=False))]
    return jsonify(participant)

if __name__ == "__main__":
    app.run(port=5003, debug=True)