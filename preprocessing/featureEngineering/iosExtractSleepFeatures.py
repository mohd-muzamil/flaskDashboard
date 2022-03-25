"""
Script for extracting below sleep related features using IOS lockstate, brightness, accelerometer and gyroscope data

Feature1(sleepStartTime): Estimated start time of the sleep
Feature2(sleepEndTime): Estimated end time of the sleep
Feature3(sleepDuration): Estimated sleep duration

input/output file names need to be specifed in the code below #config
"""

from imports import *


def sleep_analysis(df, sleep_break=30):
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
    sleep_start_time = '{:02d}:{:02d}'.format(*divmod(int(sleep_start*10), 60))
    sleep_end_time = '{:02d}:{:02d}'.format(*divmod(int(sleep_end*10), 60))
#     print(f"sleep_duration:{sleep_duration}hrs sleep_start:{sleep_start}, sleep_end:{sleep_end}, no_sleep_interruptions:{no_sleep_interruptions}, duration_of_sleep_interruptions:{duration_of_sleep_interruptions}")
    
    # return the sleep times detected by the algorithm
    return  sleep_duration, sleep_start_time, sleep_end_time


def getIosSleepFeatures(dataPath, featurePath):
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
    # screen state data
    dataFilename1 = "Lock_state.csv"
    # dataFilename1 = "Lock_state_temp.csv"
    # brightness data
    dataFilename2 = "Brightness.csv"
    # dataFilename2 = "Brightness_temp.csv"
    # accelerometer data
    dataFilename3 = "Accelerometer.csv"
    # dataFilename3 = "Accelerometer_temp.csv"
    # gyroscope data
    dataFilename4 = "Gyroscope.csv"
    # dataFilename4 = "Gyroscope_temp.csv"


    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "ios_sleep_features_" + dataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(dataPath, dataFilename1))):
        sys.exit(f"{dataFilename1} file does not exist in {dataPath} folder \nscript aborted")
    
    if not (os.path.exists(os.path.join(dataPath, dataFilename2))):
        sys.exit(f"{dataFilename2} file does not exist in {dataPath} folder \nscript aborted")
    
    if not (os.path.exists(os.path.join(dataPath, dataFilename3))):
        sys.exit(f"{dataFilename3} file does not exist in {dataPath} folder \nscript aborted")

    if not (os.path.exists(os.path.join(dataPath, dataFilename4))):
        sys.exit(f"{dataFilename4} file does not exist in {dataPath} folder \nscript aborted")


    ##################################################################
    # pre processing screenstate data
    ##################################################################
    # read file with a header
    header_list = ["id", "participant", "attribute", "lockstate", "timestamp", "uploadtimestamp"]
    screenstate = pd.read_csv(os.path.join(dataPath, dataFilename1), sep="|")
    screenstate.columns = header_list

    #change time to Halifax time
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"], utc=True)
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"]).dt.tz_convert(tz='America/Halifax')
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"], utc=False)

    #add new columns to help extract features
    screenstate["date"] = screenstate["timestamp"].dt.date
    screenstate["timeblock"] = (screenstate["timestamp"].dt.hour * 6) + (screenstate["timestamp"].dt.minute/10).astype(int)

    # sort data, remove duplicates and drop unecessary columns
    screenstate = screenstate.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    screenstate.drop_duplicates(subset=["participant", "timestamp", "lockstate"], keep="last", inplace=True)
    screenstate.drop(["id", "timestamp", "attribute", "uploadtimestamp"], axis=1, inplace=True)
    
    #keeping only those rows which indicate screen usage
    screenstate = screenstate[(screenstate.lockstate == "LOCKED") | (screenstate.lockstate == "UNLOCKED")]

    # get the number of lock events in that time-block
    # screenstate = screenstate.groupby(["participant", "date", "timeblock"]).agg(lambda x:x.value_counts().index[0]).reset_index()

    # imputing missing values
    screenstateImputed = pd.DataFrame()
    participants = screenstate.participant.unique()
    # participants = ["PROSIT0004","PROSIT001", "PROSIT00A"]
    for participant in participants:
        screenstate_participant = screenstate[screenstate.participant == participant].copy()

        timeblock = [i for i in range(0,144)]
        allMinutes = pd.DataFrame({"timeblock":timeblock})

        dates = screenstate_participant.date.unique()
        for date in dates:
            screenstate_participant_date = screenstate_participant[screenstate_participant.date == date].copy()    
            screenstate_participant_date = pd.merge(screenstate_participant_date, allMinutes, how="right", on="timeblock")

            screenstate_participant_date.ffill(inplace=True)
            screenstate_participant_date.bfill(inplace=True)
            screenstateImputed = pd.concat([screenstateImputed, screenstate_participant_date], axis=0)

            break
        break
    print("Preprocessing completed for screenstate data")
    
    
    ##################################################################
    # pre processing brightness data
    ##################################################################
    # read file with a header
    header_list = ["id", "participant", "attribute", "brightnesslevel", "timestamp", "uploadtimestamp"]
    brightness = pd.read_csv(os.path.join(dataPath, dataFilename2), sep="|", header=None)
    brightness.columns = header_list
    
    #change time to Halifax time
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=True)
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"]).dt.tz_convert(tz='America/Halifax')
    brightness["timestamp"] = pd.to_datetime(brightness["timestamp"], utc=False)

    #add new columns to help extract features
    brightness["date"] = brightness["timestamp"].dt.date
    brightness["timeblock"] = (brightness["timestamp"].dt.hour * 6) + (np.floor(brightness["timestamp"].dt.minute / 10)).astype(int)

    # sort data, remove duplicates and drop unecessary columns
    brightness = brightness.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    brightness.drop_duplicates(subset=["participant", "timestamp", "brightnesslevel"], keep="last", inplace=True)
    brightness.drop(["id", "timestamp", "attribute", "uploadtimestamp"], axis=1, inplace=True)
    
    brightness = brightness.groupby(["participant", "date", "timeblock"]).aggregate(["mean", "std", "min", "max"]).reset_index()

    header_list = ["participant", "date", "timeblock", "brightness_mean", "brightness_std", "brightness_min", "brightness_max"]
    brightness.columns = header_list
    print("Preprocessing completed for brightness data")


    ##################################################################
    # pre processing accelerometer data
    ##################################################################
    # read file with header
    header_list = ["id", "participant", "attribute", "accx", "accy", "accz", "timestamp", "uploadtimestamp"]
    accelerometer = pd.read_csv(os.path.join(dataPath, dataFilename3), sep="|", header=None)
    accelerometer.columns = header_list

    #change time to Halifax time
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=True)
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"]).dt.tz_convert(tz='America/Halifax')
    accelerometer["timestamp"] = pd.to_datetime(accelerometer["timestamp"], utc=False)

    #add new columns to help extract features
    accelerometer["date"] = accelerometer["timestamp"].dt.date
    accelerometer["timeblock"] = (accelerometer["timestamp"].dt.hour * 6) + (np.floor(accelerometer["timestamp"].dt.minute / 10)).astype(int)

    # sort data, remove duplicates and drop unecessary columns
    accelerometer = accelerometer.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    accelerometer.drop_duplicates(subset=["participant", "timestamp", "accx", "accy", "accz"], keep="last", inplace=True)
    accelerometer.drop(["id", "timestamp", "attribute", "uploadtimestamp"], axis=1, inplace=True)

    # ENMO : Euclidean Norm Minus One (ENMO) with negative values rounded to zero in g has been shown to correlate with the magnitude of acceleration and human energy expenditure
    accelerometer["acc"] = np.sqrt((accelerometer["accx"]**2) + (accelerometer["accy"]**2) + (accelerometer["accz"]**2))
    # accelerometer["acc"] = np.maximum(0, (np.sqrt((accelerometer["accelerationx"]**2) + (accelerometer["accelerationy"]**2) + (accelerometer["accelerationz"]**2)) - 1))

    # dropping the accelerometer columns
    accelerometer.drop(["accx", "accy", "accz"], axis=1, inplace=True)

    #mean #std min max
    accelerometer = accelerometer.groupby(["participant", "date", "timeblock"]).agg(["mean"]).reset_index()
    accelerometer.columns = ['_'.join(col).strip() if col[1]!="" else col[0] for col in accelerometer.columns.values ]

    print("Preprocessing completed for accelerometer data")


    ##################################################################
    # pre processing gyroscope data
    ##################################################################
    # read file with header
    header_list = ["id", "participant", "attribute", "gyrox", "gyroy", "gyroz", "timestamp", "uploadtimestamp"]
    gyroscope = pd.read_csv(os.path.join(dataPath, dataFilename4), sep="|", header=None)
    gyroscope.columns = header_list

    #change time to Halifax time
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=True)
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"]).dt.tz_convert(tz='America/Halifax')
    gyroscope["timestamp"] = pd.to_datetime(gyroscope["timestamp"], utc=False)

    #add new columns to help extract features
    gyroscope["date"] = gyroscope["timestamp"].dt.date
    gyroscope["time"] = gyroscope["timestamp"].dt.strftime('%H:%M:%S')
    gyroscope["timeblock"] = (gyroscope["timestamp"].dt.hour * 6) + (np.floor(gyroscope["timestamp"].dt.minute / 10)).astype(int)

    # sort data, remove duplicates and drop unecessary columns
    gyroscope = gyroscope.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    gyroscope.drop_duplicates(subset=["participant", "timestamp", "gyrox", "gyroy", "gyroz"], keep="last", inplace=True)
    gyroscope.drop(["id", "timestamp", "attribute", "uploadtimestamp"], axis=1, inplace=True)

    # ENMO : Euclidean Norm Minus One (ENMO) with negative values rounded to zero in g has been shown to correlate with the magnitude of acceleration and human energy expenditure
    gyroscope["gyr"] = np.sqrt((gyroscope["gyrox"]**2) + (gyroscope["gyroy"]**2) + (gyroscope["gyroz"]**2))
    # gyroscope["gyr"] = np.maximum(0, (np.sqrt((gyroscope["gyrox"]**2) + (gyroscope["gyroy"]**2) + (gyroscope["gyroz"]**2)) - 1))

    # dropping the gyroscope columns
    gyroscope.drop(["gyrox", "gyroy", "gyroz"], axis=1, inplace=True)

    #mean #std min max
    gyroscope = gyroscope.groupby(["participant", "date", "timeblock"]).agg(["mean"]).reset_index()
    gyroscope.columns = ['_'.join(col).strip() if col[1]!="" else col[0] for col in gyroscope.columns.values ]

    print("Preprocessing completed for gyroscope data")


    ##################################################################
    # combining all the sensor data to prepare sleep data
    ##################################################################
    dfs = [screenstate, brightness, accelerometer, gyroscope]

    sleep_data = reduce(lambda left,right: pd.merge(left,right,on=["participant", "date", "timeblock"], how="outer"), dfs)
    sleep_data.fillna(0, inplace=True)

    # for participant in sleep_data.participant.unique():
    #     sleep_data.loc[sleep_data.participant == participant,'date_num'] = pd.factorize(sleep_data.loc[sleep_data.participant == participant, "date"])[0] + 1


    # defining a dataframe to store the sleep features
    sleepFeatures = pd.DataFrame(columns=["participant", "date", "date_num", "sleeping_hrs", "sleep_start_time", "sleep_end_time"])

    participants = sleep_data.groupby('participant').size().reset_index(name="cnt").sort_values("cnt", ascending=False).participant.unique()
    index = 0
    for participant in tqdm(participants):
        sleep_data_participant = sleep_data[sleep_data.participant == participant].copy()
        sleep_data_participant['date_num'] = pd.factorize(sleep_data_participant["date"])[0] + 1
        for date_num in sleep_data_participant.date_num.unique():
            sleep_data_participant_date = sleep_data_participant[sleep_data_participant.date_num == date_num].copy()

            # set values with less than 0.1 quantile values to 0 to remove noise
            # sleep_data_participant_date.loc[sleep_data_participant_date["acc_mean"] <= sleep_data_participant_date["acc_mean"].quantile(0.1), "acc_mean"] = 0
            # sleep_data_participant_date.loc[sleep_data_participant_date["gyro_mean"] <= sleep_data_participant_date["gyro_mean"].quantile(0.1), "gyro_mean"] = 0

            # filtering out only those timeblocks which show device usage
            # sleep_data_participant_date = sleep_data_participant_date[(sleep_data_participant_date["lockstate"] == "LOCKED") & (sleep_data_participant_date["brightness_mean" == 0]) & (sleep_data_participant_date["acc_mean"] == 0) & (sleep_data_participant_date["gyro_mean"] == 0)]
            
            sleep_duration, sleep_start_time, sleep_end_time = sleep_analysis(sleep_data_participant_date, sleep_break=30)
            sleepFeatures.loc[index] = [participant, sleep_data_participant_date.date.unique()[0], date_num, sleep_duration, sleep_start_time, sleep_end_time]
            index += 1
    
    #saving the file
    sleepFeatures.to_csv(os.path.join(featurePath, featureFilename), header=True, index=False)

    print("Extraction of Sleep features compelted")


if __name__ == "__main__":
    # config
    dataPath1 = "/csv/backup_frigg1"
    dataPath2 = "/csv/backup"
    featurePath = "/csv/features"

    strTime = time.time()
    getIosSleepFeatures(dataPath1, featurePath)
    endTime = time.time()

    strTime = time.time()
    getIosSleepFeatures(dataPath2, featurePath)
    endTime = time.time()

    print(f"run time: {round((endTime - strTime)/60, 2)}")