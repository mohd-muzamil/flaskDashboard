# BackEnd Server
from datetime import time
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, make_response
import pandas as pd
import numpy as np

# sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import LabelEncoder

from removeOverlap.dgrid import *

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


def DGridRemoveOverlap(dimReduxProjections, width, height, radius):
    # Overlap removal of projections
    x = np.expand_dims(dimReduxProjections[:, 0], axis=1)
    y = np.expand_dims(dimReduxProjections[:, 1], axis=1)
    cords = np.concatenate((x, y), axis=1)
    icon_width = 1/(width/(2*radius))
    icon_height = 1/(height/(2*radius))

    dimReduxProjectionsOverlapRemoved = DGrid(icon_width, icon_height, delta=1).fit_transform(cords)
    resultX = np.round(dimReduxProjectionsOverlapRemoved[:, 0], 3)
    resultY = np.round(dimReduxProjectionsOverlapRemoved[:, 1], 3)
    return resultX, resultY


def getTSNE(df, columns, width, height, radius):
    #TSNE projection
    tsne = TSNE(n_components=2, verbose=1,
                perplexity=40, n_iter=300, init='random', learning_rate="auto")
    tsneResult = tsne.fit_transform(df.loc[:, columns])
    tsneResult = np.round(MinMaxScaler().fit_transform(tsneResult), 3)
    tsneX, tsneY = tsneResult[:, 0], tsneResult[:, 1]
    tsneX_overlapRemoved, tsneY_overlapRemoved = DGridRemoveOverlap(tsneResult, width, height, radius)
    return tsneX, tsneY, tsneX_overlapRemoved, tsneY_overlapRemoved


def getPCA(df, columns, width, height, radius):
    #PCA projection
    pca = PCA(n_components=2)
    pcaResult = pca.fit_transform(df.loc[:, columns])
    pcaResult = np.round(MinMaxScaler().fit_transform(pcaResult), 3)
    pcaX, pcaY = pcaResult[:, 0], pcaResult[:, 1]
    pcaX_overlapRemoved, pcaY_overlapRemoved = DGridRemoveOverlap(pcaResult, width, height, radius)
    return pcaX, pcaY, pcaX_overlapRemoved, pcaY_overlapRemoved


def getClusters(df, columns, label, k):
    # KNN clustering
    X = df.loc[:, columns]
    Y = df.loc[:, label]    #change the column here-use glyph color column for knn
    clusters = []
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, Y)
    clusters = knn.predict(X)
    return clusters


def getFeatureImportance(df, columns, label):
    # Feature imporance score is measured by training an XGboost model.
    if not label.isnumeric():
        le = LabelEncoder().fit(df[label].values)
        df["label"] = le.transform(df[label].values)
    elif df[label].unique()>10:
        df[label] = pd.cut(df[label], q=4, labels=[1, 2, 3, 4])

    X, y = df.loc[:, columns], df.loc[:, label]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    X_train, y_train = X, y     #no test set, since all of the instances are needed to calculate the feature importance
    
    xgb_clf = xgb.XGBClassifier()
    xgb_clf.fit(X_train, y_train)
    #feature importance using XGboost model alone
    importanceScore = xgb_clf.feature_importances_

    #Permutation importance for feature evaluation using XGboost classifier. Works better in cases with test data, which is different that train data used for model fitting.
    # importanceScore = permutation_importance(xgb_clf, X_train, y_train).importances_mean

    importanceScore = np.round(importanceScore, 3)
    return dict(sorted(zip(columns, [str(x) for x in importanceScore])))


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
    featureData = pd.read_csv(os.path.join("data/rawData", featureFile))
    ids = featureData["id"].unique().tolist()
    return jsonify(ids)


@app.route('/dimReduceIds', methods=['POST'])
def dimReduceIds():
    featureData = pd.read_csv(os.path.join("data/rawData", featureFile)).groupby("id").mean().reset_index()
    personalityData = pd.read_csv(os.path.join("data/rawData", personalityFile))
    combinedData = featureData.merge(personalityData, how='inner', on='id')
    print("______________\n"*10, featureData.shape, personalityData.shape, combinedData.shape, combinedData.columns)
    
    if request.method == 'POST':
        content = request.get_json()
        print("$$$$$$", content)
        columns = content["featureColumns"]
        width = content['width']
        height = content['height']
        radius = int(content["radius"])
        k = int(content["k"])
        toggleDimRedux = content["toggleDimRedux"]
        label = content["label"]

        # print("_"*100, "\n", columns, featureData[columns].head(5))
        # dim reduction
        if toggleDimRedux == "tsne":
            x, y, x_overlapRemoved, y_overlapRemoved = getTSNE(combinedData, columns, width, height, radius)
        elif toggleDimRedux == "pca":
            x, y, x_overlapRemoved, y_overlapRemoved = getPCA(combinedData, columns, width, height, radius)
        
        cluster = getClusters(combinedData, columns, label, k)    #KNN clustering
        personalityData["x"], personalityData["y"] = x, y
        personalityData["x_overlapRemoved"], personalityData["y_overlapRemoved"] = x_overlapRemoved, y_overlapRemoved
        personalityData["cluster"] = cluster
        
        personalityData.dropna(axis=1, how='all', inplace=True)
        personalityData.to_csv(os.path.join(
            "data/processedData", personalityFile), index=False, header=True)
        message = "status1:fileUpdated"
    return jsonify(message)


