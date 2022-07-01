"""
#################################################################################################################
Script for extracting below sleep related features using android lockstate, brightness, accelerometer and gyroscope data

Feature1(sleepStartTime): Estimated start time of the sleep
Feature2(sleepEndTime): Estimated end time of the sleep
Feature3(sleepDuration): Estimated sleep duration

input/output file names need to be specifed in the code below #config
#################################################################################################################
"""

from imports import *

# Filtered participantIds from another notebook. Only data from these will be analysed
filteredParticipantIds = []
filteredParticipantIds = ['aPROSITC0060', 'aPROSITC0064', 'aPROSITC00D', 'aPROSITC00M', 'aPROSITC0103', 'aPROSITC0107', 'aPROSITC0116', 'aPROSITC0118', 'aPROSITC0119', 'aPROSITC0128', 'aPROSITC0130', 'aPROSITC0131', 'aPROSITC0134', 'aPROSITC0144', 'aPROSITC0175', 'aPROSITC0188', 'aPROSITC0200', 'aPROSITC0211', 'aPROSITC0225', 'aPROSITC0229', 'aPROSITC0235', 'aPROSITC0237', 'aPROSITC0252', 'aPROSITC0260', 'aPROSITC0275', 'aPROSITC0279', 'aPROSITC0290', 'aPROSITC0295', 'aPROSITC0301', 'aPROSITC0303', 'aPROSITC0310', 'aPROSITC0326', 'aPROSITC0357', 'aPROSITC0376', 'aPROSITC0379', 'aPROSITC0398', 'aPROSITC0414', 'aPROSITC0416', 'aPROSITC0433', 'aPROSITC0436', 'aPROSITC0437', 'aPROSITC0457', 'aPROSITC0483', 'aPROSITC0497', 'aPROSITC0645', 'aPROSITC0739', 'aPROSITC0753', 'aPROSITC0774', 'aPROSITC0805', 'aPROSITC0838', 'aPROSITC0874', 'aPROSITC1063', 'aPROSITC1065', 'aPROSITC1069', 'aPROSITC1134', 'aPROSITC1147', 'aPROSITC1149', 'aPROSITC1154', 'aPROSITC1155', 'aPROSITC1156', 'aPROSITC1165', 'aPROSITC1170', 'aPROSITC1171', 'aPROSITC1172', 'aPROSITC1175', 'aPROSITC1182', 'aPROSITC1201', 'aPROSITC1204', 'aPROSITC1205', 'aPROSITC1208', 'aPROSITC1215', 'aPROSITC1226', 'aPROSITC1230', 'aPROSITC1233', 'aPROSITC1241', 'aPROSITC1242', 'aPROSITC1255', 'aPROSITC1271', 'aPROSITC1273', 'aPROSITC1277', 'aPROSITC1283', 'aPROSITC1302', 'aPROSITC1303', 'aPROSITC1306', 'aPROSITC1309', 'aPROSITC1312', 'aPROSITC1315', 'aPROSITC1322', 'aPROSITC1337', 'aPROSITC1349', 'aPROSITC1363', 'aPROSITC1368', 'aPROSITC1374', 'aPROSITC1378', 'aPROSITC1381', 'aPROSITC1387', 'aPROSITC1388', 'aPROSITC1392', 'aPROSITC1399', 'aPROSITC1402', 'aPROSITC1403', 'aPROSITC1419', 'aPROSITC1423', 'aPROSITC1425', 'aPROSITC1429', 'aPROSITC1430', 'aPROSITC1431', 'aPROSITC1433', 'aPROSITC1439', 'aPROSITC1444', 'aPROSITC1458', 'aPROSITC1462', 'aPROSITC1473', 'aPROSITC1489', 'aPROSITC1504', 'aPROSITC1536', 'aPROSITC1541', 'aPROSITC1542', 'aPROSITC1565', 'aPROSITC1568', 'aPROSITC1575', 'aPROSITC1604', 'aPROSITC1613', 'aPROSITC1618', 'aPROSITC1620', 'aPROSITC1628', 'aPROSITC1630', 'aPROSITC1638', 'aPROSITC1688', 'aPROSITC1694', 'aPROSITC1697', 'aPROSITC1699', 'aPROSITC1701', 'aPROSITC1709', 'aPROSITC1713', 'aPROSITC1718', 'aPROSITC1734', 'aPROSITC1745', 'aPROSITC1747', 'aPROSITC1770', 'aPROSITC1778', 'aPROSITC1780', 'aPROSITC1787', 'aPROSITC1791', 'aPROSITC1793', 'aPROSITC1796', 'aPROSITC1799', 'aPROSITC1805', 'aPROSITC1818', 'aPROSITC1822', 'aPROSITC1840', 'aPROSITC1855', 'aPROSITC1856', 'aPROSITC1862', 'aPROSITC1873', 'aPROSITC1887', 'aPROSITC1893', 'aPROSITC1903', 'aPROSITC1905', 'aPROSITC1921', 'aPROSITC1928', 'aPROSITC1930', 'aPROSITC1931', 'aPROSITC1941', 'aPROSITC1944', 'aPROSITC1949', 'aPROSITC1963', 'aPROSITC1986', 'aPROSITC1994', 'aPROSITC2009', 'aPROSITC2010', 'aPROSITC2019', 'aPROSITC2039', 'aPROSITC2044', 'aPROSITC2067', 'aPROSITC2089', 'aPROSITC2095', 'aPROSITC2098', 'aPROSITC2101', 'aPROSITC2102', 'aPROSITC2115', 'aPROSITC2130', 'aPROSITC2132', 'aPROSITC2143', 'aPROSITC2160', 'aPROSITC2177', 'aPROSITC2180', 'aPROSITC2185', 'aPROSITC2193', 'aPROSITC2226', 'aPROSITC2232', 'aPROSITC2237', 'aPROSITC2241', 'aPROSITC2255', 'aPROSITC2256', 'aPROSITC2268', 'aPROSITC2285', 'aPROSITC2292', 'aPROSITC2295', 'aPROSITC2298', 'aPROSITC2304', 'aPROSITC2348', 'aPROSITC2349', 'aPROSITC2353', 'aPROSITC2375', 'aPROSITC2392', 'aPROSITC2725', 'aPROSITC2742', 'aPROSITC2743', 'aPROSITC2780', 'aPROSITC2797', 'aPROSITC2825', 'aPROSITC2836', 'aPROSITC2848', 'aPROSITC2876', 'aPROSITC2954', 'aPROSITC2955', 'aPROSITC2973', 'aPROSITC2987', 'aPROSITC2990', 'aPROSITC2992', 'aPROSITC2994', 'aPROSITC2998', 'aPROSITC3000', 'aPROSITC3020', 'aPROSITC3021', 'aPROSITC3036', 'aPROSITC3050', 'aPROSITC3058', 'aPROSITC3087', 'aPROSITC3089', 'aPROSITC3097', 'aPROSITC3108', 'aPROSITC3129', 'aPROSITC3222', 'aPROSITC3232', 'aPROSITC3298']


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
def process_lockstate_android_data(inputDataPath, dataFilename):
    print(f"Processing Lockstate android data from '{inputDataPath}'...")
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
                lockstate_participantId_date = lockstate_participantId_date[(lockstate_participantId_date["lck"] == "screen_on") | (lockstate_participantId_date["lck"] == "screen_off")].copy()
                
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
# pre processing accelerometer data
######################################################################################
def process_accelerometer_android_data(inputDataPath, dataFilename):    
    print(f"Processing Accelerometer android data from '{inputDataPath}'...")
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
def process_gyroscope_android_data(inputDataPath, dataFilename):    
    print(f"Processing Gyroscope android data from '{inputDataPath}'...")
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
def combine_android_features(lockstate, accelerometer, gyroscope):
    dfs = [lockstate, accelerometer, gyroscope]

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
            sleep_data_participantId_date = sleep_data_participantId_date[(sleep_data_participantId_date.lck == "screen_off") & (sleep_data_participantId_date.acc == 0) & (sleep_data_participantId_date.gyro == 0)]
            
            if sleep_data_participantId_date.shape[0]>0:
                sleep_duration, sleep_start_time, sleep_end_time = sleep_analysis(sleep_data_participantId_date, sleep_break=30)
                sleepFeatures.loc[index] = [participantId, sleep_data_participantId_date.date.unique()[0], date_num, sleep_duration, sleep_start_time, sleep_end_time]
                index += 1
    
    return sleepFeatures

    
