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
import random as rand
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
# gyroscopeFIle = "dummygyroscope"

personalityFile = "PersonalityScores.csv"
featureFile = "featureData.csv"
brightnessFile = "Brightness_processed.csv"
accelerometerFile = "Accelerometer_processed.csv"
gyroscopeFile = "Gyroscope_processed.csv"
lockStateFile = "Lock_state_processed.csv"


def getPCA(df, columns, width, height):
    df = df.groupby("participantId").mean().reset_index()
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df.loc[:, columns])

    pca_result_overlap_removed = pca_result

    x = np.expand_dims(pca_result[:, 0], axis=1)
    y = np.expand_dims(pca_result[:, 1], axis=1)

    if width is not None and height is not None:
        x = np.interp(x, (x.min(), x.max()), (20, width-20))
        y = np.interp(y, (y.min(), y.max()), (height-20, 20))
        cords = np.concatenate((x, y), axis=1)
        pca_result_overlap_removed = DGrid(
            icon_width=1, icon_height=1, delta=2).fit_transform(cords)
    else:
        pca_result_overlap_removed = pca_result

    pca_x = pca_result_overlap_removed[:, 0]
    pca_y = pca_result_overlap_removed[:, 1]
    return pca_x, pca_y


def getTSNE(df, columns, width, height):
    # df = df.groupby("participantId").mean().reset_index()
    tsne = TSNE(n_components=2, verbose=1,
                perplexity=40, n_iter=300, init='random', learning_rate="auto")
    tsne_result = tsne.fit_transform(df.loc[:, columns])

    tsne_result_overlap_removed = tsne_result

    # comment this section to remove Dgrid
    x = np.expand_dims(tsne_result[:, 0], axis=1)
    y = np.expand_dims(tsne_result[:, 1], axis=1)

    if width is not None and height is not None:
        x = np.interp(x, (x.min(), x.max()), (20, width-20))
        y = np.interp(y, (y.min(), y.max()), (height-20, 20))
        cords = np.concatenate((x, y), axis=1)
        cords = preprocessing.StandardScaler().fit_transform(cords)
        cords = ForceScheme().fit_transform(cords)
        # tsne_result_overlap_removed = DGrid(
        #     icon_width=1/3, icon_height=1/3, delta=10).fit_transform(cords)
        tsne_result_overlap_removed = DGrid(
            icon_width=1/2, icon_height=1/2, delta=10).fit_transform(cords)
    else:
        tsne_result_overlap_removed = tsne_result

    tsne_x = tsne_result_overlap_removed[:, 0]
    tsne_y = tsne_result_overlap_removed[:, 1]
    return tsne_x, tsne_y


# Decided not to implement clustering functionality
def getClusters(df, columns, clusteringMethod="kmeans"):
    print("clustering begin" + '*'*100)
    X = df.loc[:, columns]
    clusters = []
    # kmeans clustering
    if clusteringMethod == "kmeans":
        clustering = KMeans(n_clusters=2, random_state=0).fit(X)
        clusters = clustering.labels_
    elif clusteringMethod == "spectral":
        clustering = SpectralClustering(
            n_clusters=2, assign_labels='discretize', random_state=0).fit(X)
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

# @app.route("/participantIds", methods=["GET", "POST"])
# def participantIds():
#     if request.method == 'POST':
#         attributes = fetch_participantIds()

#         '''
#         tab1, just 2 containers, maybe 3 if some additional feature data is required.
#         I would like to call a script that fetches entire data and derives features from that data for all the participantIds,
#         and I would like to cluster those participantIds based on the extracted features.
#         This is where most of the Behaviorial analysis is required.
#         once clustered, it would be nice to have a parallel coordinates chart that shows the derived features values for all the participantIds.
#         when one of more participantIds are selected, features of only those participantIds needs to be displayed. (brain storming is required)
#         good to have this in tab 1 of the dashboard
#         '''

#         '''
#         Based on clustering done on tab1 data, fill colors in tab2 chart for the participantId circles.
#         single/multiple selection (need a bit of thinking on this.)
#         Think about utility of haivng to compare the data between 2 or more participantIds.
#         based on selections, show charts of mobile screen usage, estimated sleep pattern, mobility, calling patterns, (lookg for other features that can be derived here.)
#         '''
#         return jsonify(attributes)


# @app.route("/fetch_data", methods=["GET", "POST"])
# def participantId_data():
#     if request.method == 'POST':
#         participantId = request.form['participantId']
#         attribute = request.form['attribute']
#         print("from fetch data", participantId)
#         data = fetch_data(participantId=participantId,
#                           attribute=attribute, allparticipantIds=True)

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
    # preprocessing combine ios android data and put it in a single file, add a column for device
    # pd.read_csv(os.path.join(data_path), "Acceleromter")
    df_accelerometer = None
    df_gyroscope = None
    df_brightness = None
    return render_template('test2.html')


