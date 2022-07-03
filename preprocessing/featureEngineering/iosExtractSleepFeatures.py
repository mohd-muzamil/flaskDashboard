"""
#################################################################################################################
Script for extracting below sleep related features using IOS lockstate, brightness, accelerometer and gyroscope data
Feature1(sleepStartTime): Estimated start time of the sleep
Feature2(sleepEndTime): Estimated end time of the sleep
Feature3(sleepDuration): Estimated sleep duration

input/output file names need to be specifed in the code below #config
#################################################################################################################
"""

from imports import *

# Filtered participantIds from another notebook. Only data from these will be analysed
filteredParticipantIds = []
filteredParticipantIds = ['iPROSITC0003','iPROSITC0007','iPROSITC0010','iPROSITC0019','iPROSITC0022','iPROSITC0030','iPROSITC0037','iPROSITC0041','iPROSITC0043','iPROSITC0048','iPROSITC0052','iPROSITC0057','iPROSITC0059','iPROSITC0061','iPROSITC0063','iPROSITC0067','iPROSITC0072','iPROSITC0074','iPROSITC0078','iPROSITC0083','iPROSITC0086','iPROSITC0087','iPROSITC0088','iPROSITC0090','iPROSITC0094','iPROSITC0096','iPROSITC0100','iPROSITC0102','iPROSITC0108','iPROSITC0110','iPROSITC0117','iPROSITC0121','iPROSITC0122','iPROSITC0124','iPROSITC0138','iPROSITC0146','iPROSITC0154','iPROSITC0155','iPROSITC0170','iPROSITC0181','iPROSITC0185','iPROSITC0189','iPROSITC0204','iPROSITC0208','iPROSITC0215','iPROSITC0219','iPROSITC0222','iPROSITC0226','iPROSITC0234','iPROSITC0244','iPROSITC0247','iPROSITC0253','iPROSITC0261','iPROSITC0270','iPROSITC0278','iPROSITC0292','iPROSITC0297','iPROSITC0309','iPROSITC0312','iPROSITC0323','iPROSITC0329','iPROSITC0331','iPROSITC0332','iPROSITC0333','iPROSITC0337','iPROSITC0345','iPROSITC0346','iPROSITC0350','iPROSITC0387','iPROSITC0389','iPROSITC0390','iPROSITC0399','iPROSITC0405','iPROSITC0408','iPROSITC0411','iPROSITC0425','iPROSITC0429','iPROSITC0430','iPROSITC0431','iPROSITC0439','iPROSITC0445','iPROSITC0447','iPROSITC0448','iPROSITC0451','iPROSITC0455','iPROSITC0456','iPROSITC0464','iPROSITC0474','iPROSITC0505','iPROSITC0506','iPROSITC0509','iPROSITC0510','iPROSITC0511','iPROSITC0513','iPROSITC0516','iPROSITC0526','iPROSITC0528','iPROSITC0529','iPROSITC0530','iPROSITC0531','iPROSITC0546','iPROSITC0560','iPROSITC0561','iPROSITC0569','iPROSITC0573','iPROSITC0580','iPROSITC0583','iPROSITC0586','iPROSITC0592','iPROSITC0595','iPROSITC0596','iPROSITC0599','iPROSITC0622','iPROSITC0625','iPROSITC0636','iPROSITC0640','iPROSITC0861','iPROSITC0876','iPROSITC0878','iPROSITC0890','iPROSITC0909','iPROSITC0919','iPROSITC0926','iPROSITC0928','iPROSITC0942','iPROSITC0961','iPROSITC0974','iPROSITC0978','iPROSITC0980','iPROSITC0981','iPROSITC0984','iPROSITC0992','iPROSITC0996','iPROSITC1005','iPROSITC1014','iPROSITC1018','iPROSITC1025','iPROSITC1026','iPROSITC1027','iPROSITC1029','iPROSITC1030','iPROSITC1031','iPROSITC1033','iPROSITC1034','iPROSITC1036','iPROSITC1037','iPROSITC1038','iPROSITC1039','iPROSITC1040','iPROSITC1041','iPROSITC1044','iPROSITC1046','iPROSITC1057','iPROSITC1061','iPROSITC1062','iPROSITC1066','iPROSITC1070','iPROSITC1079','iPROSITC1080','iPROSITC1086','iPROSITC1089','iPROSITC1090','iPROSITC1097','iPROSITC1100','iPROSITC1101','iPROSITC1104','iPROSITC1109','iPROSITC1110','iPROSITC1111','iPROSITC1119','iPROSITC1122','iPROSITC1126','iPROSITC1128','iPROSITC1135','iPROSITC1136','iPROSITC1137','iPROSITC1140','iPROSITC1153','iPROSITC1158','iPROSITC1174','iPROSITC1187','iPROSITC1192','iPROSITC1193','iPROSITC1221','iPROSITC1222','iPROSITC1223','iPROSITC1224','iPROSITC1227','iPROSITC1237','iPROSITC1240','iPROSITC1244','iPROSITC1261','iPROSITC1272','iPROSITC1293','iPROSITC1297','iPROSITC1299','iPROSITC1304','iPROSITC1317','iPROSITC1325','iPROSITC1326','iPROSITC1343','iPROSITC1369','iPROSITC1372','iPROSITC1379','iPROSITC1412','iPROSITC1413','iPROSITC1422','iPROSITC1424','iPROSITC1428','iPROSITC1501','iPROSITC1502','iPROSITC1512','iPROSITC1516','iPROSITC1526','iPROSITC1529','iPROSITC1548','iPROSITC1550','iPROSITC1553','iPROSITC1555','iPROSITC1562','iPROSITC1564','iPROSITC1602','iPROSITC1615','iPROSITC1621','iPROSITC1623','iPROSITC1627','iPROSITC1629','iPROSITC1635','iPROSITC1639','iPROSITC1642','iPROSITC1663','iPROSITC1666','iPROSITC1671','iPROSITC1678','iPROSITC1684','iPROSITC1685','iPROSITC1705','iPROSITC1712','iPROSITC1722','iPROSITC1742','iPROSITC1748','iPROSITC1754','iPROSITC1756','iPROSITC1761','iPROSITC1762','iPROSITC1763','iPROSITC1764','iPROSITC1785','iPROSITC1795','iPROSITC1798','iPROSITC1803','iPROSITC1807','iPROSITC1809','iPROSITC1810','iPROSITC1823','iPROSITC1826','iPROSITC1827','iPROSITC1835','iPROSITC1844','iPROSITC1861','iPROSITC1863','iPROSITC1864','iPROSITC1865','iPROSITC1874','iPROSITC1877','iPROSITC1898','iPROSITC1911','iPROSITC1914','iPROSITC1926','iPROSITC1942','iPROSITC1966','iPROSITC1979','iPROSITC1980','iPROSITC1983','iPROSITC1985','iPROSITC1996','iPROSITC1999','iPROSITC2002','iPROSITC2029','iPROSITC2037','iPROSITC2059','iPROSITC2065','iPROSITC2069','iPROSITC2076','iPROSITC2096','iPROSITC2111','iPROSITC2117','iPROSITC2129','iPROSITC2134','iPROSITC2135','iPROSITC2156','iPROSITC2162','iPROSITC2170','iPROSITC2195','iPROSITC2202','iPROSITC2203','iPROSITC2207','iPROSITC2219','iPROSITC2239','iPROSITC2247','iPROSITC2259','iPROSITC2264','iPROSITC2265','iPROSITC2267','iPROSITC2269','iPROSITC2271','iPROSITC2278','iPROSITC2303','iPROSITC2306','iPROSITC2315','iPROSITC2323','iPROSITC2330','iPROSITC2332','iPROSITC2333','iPROSITC2360','iPROSITC2382','iPROSITC2384','iPROSITC2394','iPROSITC2928','iPROSITC2964','iPROSITC2986','iPROSITC3001','iPROSITC3014','iPROSITC3025','iPROSITC3029','iPROSITC3031','iPROSITC3035','iPROSITC3037','iPROSITC3038','iPROSITC3044','iPROSITC3053','iPROSITC3070','iPROSITC3071','iPROSITC3076','iPROSITC3078','iPROSITC3079','iPROSITC3101','iPROSITC3102','iPROSITC3110','iPROSITC3111','iPROSITC3114','iPROSITC3117','iPROSITC3121','iPROSITC3124','iPROSITC3148','iPROSITC3150','iPROSITC3169','iPROSITC3172','iPROSITC3196','iPROSITC3201','iPROSITC3213','iPROSITC3214','iPROSITC3217','iPROSITC3219','iPROSITC3221','iPROSITC3226','iPROSITC3227','iPROSITC3229','iPROSITC3230','iPROSITC3233','iPROSITC3234','iPROSITC3235','iPROSITC3244','iPROSITC3249','iPROSITC3259','iPROSITC3261','iPROSITC3279','iPROSITC3282','iPROSITC3305']


