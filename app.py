# BackEnd Server
import time
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, make_response
import pandas as pd
import numpy as np
from re import search
from sklearn import cluster

# sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
# from sklearn.feature_selection import SequentialFeatureSelector
# from sklearn.model_selection import train_test_split
# from sklearn.inspection import permutation_importance

from removeOverlap.dgrid import *

# personalityFile = "dummyPersonalityScores"
# featureFile = "dummyFeatureData"
# brightnessFile = "dummyBrightness"
# accelerometer File = "dummyAccelerometer"
# gyroscopeFIle = "dummygyroscope"

personalityFile = "PersonalityScores.csv"
featureFile = "featureData.csv"
featureAggFile = "featureDataAgg.csv"
brightnessFile = "Brightness_processed_ios.csv"
accelerometerFile = "Accelerometer_processed_ios.csv"
gyroscopeFile = "Gyroscope_processed_ios.csv"
lockStateFile = "Lock_state_processed_ios.csv"
noiseFile = "Sleep_Noise_processed_ios.csv"
accelerometerFileAndroid = "Accelerometer_processed_android.csv"
gyroscopeFileAndroid = "Gyroscope_processed_android.csv"
lockStateFileAndroid = "powerState_processed_android.csv"

def DGridRemoveOverlap(dimReduxProjections, width, height, radius):
    # Overlap removal of projections
    x = np.expand_dims(dimReduxProjections[:, 0], axis=1)
    y = np.expand_dims(dimReduxProjections[:, 1], axis=1)
    cords = np.concatenate((x, y), axis=1)
    icon_width = 1.35*(1/(width/(2*radius)))
    icon_height = 1.1*(1/(height/(2*radius)))

    dimReduxProjectionsOverlapRemoved = DGrid(icon_width, icon_height, delta=1).fit_transform(cords)
    resultX = np.round(dimReduxProjectionsOverlapRemoved[:, 0], 3)
    resultY = np.round(dimReduxProjectionsOverlapRemoved[:, 1], 3)
    return resultX, resultY


def getTSNE(df, width, height, radius):
    #TSNE projection
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300, init='random', learning_rate="auto")
    tsneResult = tsne.fit_transform(df)
    tsneResult = np.round(MinMaxScaler().fit_transform(tsneResult), 3)
    tsneX, tsneY = tsneResult[:, 0], tsneResult[:, 1]
    tsneX_overlapRemoved, tsneY_overlapRemoved = DGridRemoveOverlap(tsneResult, width, height, radius)
    return tsneX, tsneY, tsneX_overlapRemoved, tsneY_overlapRemoved


def getPCA(df, width, height, radius):
    #PCA projection
    pca = PCA(n_components=2)
    pcaResult = pca.fit_transform(df)
    pcaResult = np.round(MinMaxScaler().fit_transform(pcaResult), 3)
    pcaX, pcaY = pcaResult[:, 0], pcaResult[:, 1]
    pcaX_overlapRemoved, pcaY_overlapRemoved = DGridRemoveOverlap(pcaResult, width, height, radius)
    return pcaX, pcaY, pcaX_overlapRemoved, pcaY_overlapRemoved


def getClusters(df, columns, classLabel, k):
    # KNN clustering
    X = df.loc[:, columns].copy()
    Y = df.loc[:, classLabel].copy()    #change the column here-use glyph color column for knn
    if classLabel == "age_group":
        mapping_dict = {0:"Youth(15-24)", 1:"Adults(25-64)", 2:"Seniors(65+)"}
        Y.mask(Y == "Youth(15-24)" ,0, inplace=True)
        Y.mask(Y == "Adults(25-64)" ,1, inplace=True)
        Y.mask(Y == "Seniors(65+)" ,2, inplace=True)
        Y = Y.astype('int')
    clusters = []
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, Y)
    clusters = knn.predict(X)
    if classLabel == "age_group":
        clusters = [mapping_dict[x] for x in clusters]
    return clusters


