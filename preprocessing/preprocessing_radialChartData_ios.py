"""
#################################################################################################################
Script for agregatting raw sensor data over 1-minute periods for visualizating on Radial-time-chart
#################################################################################################################
"""
from itertools import combinations
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
filteredParticipantIds = ['iPROSITC0003','iPROSITC0007','iPROSITC0010','iPROSITC0019','iPROSITC0022','iPROSITC0030','iPROSITC0037','iPROSITC0041','iPROSITC0043','iPROSITC0048','iPROSITC0052','iPROSITC0057','iPROSITC0059','iPROSITC0061','iPROSITC0063','iPROSITC0067','iPROSITC0072','iPROSITC0074','iPROSITC0078','iPROSITC0083','iPROSITC0086','iPROSITC0087','iPROSITC0088','iPROSITC0090','iPROSITC0094','iPROSITC0096','iPROSITC0100','iPROSITC0102','iPROSITC0108','iPROSITC0110','iPROSITC0117','iPROSITC0121','iPROSITC0122','iPROSITC0124','iPROSITC0138','iPROSITC0146','iPROSITC0154','iPROSITC0155','iPROSITC0170','iPROSITC0181','iPROSITC0185','iPROSITC0189','iPROSITC0204','iPROSITC0208','iPROSITC0215','iPROSITC0219','iPROSITC0222','iPROSITC0226','iPROSITC0234','iPROSITC0244','iPROSITC0247','iPROSITC0253','iPROSITC0261','iPROSITC0270','iPROSITC0278','iPROSITC0292','iPROSITC0297','iPROSITC0309','iPROSITC0312','iPROSITC0323','iPROSITC0329','iPROSITC0331','iPROSITC0332','iPROSITC0333','iPROSITC0337','iPROSITC0345','iPROSITC0346','iPROSITC0350','iPROSITC0387','iPROSITC0389','iPROSITC0390','iPROSITC0399','iPROSITC0405','iPROSITC0408','iPROSITC0411','iPROSITC0425','iPROSITC0429','iPROSITC0430','iPROSITC0431','iPROSITC0439','iPROSITC0445','iPROSITC0447','iPROSITC0448','iPROSITC0451','iPROSITC0455','iPROSITC0456','iPROSITC0464','iPROSITC0474','iPROSITC0505','iPROSITC0506','iPROSITC0509','iPROSITC0510','iPROSITC0511','iPROSITC0513','iPROSITC0516','iPROSITC0526','iPROSITC0528','iPROSITC0529','iPROSITC0530','iPROSITC0531','iPROSITC0546','iPROSITC0560','iPROSITC0561','iPROSITC0569','iPROSITC0573','iPROSITC0580','iPROSITC0583','iPROSITC0586','iPROSITC0592','iPROSITC0595','iPROSITC0596','iPROSITC0599','iPROSITC0622','iPROSITC0625','iPROSITC0636','iPROSITC0640','iPROSITC0861','iPROSITC0876','iPROSITC0878','iPROSITC0890','iPROSITC0909','iPROSITC0919','iPROSITC0926','iPROSITC0928','iPROSITC0942','iPROSITC0961','iPROSITC0974','iPROSITC0978','iPROSITC0980','iPROSITC0981','iPROSITC0984','iPROSITC0992','iPROSITC0996','iPROSITC1005','iPROSITC1014','iPROSITC1018','iPROSITC1025','iPROSITC1026','iPROSITC1027','iPROSITC1029','iPROSITC1030','iPROSITC1031','iPROSITC1033','iPROSITC1034','iPROSITC1036','iPROSITC1037','iPROSITC1038','iPROSITC1039','iPROSITC1040','iPROSITC1041','iPROSITC1044','iPROSITC1046','iPROSITC1057','iPROSITC1061','iPROSITC1062','iPROSITC1066','iPROSITC1070','iPROSITC1079','iPROSITC1080','iPROSITC1086','iPROSITC1089','iPROSITC1090','iPROSITC1097','iPROSITC1100','iPROSITC1101','iPROSITC1104','iPROSITC1109','iPROSITC1110','iPROSITC1111','iPROSITC1119','iPROSITC1122','iPROSITC1126','iPROSITC1128','iPROSITC1135','iPROSITC1136','iPROSITC1137','iPROSITC1140','iPROSITC1153','iPROSITC1158','iPROSITC1174','iPROSITC1187','iPROSITC1192','iPROSITC1193','iPROSITC1221','iPROSITC1222','iPROSITC1223','iPROSITC1224','iPROSITC1227','iPROSITC1237','iPROSITC1240','iPROSITC1244','iPROSITC1261','iPROSITC1272','iPROSITC1293','iPROSITC1297','iPROSITC1299','iPROSITC1304','iPROSITC1317','iPROSITC1325','iPROSITC1326','iPROSITC1343','iPROSITC1369','iPROSITC1372','iPROSITC1379','iPROSITC1412','iPROSITC1413','iPROSITC1422','iPROSITC1424','iPROSITC1428','iPROSITC1501','iPROSITC1502','iPROSITC1512','iPROSITC1516','iPROSITC1526','iPROSITC1529','iPROSITC1548','iPROSITC1550','iPROSITC1553','iPROSITC1555','iPROSITC1562','iPROSITC1564','iPROSITC1602','iPROSITC1615','iPROSITC1621','iPROSITC1623','iPROSITC1627','iPROSITC1629','iPROSITC1635','iPROSITC1639','iPROSITC1642','iPROSITC1663','iPROSITC1666','iPROSITC1671','iPROSITC1678','iPROSITC1684','iPROSITC1685','iPROSITC1705','iPROSITC1712','iPROSITC1722','iPROSITC1742','iPROSITC1748','iPROSITC1754','iPROSITC1756','iPROSITC1761','iPROSITC1762','iPROSITC1763','iPROSITC1764','iPROSITC1785','iPROSITC1795','iPROSITC1798','iPROSITC1803','iPROSITC1807','iPROSITC1809','iPROSITC1810','iPROSITC1823','iPROSITC1826','iPROSITC1827','iPROSITC1835','iPROSITC1844','iPROSITC1861','iPROSITC1863','iPROSITC1864','iPROSITC1865','iPROSITC1874','iPROSITC1877','iPROSITC1898','iPROSITC1911','iPROSITC1914','iPROSITC1926','iPROSITC1942','iPROSITC1966','iPROSITC1979','iPROSITC1980','iPROSITC1983','iPROSITC1985','iPROSITC1996','iPROSITC1999','iPROSITC2002','iPROSITC2029','iPROSITC2037','iPROSITC2059','iPROSITC2065','iPROSITC2069','iPROSITC2076','iPROSITC2096','iPROSITC2111','iPROSITC2117','iPROSITC2129','iPROSITC2134','iPROSITC2135','iPROSITC2156','iPROSITC2162','iPROSITC2170','iPROSITC2195','iPROSITC2202','iPROSITC2203','iPROSITC2207','iPROSITC2219','iPROSITC2239','iPROSITC2247','iPROSITC2259','iPROSITC2264','iPROSITC2265','iPROSITC2267','iPROSITC2269','iPROSITC2271','iPROSITC2278','iPROSITC2303','iPROSITC2306','iPROSITC2315','iPROSITC2323','iPROSITC2330','iPROSITC2332','iPROSITC2333','iPROSITC2360','iPROSITC2382','iPROSITC2384','iPROSITC2394','iPROSITC2928','iPROSITC2964','iPROSITC2986','iPROSITC3001','iPROSITC3014','iPROSITC3025','iPROSITC3029','iPROSITC3031','iPROSITC3035','iPROSITC3037','iPROSITC3038','iPROSITC3044','iPROSITC3053','iPROSITC3070','iPROSITC3071','iPROSITC3076','iPROSITC3078','iPROSITC3079','iPROSITC3101','iPROSITC3102','iPROSITC3110','iPROSITC3111','iPROSITC3114','iPROSITC3117','iPROSITC3121','iPROSITC3124','iPROSITC3148','iPROSITC3150','iPROSITC3169','iPROSITC3172','iPROSITC3196','iPROSITC3201','iPROSITC3213','iPROSITC3214','iPROSITC3217','iPROSITC3219','iPROSITC3221','iPROSITC3226','iPROSITC3227','iPROSITC3229','iPROSITC3230','iPROSITC3233','iPROSITC3234','iPROSITC3235','iPROSITC3244','iPROSITC3249','iPROSITC3259','iPROSITC3261','iPROSITC3279','iPROSITC3282','iPROSITC3305']
timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
logFile = f"log_preprocessing_radialChartData_new_{timestamp}.txt"