def sleep_analysis(df, sleep_break=30):
    """
    method to assign a sleep/awake state to each 10-minute time block
    Estimate the sleeping hours based on consecutive sleep time-blocks
    """
    prev = 0
    sleep = 0
    start = end = 0
    sleep_start = sleep_end = 0
    sleep_duration = 0

    for _, row in df.iterrows():
        curr = row.timeblock
        if (np.round((curr - prev), 2)) <= (sleep_break/10):
            sleep += 1
            end = curr
        else:
            sleep = 0
            start = curr
            end = curr
        
        if sleep>sleep_duration:
            sleep_duration = sleep
            sleep_start = np.round(start, 2)
            sleep_end = np.round(end, 2)

        prev = row.timeblock
    
    sleep_duration = np.round((sleep_duration*10/60), 2)
    # sleep_start_time and sleep_end_time are in minute of the day format
    # sleep_start_time = '{:02d}:{:02d}'.format(*divmod(int(sleep_start*10), 60))
    # sleep_end_time = '{:02d}:{:02d}'.format(*divmod(int(sleep_end*10), 60))
    # changed this to reflect hour of the day
    sleep_start_time = round((sleep_start*10)/60, 2)
    sleep_end_time = round((sleep_end*10)/60, 2)
    # print(f"sleep_duration:{sleep_duration}hrs sleep_start:{sleep_start}, sleep_end:{sleep_end}, no_sleep_interruptions:{no_sleep_interruptions}, duration_of_sleep_interruptions:{duration_of_sleep_interruptions}")
    # return the sleep times detected by the algorithm
    return  sleep_duration, sleep_start_time, sleep_end_time