@app.route('/test3/')
def test3():
    return render_template('test3.html')


@app.route('/dimReduceparticipantIds', methods=['GET', 'POST'])
def dimReduceparticipantIds():
    global featureData
    global personalityData

    df = pd.read_csv(os.path.join("data/processedData",
                     featureFile), sep="|")
    print("*"*1000, "\nPrinting from dimReducedparticipantIds", df.shape)
    featureData = pd.read_csv(os.path.join(
        "data/processedData", featureFile), sep="|").groupby("participantId").mean().reset_index()
    personalityData = pd.read_csv(os.path.join(
        "./data/processedData", personalityFile), sep="|")
    # print("featureData:", featureData.shape, "personalityData", personalityData.shape)
    # print("featureData['participantId']", featureData["participantId"].tolist())
    # personalityData = personalityData[personalityData['participantId'].isin(featureData["participantId"].tolist())]
    # personalityData.to_csv(os.path.join("data/processedData", personalityFile), sep="|",  header=True, index=False)

    columns = featureData.columns.values[2:]  # get all the feature columns
    width = None
    height = None

    if request.method == 'POST':
        content = request.get_json()
        width = content['width']
        height = content['height']

        if len(columns) > 1:  # in case of feature columns are selected in dropdown, consider only those
            columns = content['featureColumns']
            message = "status1:file updated"
        else:
            message = "status2:single column"
    else:
        message = "status3:file reset"

    x, y = getTSNE(featureData, columns, width, height)  # dim reduction
    # x, y = getPCA(featureData, columns, width, height)     #dim reduction
    # clusters = getClusters(featureData, columns, clusteringMethod="spectral")    #spectralClustering
    # clusters = getClusters(featureData, columns, clusteringMethod="kmeans")    #k-means clustering
    personalityData["x"], personalityData["y"] = x, y
    # personalityData["clusters"] = clusters

    personalityData.to_csv(os.path.join(
        "data/processedData", personalityFile), sep="|", index=False, header=True)
    return jsonify(message)


@app.route('/fetchPersonalityScores', methods=['GET'])
def fetchPersonalityScores():
    """
    Return Data for Chart1: Personality scores that are used to make glyphs
    """
    if request.method == 'GET':
        print("Request recieved for fetching Personality scores")
        data = pd.read_csv(os.path.join(
            "data/processedData", personalityFile), sep="|")
        print(data.columns)

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/filterparticipantIds', methods=['POST'])
def filterparticipantIdsDummy():
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
        print("request recieved", content)  # print statement

        strt = time.time()
        filenames = {"brt": brightnessFile,
                     "acc": accelerometerFile, "gyro": gyroscopeFile}
        data = pd.DataFrame()
        for attr, checkState in attributes.items():
            if checkState:
                df = pd.read_csv(os.path.join(
                    "data/processedData", filenames[attr]), sep="|")
                # .sample(frac=0.001)
                df = df[df["participantId"] == participantId]

                # Randomly removing data for night time, this step wont be necessary once the proper synthetic data is made
                for i in range(ceil(df.shape[0]/1440)):
                    x = np.random.randint(0, 3*60)
                    sleepDur = np.random.randint(6, 9)
                    startindex = i * 1440 + x
                    df.iloc[startindex:(startindex+sleepDur*60), -1] = 0
                    # data = data[data.iloc[:,-1] != 0]

                data = pd.concat([data, df])

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredparticipantIds.csv"
        resp.headers["Content-Type"] = "text/csv"
        print(time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} participantId:{participantId}")

    else:
        return jsonify("no post requests")