@app.route('/knnClustering', methods=["POST"])
def knnClustering():
    """
    This function is used to just calculate the k-nearest neighbours of the feature instances
    """
    featureData = pd.read_csv(os.path.join("data/processedData", featureFile))
    if request.method == 'POST':
        content = request.get_json()
        columns = content["featureColumns"]
        k = int(content["k"])

        cluster = getClusters(featureData, columns, k)    #KNN clustering
        featureData["cluster"] = cluster
        featureData.dropna(axis=1, how='all', inplace=True)
        featureData.to_csv(os.path.join(
            "data/processedData", featureFile), index=False, header=True)
        message = "status1:fileUpdated"

    return jsonify(message)


@app.route('/getProjections', methods=['GET'])
def fetchProjections():
    """
    Return Data for Chart1: Personality scores that are used to make glyphs
    """
    if request.method == 'GET':
        data = pd.read_csv(os.path.join(
            "data/processedData", personalityFile))

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
        id = content['id']
        attributes = content["attributes"]

        strt = time.time()
        filenames = {"brt": brightnessFile,
                     "acc": accelerometerFile, "gyro": gyroscopeFile}
        data = pd.DataFrame()
        for attr, checkState in attributes.items():
            if checkState:
                df = pd.read_csv(os.path.join(
                    "data/processedData", filenames[attr]))
                # .sample(frac=0.001)
                df = df[df["id"] == id]

                # Randomly removing data for night time, this step wont be necessary once the proper synthetic data is made
                for i in range(np.ceil(df.shape[0]/1440)):
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
        # return jsonify(f"post works filename:{filename} id:{id}")

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
        id = content['id']
        attributes = content["attributes"]

        strt = time.time()
        filenames = {"brt": brightnessFile, "acc": accelerometerFile,
                     "gyro": gyroscopeFile, "lck": lockStateFile}
        data = pd.DataFrame()
        for attr, checkState in attributes.items():
            print("attr:", attr, "checkState:", checkState)
            if checkState:
                df = pd.read_csv(os.path.join(
                    "data/processedData", filenames[attr]))
                # .sample(frac=0.001)
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
                    #     temp = pd.read_csv(os.path.join("data", filenames['lck']))
                    #     temp = temp[(temp["id"]==id) & (temp.date == date)].copy()
                    #     temp = temp.merge(dfImputed, on=["id", "device", "date", "minuteOfTheDay"], how="inner")
                    #     dfImputed = temp[temp.lck==1]
                    #     dfImputed.drop("lck", axis=1, inplace=True)

                data = pd.concat([data, dfImputed])
                print("data.date.unique()", data.date.nunique())

        resp = make_response(data.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=filteredparticipantIds.csv"
        resp.headers["Content-Type"] = "text/csv"
        print("Execution Time", time.time()-strt)
        return resp
        # return jsonify(f"post works filename:{filename} id:{id}")

    else:
        return jsonify("no post requests")


@app.route('/fetchAggFeatures', methods=['POST'])
def fetchAggFeatures():
    """
    Returns Data for Chart3: Parallel cordinate chart to visualize extracted features
    """
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']

        featureData = pd.read_csv(os.path.join(
            "data/processedData", featureFile))
        # Aggregating based on id
        featureData = featureData.groupby("id").mean().reset_index()
        # getting cluster id for ids form personality file
        df = pd.read_csv(os.path.join("data/processedData", personalityFile),
                        sep="|").loc[:, ["id", "clusters"]]
        featureData = pd.merge(featureData, df, how="left")

        # rearranging data such that selected participant data is always at the last
        # this helps in the visualization of parallel cord chart
        idx = df.index.tolist()
        index_to_shift = featureData.index[featureData["id"] == id].tolist()[0]
        idx.pop(index_to_shift)
        featureData = featureData.reindex(idx + [index_to_shift])

        resp = make_response(featureData.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=personalityScores.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route('/fetchIndividualFeatures', methods=['POST'])
def fetchIndividualFeatures():
    """
    Returns Data for Chart4: Parallel cordinate chart to visualize extracted features - This will return the feature of single id.
    """
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']

        featureData = pd.read_csv(os.path.join(
            "data/processedData", featureFile))
        # Fetching data for selected id
        featureData = featureData[featureData["id"] == id].copy()

        resp = make_response(data.to_csv(index=False))
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
def featureImportance():
    """
    Returns a list of features sorted based on their importance to classify the dataset. 
    This will be used to sort features in parallel cord chart
    """
    if request.method == 'POST':
        content = request.get_json()
        columns = content["featureColumns"]

        featureData = pd.read_csv(os.path.join("data/rawData", featureFile))
        if len(columns)<=1:
            columns = [col for col in list(featureData.columns) if col not in ["id", "gender"]]
        featuresWithImportance = getFeatureImportance(featureData, columns)
        return jsonify(featuresWithImportance)


if __name__ == "__main__":
    app.run(port=5008, debug=True)
    #age_groups ["Millennial", "GenX", "Boomer", "Silent"] [(18-34), (35-50), (51-69), (70-87)]