######################################################################################
# pre processing lockstate data
######################################################################################
def process_lockstate_ios_data(inputDataPath, dataFilename):
    print(f"Processing Lockstate IOS data from '{inputDataPath}'...")
    # read file with a header
    header_list = ["id", "participantId", "attribute", "lck", "timestamp", "uploadtimestamp", "id1"]
    lockstate = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep='|', header=None, names=header_list)

    # drop unecessary columns
    lockstate.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        lockstate = lockstate[lockstate["participantId"].isin(filteredParticipantIds)]

    #change time to Halifax time
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"], utc=True)
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"]).dt.tz_convert(tz='America/Halifax')
    lockstate["timestamp"] = pd.to_datetime(lockstate["timestamp"], utc=False)

    #add new columns to help extract features
    lockstate["date"] = lockstate["timestamp"].dt.date
    
    # For imputation and concatenation
    lockstateProcessed = pd.DataFrame()
    timeblock = [i for i in range(0,144)]
    allMinutes = pd.DataFrame({"timeblock":timeblock})
    # breaking down processing into multiple iterations
    participantIds = lockstate["participantId"].unique()
    for participantId in tqdm(participantIds):
        lockstate_participantId = lockstate[lockstate["participantId"] == participantId].copy()
        dates = lockstate_participantId["date"].unique()
        for date in dates:
            try:
                lockstate_participantId_date = lockstate_participantId[lockstate_participantId["date"] == date].copy()

                # drop duplicates
                lockstate_participantId_date.drop_duplicates(keep="last", inplace=True)

                #keeping only those rows which indicate locking events
                lockstate_participantId_date = lockstate_participantId_date[(lockstate_participantId_date["lck"] == "UNLOCKED") | (lockstate_participantId_date["lck"] == "LOCKED")].copy()
                
                #sort values
                lockstate_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                lockstate_participantId_date["timeblock"] = (lockstate_participantId_date["timestamp"].dt.hour * 6) + (lockstate_participantId_date["timestamp"].dt.minute/10).astype(int)

                # drop timestamp column
                lockstate_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                # imputing missing values
                lockstate_participantId_date = pd.merge(lockstate_participantId_date, allMinutes, how="right", on="timeblock")
                lockstate_participantId_date.ffill(inplace=True)
                lockstate_participantId_date.bfill(inplace=True)
                
                # concatenating the data into single dataframe
                lockstateProcessed = pd.concat([lockstateProcessed, lockstate_participantId_date], axis=0)

            except:
                print(f"An exception occurred on Lock_state data for {participantId} {date}")

    print("Preprocessing completed for lockstate data")
    return lockstateProcessed


