"""
#################################################################################################################
Script for agregatting raw sensor data over 1-minute periods for visualizating on Radial-time-chart
#################################################################################################################
"""
import pandas as pd
import os
import sys
from pathlib import Path
import numpy as np
from datetime import datetime
pd.set_option('display.max_rows', None)
from tqdm import tqdm
tqdm.pandas()
from time import time

# Filtered participantIds from another notebook. Only data from these will be analysed
filteredParticipantIds = []
timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
logFile = f"log_preprocessing_radialChartData_{timestamp}.txt"


def remove_file(filePath, filename):
    """
    function to remove the output file if it already exists
    """
    file = os.path.join(filePath, filename)
    if os.path.exists(file):
        os.remove(file)


def process_accelerometer_android_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Accelerometer Android
    """
    print(f"Processing Accelerometer Android data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    accelerometerInputFilename = "accelerometer_m_s2__x_y_z_android.csv"
    accelerometerOutputFilename = "Accelerometer_processed_android.csv"
    if removeOutputFileFlag:
        remove_file(outputDataPath, accelerometerOutputFilename)        # removing the output file if they already exist
    
    header_list = ["id", "participantId", "attribute", "accX", "accY", "accZ", "timestamp", "uploadtimestamp", "id1"]
    accelerometer = pd.read_csv(os.path.join(inputDataPath, accelerometerInputFilename), sep='|', header=None, names=header_list)
    print(f"Raw file shape: {accelerometer.shape}", file=open(os.path.join(outputDataPath, logFile), "a"))

    # drop unecessary columns
    accelerometer.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        accelerometer = accelerometer[accelerometer["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=True)
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"]).dt.tz_convert(tz='America/Halifax')
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=False)

    # add a date column
    accelerometer["date"] = accelerometer["timestamp"].dt.date

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = accelerometer["participantId"].unique()
    for participantId in (participantIds):
        accelerometer_participantId = accelerometer[accelerometer["participantId"] == participantId].copy()
        dates = accelerometer_participantId["date"].unique()
        for date in dates:
            try:
                accelerometer_participantId_date = accelerometer_participantId[accelerometer_participantId["date"] == date].copy()

                # drop duplicates
                accelerometer_participantId_date.drop_duplicates(keep="last", inplace=True)

                #sort values
                accelerometer_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                accelerometer_participantId_date["minuteOfTheDay"] = (accelerometer_participantId_date["timestamp"] - accelerometer_participantId_date["timestamp"].dt.floor('d')).astype('timedelta64[m]').astype('int')
                accelerometer_participantId_date["acc"] = np.sqrt(accelerometer_participantId_date.accX**2 + accelerometer_participantId_date.accY**2 + accelerometer_participantId_date.accZ**2)

                # drop timestamp column
                accelerometer_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #drop axial accelerometer columns
                accelerometer_participantId_date.drop(["accX", "accY", "accZ"], axis=1, inplace=True)

                #Aggregate the data over a period of 1minute
                accelerometerAgg = accelerometer_participantId_date.groupby(["participantId", "date", "minuteOfTheDay"])["acc"].agg("mean").reset_index()
                accelerometerAgg["acc"] = round(accelerometerAgg["acc"], 2)
                
                rows += accelerometerAgg.shape[0]
                cols = accelerometerAgg.shape[1]
                # append the data to file
                accelerometerAgg.to_csv(os.path.join(outputDataPath, accelerometerOutputFilename), mode='a', sep="|", header=headerWriteFlag, index=False)
                headerWriteFlag = False
            
            except:
                print(f"An exception occurred on Accelerometer data for {participantId} {date}", file=open(os.path.join(outputDataPath, logFile), "a"))

    print(f"Processed file shape: ({rows},{cols})", file=open(os.path.join(outputDataPath, logFile), "a"))
    print("Accelerometer completed", file=open(os.path.join(outputDataPath, logFile), "a"))


def process_gyroscope_android_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Gyroscope Android
    """
    print(f"Processing Gyroscope Android data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    gyroscopeInputFilename = "gyroscope_rad_s__x_y_z_android.csv"
    gyroscopeOutputFilename = "Gyroscope_processed_android.csv"
    if removeOutputFileFlag:
        remove_file(outputDataPath, gyroscopeOutputFilename)        # removing the output file if they already exist

    header_list = ["id", "participantId", "attribute", "gyroX", "gyroY", "gyroZ", "timestamp", "uploadtimestamp", "id1"]
    gyroscope = pd.read_csv(os.path.join(inputDataPath, gyroscopeInputFilename), sep='|', header=None, names=header_list)
    print(f"Raw file shape: {gyroscope.shape}", file=open(os.path.join(outputDataPath, logFile), "a"))

    # drop unecessary columns
    gyroscope.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        gyroscope = gyroscope[gyroscope["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=True)
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"]).dt.tz_convert(tz='America/Halifax')
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=False)

    # add a date column
    gyroscope["date"] = gyroscope["timestamp"].dt.date

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = gyroscope["participantId"].unique()
    for participantId in (participantIds):
        gyroscope_participantId = gyroscope[gyroscope["participantId"] == participantId].copy()
        dates = gyroscope_participantId["date"].unique()
        for date in dates:
            # try:
                gyroscope_participantId_date = gyroscope_participantId[gyroscope_participantId["date"] == date].copy()

                # drop duplicates
                gyroscope_participantId_date.drop_duplicates(keep="last", inplace=True)

                #sort values
                gyroscope_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                gyroscope_participantId_date["minuteOfTheDay"] = (gyroscope_participantId_date["timestamp"] - gyroscope_participantId_date["timestamp"].dt.floor('d')).astype('timedelta64[m]').astype('int')
                gyroscope_participantId_date["gyro"] = np.sqrt(gyroscope_participantId_date["gyroX"]**2 + gyroscope_participantId_date["gyroY"]**2 + gyroscope_participantId_date["gyroZ"]**2)

                # drop timestamp column
                gyroscope_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #drop axial gyroscope columns
                gyroscope_participantId_date.drop(["gyroX", "gyroY", "gyroZ"], axis=1, inplace=True)

                #Aggregate the data over a period of 1minute
                gyroscopeAgg = gyroscope_participantId_date.groupby(["participantId", "date", "minuteOfTheDay"])["gyro"].agg("mean").reset_index()
                gyroscopeAgg["gyro"] = round(gyroscopeAgg["gyro"], 2)
                
                rows += gyroscopeAgg.shape[0]
                cols = gyroscopeAgg.shape[1]
                # append the data to file
                gyroscopeAgg.to_csv(os.path.join(outputDataPath, gyroscopeOutputFilename), mode='a', sep="|", header=headerWriteFlag, index=False)
                headerWriteFlag = False

            # except:
                # print(f"An exception occurred on Gyroscope data for {participantId} {date}", file=open(os.path.join(outputDataPath, logFile), "a"))

    print(f"Processed file shape: ({rows},{cols})", file=open(os.path.join(outputDataPath, logFile), "a"))
    print("Gyroscope completed", file=open(os.path.join(outputDataPath, logFile), "a"))


def measure_processing_time(method, inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    # try:
        strTime = time()
        method(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag)
        endTime = time()
        print(f"run time: {round((endTime - strTime)/60, 4)} mins\n", file=open(os.path.join(outputDataPath, logFile), "a"))
    # except:
        # print(f"An exception occurred at file level", file=open(os.path.join(outputDataPath, logFile), "a"))
    

if __name__ == "__main__":
    # config
    inputDataPath1 = "../data/allNoLoc"
    # inputDataPath2 = "/csv/backup"
    outputDataPath = Path("../data/rawData")

    removeOutputFileFlag = None     #flag used to delete a file if it already exists
    headerWriteFlag = None          #flag used to write header row into the output file

    totalstrTime = time()
    print("Start Time: " + datetime.now().strftime("%Y:%m:%d %I:%M:%S%p") + "\n", file=open(os.path.join(outputDataPath, logFile), "a"))

    # Accelerometer data
    measure_processing_time(process_accelerometer_android_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)

    # Gyroscope data
    measure_processing_time(process_gyroscope_android_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)

    totalendTime = time()
    print("End Time: " + datetime.now().strftime("%Y:%m:%d %I:%M:%S%p"), file=open(os.path.join(outputDataPath, logFile), "a"))
    print(f"Total run time: {round((totalendTime - totalstrTime)/60, 4)} mins", file=open(os.path.join(outputDataPath, logFile), "a"))