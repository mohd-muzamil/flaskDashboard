from unicodedata import combining
from imports import *
from iosExtractScreenFeatures import *
from iosExtractCallingFeatures import *
from iosExtractMobilityFeatures import *
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
        if (config["features"][2] == "mobility" and config["values"][2] == "1"):
            getIosMobilityFeatures(dataPath, featurePath)
        if (config["features"][3] == "sleep" and config["values"][3] == "1"):
            getIosSleepFeatures(dataPath, featurePath)


def combineFeatures(featurePath):
    """
    method to combine all the features based on data and patricipant
    """
    pass

if __name__ == "__main__":
    """
    config["values"] will be used to control the features that will be extracted from the raw data, '1' means true and anythin else will be flase.
    """
    dataPath1 = "/csv/backup_frigg1"
    dataPath2 = "/csv/backup"
    featurePath = "/csv/features"

    config1 = {"path":[dataPath1, featurePath], "features":["screen", "calling", "mobility", "sleep"], "values":"0100"}
    # config2 = {"path":[dataPath2, featurePath], "features":["screen", "calling", "mobility", "sleep"], "values":"1111"}

    strTime = time.time()
    getFeatures(config1)
    # combineFeatures(featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}")

    # strTime = time.time()
    # getFeatures(config2)
    # combineFeatures(featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}")``
