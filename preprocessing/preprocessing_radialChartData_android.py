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
filteredParticipantIds = ['aPROSITC0060','aPROSITC0064','aPROSITC00D','aPROSITC00M','aPROSITC0103','aPROSITC0107','aPROSITC0116','aPROSITC0118','aPROSITC0119','aPROSITC0128','aPROSITC0130','aPROSITC0131','aPROSITC0134','aPROSITC0144','aPROSITC0175','aPROSITC0188','aPROSITC0200','aPROSITC0211','aPROSITC0229','aPROSITC0235','aPROSITC0237','aPROSITC0252','aPROSITC0260','aPROSITC0275','aPROSITC0279','aPROSITC0290','aPROSITC0295','aPROSITC0301','aPROSITC0303','aPROSITC0310','aPROSITC0326','aPROSITC0357','aPROSITC0376','aPROSITC0379','aPROSITC0398','aPROSITC0414','aPROSITC0416','aPROSITC0433','aPROSITC0436','aPROSITC0437','aPROSITC0457','aPROSITC0483','aPROSITC0497','aPROSITC0645','aPROSITC0739','aPROSITC0753','aPROSITC0774','aPROSITC0805','aPROSITC0838','aPROSITC0874','aPROSITC1063','aPROSITC1065','aPROSITC1069','aPROSITC1134','aPROSITC1147','aPROSITC1149','aPROSITC1154','aPROSITC1155','aPROSITC1156','aPROSITC1165','aPROSITC1170','aPROSITC1171','aPROSITC1172','aPROSITC1175','aPROSITC1182','aPROSITC1201','aPROSITC1204','aPROSITC1205','aPROSITC1208','aPROSITC1215','aPROSITC1226','aPROSITC1230','aPROSITC1233','aPROSITC1241','aPROSITC1242','aPROSITC1255','aPROSITC1271','aPROSITC1273','aPROSITC1277','aPROSITC1283','aPROSITC1302','aPROSITC1303','aPROSITC1306','aPROSITC1309','aPROSITC1312','aPROSITC1315','aPROSITC1322','aPROSITC1337','aPROSITC1349','aPROSITC1363','aPROSITC1368','aPROSITC1374','aPROSITC1378','aPROSITC1381','aPROSITC1387','aPROSITC1388','aPROSITC1392','aPROSITC1399','aPROSITC1402','aPROSITC1403','aPROSITC1419','aPROSITC1423','aPROSITC1425','aPROSITC1429','aPROSITC1430','aPROSITC1431','aPROSITC1433','aPROSITC1439','aPROSITC1444','aPROSITC1458','aPROSITC1462','aPROSITC1473','aPROSITC1489','aPROSITC1504','aPROSITC1536','aPROSITC1541','aPROSITC1542','aPROSITC1565','aPROSITC1568','aPROSITC1575','aPROSITC1604','aPROSITC1613','aPROSITC1618','aPROSITC1620','aPROSITC1628','aPROSITC1630','aPROSITC1638','aPROSITC1688','aPROSITC1694','aPROSITC1697','aPROSITC1699','aPROSITC1701','aPROSITC1709','aPROSITC1713','aPROSITC1718','aPROSITC1734','aPROSITC1745','aPROSITC1747','aPROSITC1770','aPROSITC1778','aPROSITC1780','aPROSITC1787','aPROSITC1791','aPROSITC1793','aPROSITC1796','aPROSITC1805','aPROSITC1818','aPROSITC1822','aPROSITC1840','aPROSITC1862','aPROSITC1873','aPROSITC1887','aPROSITC1893','aPROSITC1903','aPROSITC1905','aPROSITC1921','aPROSITC1928','aPROSITC1930','aPROSITC1941','aPROSITC1944','aPROSITC1949','aPROSITC1963','aPROSITC1986','aPROSITC2010','aPROSITC2019','aPROSITC2039','aPROSITC2044','aPROSITC2067','aPROSITC2089','aPROSITC2095','aPROSITC2098','aPROSITC2101','aPROSITC2102','aPROSITC2115','aPROSITC2130','aPROSITC2132','aPROSITC2143','aPROSITC2160','aPROSITC2177','aPROSITC2180','aPROSITC2185','aPROSITC2193','aPROSITC2226','aPROSITC2232','aPROSITC2237','aPROSITC2241','aPROSITC2255','aPROSITC2256','aPROSITC2268','aPROSITC2285','aPROSITC2292','aPROSITC2295','aPROSITC2298','aPROSITC2304','aPROSITC2348','aPROSITC2349','aPROSITC2353','aPROSITC2375','aPROSITC2392','aPROSITC2725','aPROSITC2742','aPROSITC2743','aPROSITC2780','aPROSITC2797','aPROSITC2825','aPROSITC2836','aPROSITC2848','aPROSITC2876','aPROSITC2954','aPROSITC2973','aPROSITC2987','aPROSITC2990','aPROSITC2992','aPROSITC2994','aPROSITC2998','aPROSITC3000','aPROSITC3020','aPROSITC3021','aPROSITC3036','aPROSITC3050','aPROSITC3058','aPROSITC3087','aPROSITC3097','aPROSITC3108','aPROSITC3129']
timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
logFile = f"log_preprocessing_radialChartData_{timestamp}.txt"