def getImportance(df, columns, classLabel):
    # Feature imporance score is measured by training an XGboost model.
    if not classLabel.isnumeric():
        le = LabelEncoder().fit(df[classLabel].values)
        df["classLabel"] = le.transform(df[classLabel].values)

    X, y = df.loc[:, columns], df.loc[:, "classLabel"]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    X_train, y_train = X, y    #no test set, since all of the instances are needed to calculate the feature importance
    
    xgb_clf = xgb.XGBClassifier()
    xgb_clf.fit(X_train, y_train)
    #feature importance using XGboost model alone
    importanceScore = xgb_clf.feature_importances_

    #Permutation importance for feature evaluation using XGboost classifier. Works better in cases with test data, which is different that train data used for model fitting.
    # importanceScore = permutation_importance(xgb_clf, X_train, y_train).importances_mean

    importanceScore = np.round(importanceScore, 3)
    d = dict(zip(columns, [str(x) for x in importanceScore]))
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))


app = Flask(__name__, static_url_path='', static_folder='')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title="Home", header="Home")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


# Get a list of distinct participants for the search bar
@app.route('/getIds', methods=['GET'])
def getIds():
    featureData = pd.read_csv(os.path.join("data/rawData", featureAggFile))
    ids = featureData["id"].unique().tolist()
    return jsonify(ids)

# Get a list of features based on sequential feature selector
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html
@app.route('/getAutoN', methods=['POST'])
def getAutoN():
    if request.method == 'POST':
        content = request.get_json()
        autoN = int(content["autoN"])
        classLabel = content["classLabel"]
        featureDataAgg = pd.read_csv(os.path.join("data/processedData", featureAggFile))
        featureData = pd.read_csv(os.path.join("data/rawData", featureAggFile))
        columns = [col for col in list(featureData.columns) if col not in ["id", "age", "gender", "label1", "label2", "age_group"]]
        featuresWithImportance = getImportance(featureDataAgg, columns, classLabel)
        Nfeatures = list(featuresWithImportance.keys())[:autoN]
        return jsonify(Nfeatures)


# Get a list of distinct values for classLabel
@app.route('/getClassLabels', methods=['POST'])
def getClassLabels():
    if request.method == 'POST':
        content = request.get_json()
        classLabel = content["classLabel"]
        personalityData = pd.read_csv(os.path.join("data/processedData", featureAggFile))
        if classLabel == "age_group":
            labels = ["Youth(15-24)", "Adults(25-64)", "Seniors(65+)"]
        else:
            labels = sorted(personalityData[classLabel].unique().astype("str").tolist())
        # if classLabel == "age_group":
        #     # bins= [12,18,25,59,200]
        #     # labels = ['1_Teen','2_Adult','3_Mid-Adult','4_Senior-Adult']
        #     bins = [15, 24, 64, 100]
        #     labels = ["Youth(15-24)", "Adults(25-64)", "Seniors(65+)"]
        #     personalityData[classLabel] = pd.cut(personalityData['age'], bins=bins, labels=labels, right=False)
        #     labels = sorted(personalityData[classLabel].unique().tolist())
        # #     # personalityData["age_group"] = LabelEncoder().fit_transform(personalityData["age_group"].values)
        # #     # personalityData["age_group"] = le.transform(personalityData["age_group"].values)
        #     personalityData.to_csv(os.path.join("data/processedData", featureAggFile), index=False, header=True)
        return jsonify(labels)