######################################################################################
# pre processing brightness data
######################################################################################
def process_brightness_ios_data(inputDataPath, dataFilename):
    print(f"Processing Brightness IOS data from '{inputDataPath}'...")
    # read file with a header
    header_list = ["id", "participantId", "attribute", "brt", "timestamp", "uploadtimestamp", "id1"]
    brightness = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep='|', header=None, names=header_list)
    
    # drop unecessary columns
    brightness.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        brightness = brightness[brightness["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=True)
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"]).dt.tz_convert(tz='America/Halifax')
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=False)

    #add new columns to help extract features
    brightness["date"] = brightness["timestamp"].dt.date

    # For concatenation
    brightnessProcessed = pd.DataFrame()
    # breaking down processing into multiple iterations
    participantIds = brightness["participantId"].unique()
    for participantId in tqdm(participantIds):
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
                brightness_participantId_date["timeblock"] = (brightness_participantId_date["timestamp"].dt.hour * 6) + (brightness_participantId_date["timestamp"].dt.minute/10).astype(int)

                # drop timestamp column
                brightness_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #Aggregate the data over a period of 10minute timeblocks
                brightnessAgg = brightness_participantId_date.groupby(["participantId", "date", "timeblock"])["brt"].agg("mean").reset_index()
                header_list = ["participantId", "date", "timeblock", "brt"]
                brightnessAgg.columns = header_list
                brightnessAgg["brt"] = round(brightnessAgg["brt"], 2)

                # concatenating the data into single dataframe
                brightnessProcessed = pd.concat([brightnessProcessed, brightnessAgg], axis=0)

            except:
                print(f"An exception occurred on Brightness data for {participantId} {date}")

    print("Preprocessing completed for brightness data")
    return brightnessProcessed


######################################################################################
# pre processing accelerometer data
######################################################################################
def process_accelerometer_ios_data(inputDataPath, dataFilename):    
    print(f"Processing Accelerometer IOS data from '{inputDataPath}'...")
    # read file with header
    header_list = ["id", "participantId", "attribute", "accX", "accY", "accZ", "timestamp", "uploadtimestamp", "id1"]
    accelerometer = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep='|', header=None, names=header_list)
    print("accelerometer before", accelerometer.shape)

    # drop unecessary columns
    accelerometer.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        accelerometer = accelerometer[accelerometer["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=True)
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"]).dt.tz_convert(tz='America/Halifax')
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=False)

    #add a date column
    accelerometer["date"] = accelerometer["timestamp"].dt.date

    # For concatenation
    accelerometerProcessed = pd.DataFrame()
    # breaking down processing into multiple iterations
    participantIds = accelerometer["participantId"].unique()
    for participantId in tqdm(participantIds):
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
                accelerometer_participantId_date["timeblock"] = (accelerometer_participantId_date["timestamp"].dt.hour * 6) + (accelerometer_participantId_date["timestamp"].dt.minute/10).astype(int)

                # ENMO : Euclidean Norm Minus One (ENMO) with negative values rounded to zero in g has been shown to correlate with the magnitude of acceleration and human energy expenditure
                accelerometer_participantId_date["acc"] = np.sqrt(accelerometer_participantId_date["accX"]**2 + accelerometer_participantId_date["accY"]**2 + accelerometer_participantId_date["accZ"]**2)
                # accelerometer_participantId_date["acc"] = np.maximum(0, (np.sqrt((accelerometer_participantId_date["accelerationx"]**2) + (accelerometer_participantId_date["accelerationy"]**2) + (accelerometer_participantId_date["accelerationz"]**2)) - 1))

                # drop timestamp column
                accelerometer_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #drop axial accelerometer columns
                accelerometer_participantId_date.drop(["accX", "accY", "accZ"], axis=1, inplace=True)

                #Aggregate the data over a period of 10minute timeblocks
                accelerometerAgg = accelerometer_participantId_date.groupby(["participantId", "date", "timeblock"])["acc"].agg("mean").reset_index()
                # accelerometer.columns = ['_'.join(col).strip() if col[1]!="" else col[0] for col in accelerometer.columns.values ]
                accelerometerAgg["acc"] = round(accelerometerAgg["acc"], 2)
                
                # concatenating the data into single dataframe
                accelerometerProcessed = pd.concat([accelerometerProcessed, accelerometerAgg], axis=0)
                
            except:
                print(f"An exception occurred on Accelerometer data for {participantId} {date}")
    print("accelerometer after", accelerometerProcessed.shape)
    print("Preprocessing completed for accelerometer data")
    return accelerometerProcessed


######################################################################################
# pre processing gyroscope data
######################################################################################
def process_gyroscope_ios_data(inputDataPath, dataFilename):    
    print(f"Processing Gyroscope IOS data from '{inputDataPath}'...")
    # read file with header
    header_list = ["id", "participantId", "attribute", "gyroX", "gyroY", "gyroZ", "timestamp", "uploadtimestamp", "id1"]
    gyroscope = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep='|', header=None, names=header_list)

    # drop unecessary columns
    gyroscope.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        gyroscope = gyroscope[gyroscope["participantId"].isin(filteredParticipantIds)].reset_index(drop=True)

    #change time to Halifax time
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=True)
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"]).dt.tz_convert(tz='America/Halifax')
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=False)

    #add new columns to help extract features
    gyroscope["date"] = gyroscope["timestamp"].dt.date

    # For concatenation
    gyroscopeProcessed = pd.DataFrame()
    # breaking down processing into multiple iterations
    participantIds = gyroscope["participantId"].unique()
    for participantId in tqdm(participantIds):
        gyroscope_participantId = gyroscope[gyroscope["participantId"] == participantId].copy()
        dates = gyroscope_participantId["date"].unique()
        for date in dates:
            try:
                gyroscope_participantId_date = gyroscope_participantId[gyroscope_participantId["date"] == date].copy()

                # drop duplicates
                gyroscope_participantId_date.drop_duplicates(keep="last", inplace=True)

                #sort values
                gyroscope_participantId_date.sort_values(["participantId", "timestamp"], inplace=True, ascending=True, ignore_index=True)

                #add necessary columns
                gyroscope_participantId_date["timeblock"] = (gyroscope_participantId_date["timestamp"].dt.hour * 6) + (np.floor(gyroscope_participantId_date["timestamp"].dt.minute / 10)).astype(int)

                # ENMO : Euclidean Norm Minus One (ENMO) with negative values rounded to zero in g has been shown to correlate with the magnitude of acceleration and human energy expenditure
                gyroscope_participantId_date["gyro"] = np.sqrt(gyroscope_participantId_date["gyroX"]**2 + gyroscope_participantId_date["gyroY"]**2 + gyroscope_participantId_date["gyroZ"]**2)
                # gyroscope_participantId_date["acc"] = np.maximum(0, (np.sqrt((gyroscope_participantId_date["accelerationx"]**2) + (gyroscope_participantId_date["accelerationy"]**2) + (gyroscope_participantId_date["accelerationz"]**2)) - 1))=

                # drop timestamp column
                gyroscope_participantId_date.drop(["timestamp"], axis=1, inplace=True)

                #drop axial gyroscope columns
                gyroscope_participantId_date.drop(["gyroX", "gyroY", "gyroZ"], axis=1, inplace=True)

                #Aggregate the data over a period of 10minute timeblocks
                gyroscopeAgg = gyroscope_participantId_date.groupby(["participantId", "date", "timeblock"])["gyro"].agg("mean").reset_index()
                # gyroscopeAgg.columns = ['_'.join(col).strip() if col[1]!="" else col[0] for col in gyroscopeAgg.columns.values ]
                gyroscopeAgg["gyro"] = round(gyroscopeAgg["gyro"], 2)
                
                # concatenating the data into single dataframe
                gyroscopeProcessed = pd.concat([gyroscopeProcessed, gyroscopeAgg], axis=0)

            except:
                print(f"An exception occurred on Gyroscope data for {participantId} {date}")

    print("Preprocessing completed for gyroscope data")
    return gyroscopeProcessed