def remove_file(filePath, filename):
    """
    function to remove the output file if it already exists
    """
    file = os.path.join(filePath, filename)
    if os.path.exists(file):
        os.remove(file)


def process_lockstate_android_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Lockstate IOS
    """
    print(f"Processing Lockstate IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    lockstateInputFilename = "powerState_android.csv"       # input file
    lockstateOutputFilename = "powerState_processed_android.csv"   # output file
    if removeOutputFileFlag:
        remove_file(outputDataPath, lockstateOutputFilename)        # removing the output file if they already exist

    header_list = ["id", "participantId", "attribute", "lck", "timestamp", "uploadtimestamp", "id1"]
    lockstate = pd.read_csv(os.path.join(inputDataPath, lockstateInputFilename), sep='|', header=None, names=header_list)
    print(f"Raw file shape: {lockstate.shape}", file=open(os.path.join(outputDataPath, logFile), "a"))

    # drop unecessary columns
    lockstate.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        lockstate = lockstate[lockstate["participantId"].isin(filteredParticipantIds)]

    #change time to Halifax time
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"], utc=True)
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"]).dt.tz_convert(tz='America/Halifax')
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"], utc=False)

    #add a date column
    lockstate["date"] = lockstate["timestamp"].dt.date

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = lockstate["participantId"].unique()
    for participantId in (participantIds):
        lockstate_participantId = lockstate[lockstate["participantId"] == participantId].copy()
        dates = lockstate_participantId["date"].unique()
        for date in dates:
            try:
                lockstate_participantId_date = lockstate_participantId[lockstate_participantId["date"] == date].copy()

                # drop duplicates
                lockstate_participantId_date.drop_duplicates(keep="last", inplace=True)

                #keeping only those rows which indicate locking events
                lockstate_participantId_date = lockstate_participantId_date[(lockstate_participantId_date["lck"] == "screen_on") | (lockstate_participantId_date["lck"] == "screen_off")].copy()
                lockstate_participantId_date.loc[lockstate_participantId_date["lck"]=="screen_on", "lck"] = 1
                lockstate_participantId_date.loc[lockstate_participantId_date["lck"]=="screen_off", "lck"] = 0
                
                #sort values
                lockstate_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                lockstate_participantId_date["minuteOfTheDay"] = (lockstate_participantId_date["timestamp"] - lockstate_participantId_date["timestamp"].dt.floor('d')).astype('timedelta64[m]').astype('int')

                # drop timestamp column
                lockstate_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                rows += lockstate_participantId_date.shape[0]
                cols = lockstate_participantId_date.shape[1]
                # append the data to file
                lockstate_participantId_date = lockstate_participantId_date.reindex(columns=["participantId", "date", "minuteOfTheDay", "lck"])
                lockstate_participantId_date.to_csv(os.path.join(outputDataPath, lockstateOutputFilename), mode='a', sep="|", header=headerWriteFlag, index=False)
                headerWriteFlag = False
                
            except:
                print(f"An exception occurred on Lock_state data for {participantId} {date}", file=open(os.path.join(outputDataPath, logFile), "a"))
    
    print(f"Processed file shape: ({rows},{cols})", file=open(os.path.join(outputDataPath, logFile), "a"))
    print("Lockstate completed", file=open(os.path.join(outputDataPath, logFile), "a"))


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

    # Lock_state data
    measure_processing_time(process_lockstate_android_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)

    # Accelerometer data
    measure_processing_time(process_accelerometer_android_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)

    # Gyroscope data
    measure_processing_time(process_gyroscope_android_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)

    totalendTime = time()
    print("End Time: " + datetime.now().strftime("%Y:%m:%d %I:%M:%S%p"), file=open(os.path.join(outputDataPath, logFile), "a"))
    print(f"Total run time: {round((totalendTime - totalstrTime)/60, 4)} mins", file=open(os.path.join(outputDataPath, logFile), "a"))