@app.route('/dimReduceIds', methods=['POST'])
def dimReduceIds():
    # featureData = pd.read_csv(os.path.join("data/processedData", featureFile))
    featureDataAgg = pd.read_csv(os.path.join("data/processedData", featureAggFile))
    featureDataAgg.fillna(0, inplace=True)
    if request.method == 'POST':
        content = request.get_json()
        columns = content["featureColumns"]
        width = content['width']
        height = content['height']
        radius = int(content["radius"])
        k = int(content["k"])
        toggleDimRedux = content["toggleDimRedux"]
        classLabel = content["classLabel"]
        # dim reduction
        # featureDataAgg = featureData.loc[:, ["id"]+columns].groupby(['id'], as_index=False).agg(["mean"]).reset_index()
        # df = featureData.loc[:, ["id"]+columns].groupby(['id'], as_index=False).agg(["mean", "std"]).reset_index()
        # df.drop(["id"], axis=1, inplace=True)
        # df.fillna(0, inplace=True)
        df = featureDataAgg.loc[:,columns]
        if toggleDimRedux == "tsne":
            x, y, x_overlapRemoved, y_overlapRemoved = getTSNE(df, width, height, radius)
        elif toggleDimRedux == "pca":
            x, y, x_overlapRemoved, y_overlapRemoved = getPCA(df, width, height, radius)

        cluster = getClusters(featureDataAgg, columns, classLabel, k)    #KNN clustering
        featureDataAgg["x"], featureDataAgg["y"] = x, y
        featureDataAgg["x_overlapRemoved"], featureDataAgg["y_overlapRemoved"] = x_overlapRemoved, y_overlapRemoved
        featureDataAgg["cluster"] = cluster
        
        featureDataAgg.dropna(axis=1, how='all', inplace=True)
        featureDataAgg.to_csv(os.path.join(
            "data/processedData", featureAggFile), index=False, header=True)
        message = "status1:fileUpdated"
    return jsonify(message)


@app.route('/knnClustering', methods=["POST"])
def knnClustering():
    """
    This function is used to just calculate the k-nearest neighbours of the feature instances
    """
    featureData = pd.read_csv(os.path.join("data/processedData", featureAggFile))
    if request.method == 'POST':
        content = request.get_json()
        columns = content["featureColumns"]
        classLabel = content["classLabel"]
        k = int(content["k"])

        cluster = getClusters(featureData, columns, classLabel, k)    #KNN clustering
        featureData["cluster"] = cluster
        featureData.dropna(axis=1, how='all', inplace=True)
        featureData.to_csv(os.path.join(
            "data/processedData", featureAggFile), index=False, header=True)
        message = "status1:fileUpdated"

    return jsonify(message)


@app.route('/getProjections', methods=['GET'])
def getProjections():
    """
    Return Data for Chart1: Personality scores that are used to make glyphs
    """
    if request.method == 'GET':
        data = pd.read_csv(os.path.join(
            "data/processedData", featureAggFile))
        cols = [col for col in data.columns if col not in ['id', 'age', 'gender', 'label1', 'label2', 'age_group', 'x', 'y', 'x_overlapRemoved', 'y_overlapRemoved', 'cluster']]
        data[cols] = np.round(MinMaxScaler().fit_transform(data[cols]), 3)
        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/filterparticipantIds', methods=['POST'])