######################################################################################
# combining all the sensor data to prepare sleep data
######################################################################################
def combine_ios_features(lockstate, brightness, accelerometer, gyroscope):
    dfs = [lockstate, brightness, accelerometer, gyroscope]

    sleep_data = reduce(lambda left,right: pd.merge(left,right,on=["participantId", "date", "timeblock"], how="outer"), dfs)
    sleep_data.fillna(0, inplace=True)

    # datenum: decided not to use this
    # for participantId in sleep_data.participantId.unique():
    #     sleep_data.loc[sleep_data.participantId == participantId,'date_num'] = pd.factorize(sleep_data.loc[sleep_data.participantId == participantId, "date"])[0] + 1

    # defining a dataframe to store the sleep features
    sleepFeatures = pd.DataFrame(columns=["participantId", "date", "date_num", "sleeping_hrs", "sleep_start_time", "sleep_end_time"])

    # participantIds = sleep_data.groupby('participantId').size().reset_index(name="cnt").sort_values("cnt", ascending=False).participantId.unique()
    participantIds = sleep_data["participantId"].unique()
    index = 0
    for participantId in tqdm(participantIds):
        sleep_data_participantId = sleep_data[sleep_data.participantId == participantId].copy()
        sleep_data_participantId['date_num'] = pd.factorize(sleep_data_participantId["date"])[0] + 1
        for date_num in sleep_data_participantId.date_num.unique():
            sleep_data_participantId_date = sleep_data_participantId[sleep_data_participantId.date_num == date_num].copy()

            # set values with less than 0.1 quantile values to 0 to remove noise
            # sleep_data_participantId_date.loc[sleep_data_participantId_date["acc_mean"] <= sleep_data_participantId_date["acc_mean"].quantile(0.1), "acc_mean"] = 0
            # sleep_data_participantId_date.loc[sleep_data_participantId_date["gyro_mean"] <= sleep_data_participantId_date["gyro_mean"].quantile(0.1), "gyro_mean"] = 0

            # filtering out only those timeblocks which show device usage
            sleep_data_participantId_date = sleep_data_participantId_date[(sleep_data_participantId_date.lck == "LOCKED") & (sleep_data_participantId_date.acc == 0) & (sleep_data_participantId_date.gyro == 0) & (sleep_data_participantId_date.brt==0)]
            
            if sleep_data_participantId_date.shape[0]>0:
                sleep_duration, sleep_start_time, sleep_end_time = sleep_analysis(sleep_data_participantId_date, sleep_break=30)
                sleepFeatures.loc[index] = [participantId, sleep_data_participantId_date.date.unique()[0], date_num, sleep_duration, sleep_start_time, sleep_end_time]
                index += 1
    
    return sleepFeatures

    