def remove_file(filePath, filename):
    """
    function to remove the output file if it already exists
    """
    file = os.path.join(filePath, filename)
    if os.path.exists(file):
        os.remove(file)


def process_lockstate_ios_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Lockstate IOS
    """
    print(f"Processing Lockstate IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    lockstateInputFilename = "Lock_state_ios.csv"       # input file
    lockstateOutputFilename = "Lock_state_processed_ios.csv"   # output file    
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
                lockstate_participantId_date = lockstate_participantId_date[(lockstate_participantId_date["lck"] == "UNLOCKED") | (lockstate_participantId_date["lck"] == "LOCKED")].copy()
                lockstate_participantId_date.loc[lockstate_participantId_date["lck"]=="UNLOCKED", "lck"] = 1
                lockstate_participantId_date.loc[lockstate_participantId_date["lck"]=="LOCKED", "lck"] = 0
                
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


def process_call_ios_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Call IOS
    """
    print(f"Processing Call IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    callInputFilename = "Call_ios.csv"
    callOutputFilename = "Call_processed_ios.csv"
    if removeOutputFileFlag:
        remove_file(outputDataPath, callOutputFilename)        # removing the output file if they already exist

    header_list = ["id", "participantId", "attribute", "callevent", "timestamp", "uploadtimestamp", "id1"]
    call = pd.read_csv(os.path.join(inputDataPath, callInputFilename), sep="|", header=None, names=header_list)
    print(f"Raw file shape: {call.shape}", file=open(os.path.join(outputDataPath, logFile), "a"))

    # drop unecessary columns
    call.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        call = call[call["participantId"].isin(filteredParticipantIds)]
    
    #change time to Halifax time
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=True)
    call["timestamp"] = pd.to_datetime(call["timestamp"]).dt.tz_convert(tz='America/Halifax')
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=False)

    #add a date column
    call["date"] = call["timestamp"].dt.date

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = call["participantId"].unique()
    for participantId in (participantIds):
        call_participantId = call[call["participantId"] == participantId].copy()
        dates = call_participantId["date"].unique()
        for date in dates:
            try:
                call_participantId_date = call_participantId[call_participantId["date"] == date].copy()

                # drop duplicates
                call_participantId_date.drop_duplicates(inplace=True)

                #keeping only those rows which indicate calling events
                call_participantId_date = call_participantId_date[call_participantId_date["callevent"].isin(['CALL_INCOMING', 'CALL_CONNECTED', 'CALL_DISCONNECTED', 'CALL_DIALING', 'CALL_ON_HOLD'])]

                #sort values
                call_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                call_participantId_date["minuteOfTheDay"] = (call_participantId_date["timestamp"] - call_participantId_date["timestamp"].dt.floor('d')).astype('timedelta64[m]').astype('int')

                # drop timestamp column
                call_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                rows += call_participantId_date.shape[0]
                cols = call_participantId_date.shape[1]
                # append the data to file
                call_participantId_date.to_csv(os.path.join(outputDataPath, callOutputFilename), mode='a', sep="|", header=headerWriteFlag, index=False)
                headerWriteFlag = False

            except:
                print(f"An exception occurred on Call data for {participantId} {date}", file=open(os.path.join(outputDataPath, logFile), "a"))

    print(f"Processed file shape: ({rows},{cols})", file=open(os.path.join(outputDataPath, logFile), "a"))
    print("Call completed", file=open(os.path.join(outputDataPath, logFile), "a"))