def getandroidSleepFeatures(inputDataPath, featurePath):
    '''
    considering below conditions to assign a sleep state to a time block which is chosen as 10mins
    # screen state  - "screen_off"
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
    # dataFilename1 = "powerState_android.csv"
    # # dataFilename1 = "Lock_state_temp_android.csv"
    # featureFilename1 = f"android_Lock_state_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # brightness data
    # dataFilename2 = "Brightness_android.csv"
    # dataFilename2 = "Brightness_temp_android.csv"
    # featureFilename2 = f"android_Brightness_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # accelerometer data
    # dataFilename3 = "accelerometer_m_s2__x_y_z_android.csv"
    # # dataFilename3 = "Accelerometer_temp_android.csv"
    # featureFilename3 = f"android_Accelerometer_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    # # gyroscope data
    # dataFilename4 = "gyroscope_rad_s__x_y_z_android.csv"
    # # dataFilename4 = "Gyroscope_temp_android.csv"
    # featureFilename4 = f"android_Gyroscope_processed_for_sleepFeatures_{dbName}_{timestamp}.csv"

    finalFeatureFilename = f"android_sleep_features_{dbName}_{timestamp}_android.csv"

    # if not (os.path.exists(os.path.join(inputDataPath, dataFilename1))):
    #     sys.exit(f"{dataFilename1} file does not exist in {inputDataPath} folder \nscript aborted")
    
    # # if not (os.path.exists(os.path.join(inputDataPath, dataFilename2))):
    # #     sys.exit(f"{dataFilename2} file does not exist in {inputDataPath} folder \nscript aborted")
    
    # if not (os.path.exists(os.path.join(inputDataPath, dataFilename3))):
    #     sys.exit(f"{dataFilename3} file does not exist in {inputDataPath} folder \nscript aborted")

    # if not (os.path.exists(os.path.join(inputDataPath, dataFilename4))):
    #     sys.exit(f"{dataFilename4} file does not exist in {inputDataPath} folder \nscript aborted")


    # # Preprocessing and saving the raw sensor data
    # lockstate = process_lockstate_android_data(inputDataPath, dataFilename1)
    # lockstate.to_csv(os.path.join(featurePath, featureFilename1), header=True, index=False)

    # # brightness = process_brightness_android_data(inputDataPath, dataFilename2)
    # # brightness.to_csv(os.path.join(featurePath, featureFilename2), header=True, index=False)

    # accelerometer = process_accelerometer_android_data(inputDataPath, dataFilename3)
    # accelerometer.to_csv(os.path.join(featurePath, featureFilename3), header=True, index=False)

    # gyroscope = process_gyroscope_android_data(inputDataPath, dataFilename4)
    # gyroscope.to_csv(os.path.join(featurePath, featureFilename4), header=True, index=False)

    # reading preprocessed files:
    lockstate = pd.read_csv(os.path.join(featurePath, "android_Lock_state_processed_for_sleepFeatures_allNoLoc_20220630_054948PM.csv"))

    accelerometer = pd.read_csv(os.path.join(featurePath, "android_Accelerometer_processed_for_sleepFeatures_allNoLoc_20220630_054948PM.csv"))

    gyroscope = pd.read_csv(os.path.join(featurePath, "android_Gyroscope_processed_for_sleepFeatures_allNoLoc_20220630_054948PM.csv"))


    sleepFeatures = combine_android_features(lockstate, accelerometer, gyroscope)    
    #saving the file
    sleepFeatures.to_csv(os.path.join(featurePath, finalFeatureFilename), header=True, index=False)
    print("Extraction of Sleep features completed")


if __name__ == "__main__":
    # config
    inputDataPath1 = "../../data/allNoLoc"
    # inputDataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"

    strTime = time.time()
    getandroidSleepFeatures(inputDataPath1, featurePath)
    endTime = time.time()

    # strTime = time.time()
    # getandroidSleepFeatures(inputDataPath2, featurePath)
    # endTime = time.time()

    print(f"run time: {round((endTime - strTime)/60, 2)}")