def filterparticipantIds():
    """
    Returns Data for Chart2: Radial chart to visualize sleep/awake activity using 
    brightness, accelerometer and gyroscope data
    Real data
    """
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']
        attributes = content["attributes"]

        if search("iPROSITC", id):
            filenames = {"lck": lockStateFile, "noise": noiseFile, "brt": brightnessFile, "acc": accelerometerFile,
                     "gyro": gyroscopeFile}
        elif search("aPROSITC", id):
            filenames = {"lck": lockStateFileAndroid, "noise": None, "brt": None, "acc": accelerometerFileAndroid,
                     "gyro": gyroscopeFileAndroid}

        data = pd.DataFrame()
        for attr, checkState in attributes.items():
            if checkState:
                if filenames[attr] is None:
                    continue
                df = pd.read_csv(os.path.join(
                    "data/rawData", filenames[attr]))
                df = df[df["id"] == id]
                
                dfImputed = pd.DataFrame()
                # addind -1 values for minutesOfTheDay where data is not present
                # creating df with all mins to impute missing values
                mins = [i for i in range(0, 1440)]
                allMinutes = pd.DataFrame({"minuteOfTheDay": mins})

                for date in df.date.unique():
                    dfDate = df[df.date == date].copy()
                    dfDate = pd.merge(dfDate, allMinutes,
                                      how="right", on="minuteOfTheDay")

                    if attr == "lck":
                        dfDate.loc[0, attr] = 0
                    else:
                        # dfDate.loc[0,attr]=0
                        dfDate[attr].fillna(0, inplace=True)

                    dfDate.ffill(inplace=True)
                    dfDate.bfill(inplace=True)
                    dfImputed = pd.concat([dfImputed, dfDate], axis=0)

                    # if attr=="brt":
                    #     temp = pd.read_csv(os.path.join("data", filenames['lck']))
                    #     temp = temp[(temp["id"]==id) & (temp.date == date)].copy()
                    #     temp = temp.merge(dfImputed, on=["id", "device", "date", "minuteOfTheDay"], how="inner")
                    #     dfImputed = temp[temp.lck==1]
                    #     dfImputed.drop("lck", axis=1, inplace=True)

                data = pd.concat([data, dfImputed])
        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredparticipantIds.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
        # return jsonify(f"post works filename:{filename} id:{id}")

    else:
        return jsonify("no post requests")


@app.route('/getAggFeatures', methods=['POST'])
def getAggFeatures():
    """
    Returns Data for Chart3: Parallel cordinate chart to visualize extracted features
    """
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']

        featureData = pd.read_csv(os.path.join(
            "data/processedData", featureAggFile))
        
        # rearranging data such that selected participant data is always at the last
        # this helps in the visualization of parallel cord chart
        # idx = featureData.index.tolist()
        # index_to_shift = featureData.index[featureData["id"] == id].tolist()[0]
        # idx.pop(index_to_shift)
        # featureData = featureData.reindex(idx + [index_to_shift])

        resp = make_response(featureData.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/getIndividualFeatures', methods=['POST'])
def getIndividualFeatures():
    """
    Returns Data for Chart4: Parallel cordinate chart to visualize extracted features - This will return the feature of single id.
    """
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']

        featureData = pd.read_csv(os.path.join("data/processedData", featureFile))
        # Fetching data for selected id
        featureData = featureData[featureData["id"] == id].copy()

        resp = make_response(featureData.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=individualFeatureData.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/dataTable', methods=['GET', 'POST'])
def dataTable():
    if request.method == 'GET':
        df = pd.read_csv(os.path.join(
            "data/processedData", featureFile))
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
            "data/processedData", featureFile))
        df.drop(df.index, inplace=True)
        df = pd.DataFrame(data1[1:], columns=df.columns)
        os.remove(os.path.join("data/processedData", featureFile))
        df.to_csv(os.path.join("data/processedData", featureFile),
                  sep="|", index=False, header=True)

        message = "Feature file updated by the user"
        return jsonify(message)
        # test code ends


# Sort features based on their feature importance: 
# Permutation Based Feature Importance using XGBoost is used to calculate feature importance
# https://mljar.com/blog/feature-importance-xgboost/
# https://explained.ai/rf-importance/
@app.route('/getFeatureImportance', methods=['POST'])
def getFeatureImportance():
    """
    Returns a list of features sorted based on their importance to classify the dataset. 
    This will be used to sort features in parallel cord chart
    """
    if request.method == 'POST':
        content = request.get_json()
        columns = content["featureColumns"]
        classLabel = content["classLabel"]

        featureData = pd.read_csv(os.path.join("data/processedData", featureAggFile))
        if len(columns) <= 1:
            columns = [col for col in list(featureData.columns) if col not in ["id", "age", "gender", "label1", "label2", "age_group"]]
        featuresWithImportance = getImportance(featureData, columns, classLabel)
        return jsonify(featuresWithImportance)


if __name__ == "__main__":
    app.run(port=5011, debug=True)
    #age_groups ["Millennial", "GenX", "Boomer", "Silent"] [(18-34), (35-50), (51-69), (70-87)]