def process_brightness_ios_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    #### Brightness IOS data
    """
    print(f"Processing Brightness IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    brightnessInputFilename = "Brightness_ios.csv"
    brightnessOutputFilename = "Brightness_processed_ios.csv"
    if removeOutputFileFlag:
        remove_file(outputDataPath, brightnessOutputFilename)        # removing the output file if they already exist

    header_list = ["id", "participantId", "attribute", "brt", "timestamp", "uploadtimestamp", "id1"]
    brightness = pd.read_csv(os.path.join(inputDataPath, brightnessInputFilename), sep='|', header=None, names=header_list)
    print(f"Raw file shape: {brightness.shape}", file=open(os.path.join(outputDataPath, logFile), "a"))

    # drop unecessary columns
    brightness.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        brightness = brightness[brightness["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=True)
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"]).dt.tz_convert(tz='America/Halifax')
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=False)

    #add a date column
    brightness["date"] = brightness["timestamp"].dt.date

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = brightness["participantId"].unique()
    for participantId in (participantIds):
        brightness_participantId = brightness[brightness["participantId"] == participantId].copy()
        dates = brightness_participantId["date"].unique()
        for date in dates:
            try:
                brightness_participantId_date = brightness_participantId[brightness_participantId["date"] == date].copy()

                # drop duplicates
                brightness_participantId_date.drop_duplicates(inplace=True)

                #sort values
                brightness_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                brightness_participantId_date["minuteOfTheDay"] = (brightness_participantId_date["timestamp"] - brightness_participantId_date["timestamp"].dt.floor('d')).astype('timedelta64[m]').astype('int')

                # drop timestamp column
                brightness_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #Aggregate the data over a period of 1minute
                brightnessAgg = brightness_participantId_date.groupby(["participantId", "date", "minuteOfTheDay"])["brt"].agg("mean").reset_index()
                brightnessAgg["brt"] = round(brightnessAgg["brt"], 2)

                rows += brightnessAgg.shape[0]
                cols = brightnessAgg.shape[1]
                # append the data to file
                brightnessAgg.to_csv(os.path.join(outputDataPath, brightnessOutputFilename), mode='a', sep="|", header=headerWriteFlag, index=False)
                headerWriteFlag = False

            except:
                print(f"An exception occurred on Brightness data for {participantId} {date}", file=open(os.path.join(outputDataPath, logFile), "a"))

    print(f"Processed file shape: ({rows},{cols})", file=open(os.path.join(outputDataPath, logFile), "a"))
    print("Brightness completed", file=open(os.path.join(outputDataPath, logFile), "a"))


def process_accelerometer_ios_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Accelerometer IOS
    """
    print(f"Processing Accelerometer IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    accelerometerInputFilename = "Accelerometer_ios.csv"
    accelerometerOutputFilename = "Accelerometer_processed_ios.csv"
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

    # replace partcipant id
    accelerometer['participantId'] = accelerometer['participantId'].str.replace('aPROSIT','PROSIT')


    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = accelerometer["participantId"].unique()

    for participantId in (participantIds):
        if not "PROSITC" in participantId:
            continue

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


def process_gyroscope_ios_data(inputDataPath, outputDataPath, removeOutputFileFlag, headerWriteFlag):
    """
    ### Gyroscope IOS
    """
    print(f"Processing Gyroscope IOS data from '{inputDataPath}'...", file=open(os.path.join(outputDataPath, logFile), "a"))

    gyroscopeInputFilename = "Gyroscope_ios.csv"
    gyroscopeOutputFilename = "Gyroscope_processed_ios.csv"
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

    # replace partcipant id
    gyroscope['participantId'] = gyroscope['participantId'].str.replace('aPROSIT','PROSIT')

    # breaking down processing into multiple iterations
    rows, cols = 0, 0
    participantIds = gyroscope["participantId"].unique()
    for participantId in (participantIds):
        if not "PROSITC" in participantId:
            continue

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
    print("Start Time: " + datetime.now().strftime("%Y:%m:%d %I:%M:%S%p") + "\n", file=open(os.path.join(outputDataPath, logFile), "a+"))

    # Lock_state data
    measure_processing_time(process_lockstate_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_lockstate_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    # Call data
    # measure_processing_time(process_call_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_call_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    # Brightness data
    # measure_processing_time(process_brightness_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_brightness_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    # Accelerometer data
    measure_processing_time(process_accelerometer_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_accelerometer_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    # Gyroscope data
    measure_processing_time(process_gyroscope_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_gyroscope_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    # Sleepnoise data
    # measure_processing_time(process_sleepnoise_ios_data, inputDataPath1, outputDataPath, removeOutputFileFlag=True, headerWriteFlag=True)
    # measure_processing_time(process_sleepnoise_ios_data, inputDataPath2, outputDataPath, removeOutputFileFlag=False, headerWriteFlag=False)

    totalendTime = time()
    print("End Time: " + datetime.now().strftime("%Y:%m:%d %I:%M:%S%p"), file=open(os.path.join(outputDataPath, logFile), "a"))
    print(f"Total run time: {round((totalendTime - totalstrTime)/60, 4)} mins", file=open(os.path.join(outputDataPath, logFile), "a"))