def getIosSleepFeatures(inputDataPath, featurePath):
    '''
    considering below conditions to assign a sleep state to a time block which is chosen as 10mins
    # screen state  - "Locked"
    # brightness    -   0
    # accelerometer -   0
    # gyroscope     -   0
    analysis of continious timeblocks decides the start and end time of sleep duration and no of sleep interruptions.
    '''
    print("Begin extraction - Sleep features")

    # config
    timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    dbName = inputDataPath.split("/")[-1]

    # # screen state data
    dataFilename1 = "Lock_state_ios.csv"
    # # dataFilename1 = "Lock_state_temp_ios.csv"
    featureFilename1 = f"ios_Lock_state_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # brightness data
    dataFilename2 = "Brightness_ios.csv"
    # dataFilename2 = "Brightness_temp_ios.csv"
    featureFilename2 = f"ios_Brightness_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # accelerometer data
    dataFilename3 = "Accelerometer_ios.csv"
    # # dataFilename3 = "Accelerometer_temp_ios.csv"
    featureFilename3 = f"ios_Accelerometer_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # gyroscope data
    dataFilename4 = "Gyroscope_ios.csv"
    # # dataFilename4 = "Gyroscope_temp_ios.csv"
    featureFilename4 = f"ios_Gyroscope_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    finalFeatureFilename = f"ios_sleep_features_{dbName}_{timestamp}_ios.csv"

    if not (os.path.exists(os.path.join(inputDataPath, dataFilename1))):
        sys.exit(f"{dataFilename1} file does not exist in {inputDataPath} folder \nscript aborted")
    
    if not (os.path.exists(os.path.join(inputDataPath, dataFilename2))):
        sys.exit(f"{dataFilename2} file does not exist in {inputDataPath} folder \nscript aborted")
    
    if not (os.path.exists(os.path.join(inputDataPath, dataFilename3))):
        sys.exit(f"{dataFilename3} file does not exist in {inputDataPath} folder \nscript aborted")

    if not (os.path.exists(os.path.join(inputDataPath, dataFilename4))):
        sys.exit(f"{dataFilename4} file does not exist in {inputDataPath} folder \nscript aborted")


    # Preprocessing and saving the raw sensor data
    lockstate = process_lockstate_ios_data(inputDataPath, dataFilename1)
    lockstate.to_csv(os.path.join(featurePath, featureFilename1), header=True, index=False)

    brightness = process_brightness_ios_data(inputDataPath, dataFilename2)
    brightness.to_csv(os.path.join(featurePath, featureFilename2), header=True, index=False)

    accelerometer = process_accelerometer_ios_data(inputDataPath, dataFilename3)
    accelerometer.to_csv(os.path.join(featurePath, featureFilename3), header=True, index=False)

    gyroscope = process_gyroscope_ios_data(inputDataPath, dataFilename4)
    gyroscope.to_csv(os.path.join(featurePath, featureFilename4), header=True, index=False)

    # reading preprocessed files:
    # lockstate = pd.read_csv(os.path.join(featurePath, "ios_Lock_state_processed_for_sleepFeatures_allNoLoc_20220614_125752AM.csv"))

    # brightness = pd.read_csv(os.path.join(featurePath, "ios_Brightness_processed_for_sleepFeatures_allNoLoc_20220614_111633AM.csv"))

    # accelerometer = pd.read_csv(os.path.join(featurePath, "ios_Accelerometer_processed_for_sleepFeatures_allNoLoc_20220614_125752AM.csv"))

    # gyroscope = pd.read_csv(os.path.join(featurePath, "ios_Gyroscope_processed_for_sleepFeatures_allNoLoc_20220614_125752AM.csv"))


    sleepFeatures = combine_ios_features(lockstate, brightness, accelerometer, gyroscope)    
    #saving the file
    sleepFeatures.to_csv(os.path.join(featurePath, finalFeatureFilename), header=True, index=False)
    print("Extraction of Sleep features completed")


if __name__ == "__main__":
    # config
    inputDataPath1 = "../../data/allNoLoc"
    # inputDataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"

    strTime = time.time()
    getIosSleepFeatures(inputDataPath1, featurePath)
    endTime = time.time()

    # strTime = time.time()
    # getIosSleepFeatures(inputDataPath2, featurePath)
    # endTime = time.time()

    print(f"run time: {round((endTime - strTime)/60, 2)}")