@app.route('/filterparticipantIdsNew', methods=['POST'])
def filterparticipantIdsNew():
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

        print("request recieved for", participantId,
              attributes)  # print statement

        strt = time.time()
        filenames = {"brt": brightnessFile, "acc": accelerometerFile,
                     "gyro": gyroscopeFile, "lck": lockStateFile}
        data = pd.DataFrame()
        for attr, checkState in attributes.items():
            print("attr:", attr, "checkState:", checkState)
            if checkState:
                df = pd.read_csv(os.path.join(
                    "data/processedData", filenames[attr]), sep="|")
                # .sample(frac=0.001)
                df = df[df["participantId"] == participantId]
                dfImputed = pd.DataFrame()

                # addind -1 values for minutesOfTheDay where data is not present
                # creating df with all mins to impute missing values
                mins = [i for i in range(0, 1440)]
                allMinutes = pd.DataFrame({"minuteOfTheDay": mins})

                for date in df.date.unique():
                    dfDate = df[df.date == date].copy()
                    dfDate = pd.merge(dfDate, allMinutes,
                                      how="right", on="minuteOfTheDay")

                # df_call["MinuteOfTheDay"] = (df_call.timestamp - df_call.timestamp.dt.floor('d')).astype('timedelta64[m]')

                    if attr == "lck":
                        dfDate.loc[0, attr] = 0
                    else:
                        # dfDate.loc[0,attr]=0
                        dfDate[attr].fillna(0, inplace=True)
                    dfDate.ffill(inplace=True)
                    dfDate.bfill(inplace=True)
                    dfImputed = pd.concat([dfImputed, dfDate], axis=0)

                    # if attr=="brt":
                    #     temp = pd.read_csv(os.path.join("data", filenames['lck']), sep="|")
                    #     temp = temp[(temp["participantId"]==participantId) & (temp.date == date)].copy()
                    #     temp = temp.merge(dfImputed, on=["participantId", "device", "date", "minuteOfTheDay"], how="inner")
                    #     dfImputed = temp[temp.lck==1]
                    #     dfImputed.drop("lck", axis=1, inplace=True)

                data = pd.concat([data, dfImputed])
                print("data.date.unique()", data.date.nunique())

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredparticipantIds.csv"
        resp.headers["Content-Type"] = "text/csv"
        print("Execution Time", time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} participantId:{participantId}")

    else:
        return jsonify("no post requests")


@app.route('/fetchAggFeatures', methods=['POST'])
def fetchAggFeatures():
    """
    Returns Data for Chart3: Parallel cordinate chart to visualize extracted features
    """
    if request.method == 'POST':
        content = request.get_json()
        # filename = content['filename']
        participantId = content['participantId']

        print(f"Request recieved for fetching Aggregated feature data: selected_participant:{participantId}")
        data = pd.read_csv(os.path.join(
            "data/processedData", featureFile), sep="|")
        # Aggregating based on participantId
        data = data.groupby("participantId").mean().reset_index()
        # getting cluster id for participantIds form personality file
        df = pd.read_csv(os.path.join("data/processedData", personalityFile),
                        sep="|").loc[:, ["participantId", "clusters"]]
        data = pd.merge(data, df, how="left")

        # rearranging data such that selected participant data is always at the last
        # this helps in the visualization of parallel cord chart
        idx = df.index.tolist()
        index_to_shift = data.index[data["participantId"] == participantId].tolist()[0]
        idx.pop(index_to_shift)
        data = data.reindex(idx + [index_to_shift])

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/fetchIndividualFeatures', methods=['POST'])
def fetchIndividualFeatures():
    """
    Returns Data for Chart4: Parallel cordinate chart to visualize extracted features - This will return the feature of single participantId.
    """
    if request.method == 'POST':
        content = request.get_json()
        # filename = content['filename']
        participantId = content['participantId']

        print("Request recieved for fetching individual feature data")
        data = pd.read_csv(os.path.join(
            "data/processedData", featureFile), sep="|")
        # Fetching data for selected participantId
        data = data[data["participantId"] == participantId].copy()

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=individualFeatureData.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/dataTable', methods=['GET', 'POST'])
def dataTable():
    if request.method == 'GET':
        df = pd.read_csv(os.path.join(
            "data/processedData", featureFile), sep="|")
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
        df = pd.read_csv(os.path.join(
            "data/processedData", featureFile), sep="|")
        df.drop(df.index, inplace=True)
        df = pd.DataFrame(data1[1:], columns=df.columns)
        os.remove(os.path.join("data/processedData", featureFile))
        df.to_csv(os.path.join("data/processedData", featureFile),
                  sep="|", index=False, header=True)

        print("File updated")

        message = "Feature file updated by the user"
        return jsonify(message)
        # test code ends

# Get a list of distinct participants for the search bar
@app.route('/getParticipantIds', methods=['GET'])
def getParticipantIds():
    df = pd.read_csv(os.path.join("data/processedData", personalityFile), sep="|")
    participantIds = df["participantId"].unique().tolist()
    return jsonify(participantIds)


# Get a random patritipant that can be used to have a selection when page is refreshed
@app.route('/getRandomparticipantId', methods=['GET'])
def getRandomparticipantId():
    df = pd.read_csv(os.path.join("data/processedData", personalityFile), sep="|")
    sys_random = rand.SystemRandom()
    participantIds = df["participantId"].unique()
    participantId = sys_random.choice(participantIds)
    return jsonify(participantId)


if __name__ == "__main__":
    app.run(port=5003, debug=True)
