"""

"""
from imports import *
from iosExtractScreenFeatures import *
from iosExtractCallingFeatures import *
# from iosExtractMobilityFeatures import *
from iosExtractSleepFeatures import *

def getFeatures(config):
    if (list(config.keys()) != ["path", "features", "values"] or len(config["path"]) != 2  or len(config["features"]) != 4 or len(config["values"]) != 4):
        print('Please enter config in below format/n {"features":["screen", "calling", "mobility", "sleep"], "values":"1111"}')
    else:
        dataPath = config["path"][0]
        featurePath = config["path"][1]

        if (config["features"][0] == "screen" and config["values"][0] == "1"):
            getIosScreenFeatures(dataPath, featurePath)
        if (config["features"][1] == "calling" and config["values"][1] == "1"):
            getIosCallingFeatures(dataPath, featurePath)
        if (config["features"][2] == "sleep" and config["values"][2] == "1"):
            getIosSleepFeatures(dataPath, featurePath)
        if (config["features"][3] == "mobility" and config["values"][3] == "1"):
            print("GPS data will not be processed at this point in time")
            # getIosMobilityFeatures(dataPath, featurePath)


def combineFeatures(featurePath, featureFiles, finalFeatureFilename):
    """
    method to combine all the features based on data and patricipant
    """
    # Filtered participants from another notebook : participants with more that 14days of data
    filteredParticipants = []

    # concatinating files with same sensor group
    df_list = []
    for sensorGroup in featureFiles:
        df = pd.read_csv(os.path.join(featurePath, sensorGroup))
        # if len(sensorGroup) == 0:
        #     continue
        # df1 = pd.read_csv(os.path.join(featurePath, sensorGroup[0]))
        # df2 = pd.read_csv(os.path.join(featurePath, sensorGroup[1]))
        # df = pd.concat([df1, df2], ignore_index=True)
        # for file in sensorGroup[2:]:
        #     next_df = pd.read_csv(os.path.join(featurePath, file))
        #     df = pd.concat([df, next_df], ignore_index=True)
        df_list.append(df)
    
    # merging all the feature files into a single file
    if len(df_list) == 0:
        sys.exit("no feature files to merge")
    df1 = df_list[0]
    df2 = df_list[1]
    featureData = pd.merge(df1, df2, on=["participantId", "date"], how="outer")
    
    for next_featureFile in df_list[2:]:
        featureData = pd.merge(featureData, next_featureFile, on=["participantId", "date"], how="inner")

    # keep only filtered participants
    if len(filteredParticipantIds)!=0:
        featureData = featureData[featureData["participantId"].isin(filteredParticipants)].reset_index(drop=True)
    featureData.to_csv(os.path.join(featurePath, "..", finalFeatureFilename), header=True, index=False)


if __name__ == "__main__":
    """
    config["values"] will be used to control the features that will be extracted from the raw data, '1' means True and anything else will be Flase.
    """
    # config
    dataPath1 = "../../data/allNoLoc"
    # dataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"
    finalFeatureFilename = "featureData.csv"

    # create output directory if not exits
    isExist = os.path.exists(featurePath)
    if not isExist:
        os.makedirs(featurePath)

    config1 = {"path":[dataPath1, featurePath], "features":["screen", "calling", "sleep", "mobility"], "values":"0010"}
    # config2 = {"path":[dataPath2, featurePath], "features":["screen", "calling", "sleep", "mobility"], "values":"1110"}

    # strTime = time.time()
    # getFeatures(config1)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}\n")

    # strTime = time.time()
    # getFeatures(config2)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}\n")

    # idividual feature files that needs to be combined to get a final output feature file that's needed by the Dashboard
    allFiles = os.listdir(featurePath)
    screenFeatureFiles = [file for file in allFiles if "ios_screen_features_" in file]
    callFeatureFiles = [file for file in allFiles if "ios_call_features_" in file]
    sleepFeatureFiles = [file for file in allFiles if "ios_sleep_features_" in file]
    # mobilityFeatureFiles = [file for file in allFiles if "ios_mobility_features_" in file]
    mobilityFeatureFiles = []   #empty since I wont be analysisng GPS data, use above line if GPS data is neeeded
    
    featureFiles = screenFeatureFiles + callFeatureFiles + sleepFeatureFiles + mobilityFeatureFiles
    combineFeatures(featurePath, featureFiles, finalFeatureFilename)
