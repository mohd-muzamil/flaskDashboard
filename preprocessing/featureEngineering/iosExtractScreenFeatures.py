# This script is meant for extracting screen related features for IOS user data.
# <br>format of the features are as shown below
# <ul>Screen Lock/Unlock Features--------
# <li>Feature1: No of screen unlocks in a daily section
# <li>Feature2: First screen unlock event in a day
# <li>Feature3: Last screen lock event in a day
# <li>Feature4: Maximum screen unlock time in a daily section
# <li>Feature5: Maximum screen lock time in a daily section
# <li>Feature6: Total screen unlock time in a daily section
# <li>Feature7: Total screen lock time in a daily section
# <br>participant, device, date, weekday, week, dailysection, ate_num, recorded_instances, no_of_unlocks, max_screen_on_time, max_screen_off_time,total_screen_on_time, total_screen_off_time, first_screen_unlock_time, last_screen_lock_time


from imports import *

def getIosScreenFeatures(dataPath, featurePath):
    """
    Feature Engineering - "Screenstate (LOCKED/UNLOCKED)"
    This script will read files from predefined location and write feature data into predefined location

    dataPath: path to folder which has ios screen data
    featurePath: path to store the extracted features
    """

    print("Begin extraction - Screen features")
    
    dataFilename = "Lock_state.csv"
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "ios_screen_features_" + dataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(dataPath, dataFilename))):
        sys.exit("{dataFilename} file does not exist in {dataPath} folder")

    header_list = ["id", "participant", "attribute", "lockstate", "timestamp", "uploadtimestamp"]
    #read ios file
    screenstate = pd.read_csv(os.path.join(dataPath, dataFilename), sep="|", header=None)
    screenstate.columns = header_list

    #change time to Halifax time
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"], utc=True)
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"]).dt.tz_convert(tz='America/Halifax')
    screenstate["timestamp"] = pd.to_datetime(screenstate["timestamp"], utc=False)

    #add new columns to help extract features
    screenstate["date"] = screenstate["timestamp"].dt.date
    screenstate["time"] = screenstate["timestamp"].dt.strftime('%H:%M:%S')

    # decided not to filter out participants here
    # codeblock to get participants who have data greater that some range
    # filtering_df = screenstate.groupby(["participant", "date"]).size().reset_index().groupby("participant").size().reset_index(name="noOfDays")
    # filtering_df = filtering_df[(filtering_df.noOfDays >= 7) & (filtering_df.noOfDays <= 35)]
    # filtering_df = filtering_df[(filtering_df.noOfDays >= 7)]
    # filtered_participants = filtering_df.participant.unique().tolist()

    #filter the df to take only the required participants
    # screenstate = screenstate[screenstate.participant.isin(filtered_participants)].copy()

    # sort data, remove duplicates and drop unecessary columns
    screenstate = screenstate.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    screenstate.drop_duplicates(subset=["participant", "timestamp", "lockstate"], keep="last", inplace=True)
    screenstate.drop(["id", "attribute", "uploadtimestamp"], axis=1, inplace=True)

    #keeping only those rows which indicate screen usage
    screenstate = screenstate[(screenstate.lockstate == "LOCKED") | (screenstate.lockstate == "UNLOCKED")]

    df_screen_state_processed = pd.DataFrame()

    """
    filter over participant, date, daily_section:
    check if df is not empty
    remove duplicates
    add first and last rows
    append to processed_df

    """ 
    participants = screenstate.participant.unique()
    # participants = ["PROSIT0004","PROSIT001", "PROSIT00A"]
    for participant in tqdm(participants):
        screenstate_participant = screenstate[screenstate.participant == participant].copy()
        dates = screenstate_participant.date.unique()

        for i, date in enumerate(dates):
            screenstate_participant_date = screenstate_participant[screenstate_participant.date == date].copy()

            if screenstate_participant_date.shape[0] > 1:
                #add logic to remove duplicates using roll columns
                screenstate_participant_date = screenstate_participant_date[screenstate_participant_date.lockstate != screenstate_participant_date.lockstate.shift(1)]
                
                # adding first and last events to help detect screen usage from time 0 to time 1440 minutes of the day
                #first_event in a daily section
                first_event = screenstate_participant_date.iloc[:1, :].copy()
                if first_event.lockstate.item() == "LOCKED":
                    first_event.lockstate = "UNLOCKED"
                elif first_event.lockstate.item() == "UNLOCKED":
                    first_event.lockstate = "LOCKED"
                
                #last_event in a daily section
                last_event = screenstate_participant_date.iloc[-1:, :].copy()
                if last_event.lockstate.item() == "LOCKED":
                    last_event.lockstate = "UNLOCKED"
                elif last_event.lockstate.item() == "UNLOCKED":
                    last_event.lockstate = "LOCKED"
                
                screenstate_participant_date = pd.concat([first_event, screenstate_participant_date, last_event], ignore_index=True)
                screenstate_participant_date["screen_on_time"] = 0
                screenstate_participant_date["screen_off_time"] = 0
                
                #logic to calculate screen_time
                index = (screenstate_participant_date.lockstate == "UNLOCKED" ) & (screenstate_participant_date.lockstate.shift(-1) == "LOCKED" )
                screenstate_participant_date.loc[index, "screen_on_time"] = (screenstate_participant_date.timestamp.shift(-1)[index] - screenstate_participant_date.timestamp[index]).astype('timedelta64[s]')
                
                index = (screenstate_participant_date.lockstate == "LOCKED" ) & (screenstate_participant_date.lockstate.shift(-1) == "UNLOCKED" )
                screenstate_participant_date.loc[index, "screen_off_time"] = (screenstate_participant_date.timestamp.shift(-1)[index] - screenstate_participant_date.timestamp[index]).astype('timedelta64[s]')
                
                screenstate_participant_date.screen_on_time = np.round(screenstate_participant_date.screen_on_time / 60)    #use /60 here to convert time to minutes
                screenstate_participant_date.screen_off_time = np.round(screenstate_participant_date.screen_off_time / 60)  #use /60 here to convert time to minutes
                
                df_screen_state_processed = pd.concat([df_screen_state_processed, screenstate_participant_date], ignore_index=True)

    df_screen_state_processed[df_screen_state_processed.screen_on_time < 0]
    df_screen_state_processed = df_screen_state_processed[df_screen_state_processed.screen_on_time >= 0]

    df1 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "date"]).size().reset_index(name="no_of_unlocks"))
    df2 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "date"])["screen_on_time"].agg("max").reset_index(name="max_screen_on_time"))
    df3 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "date"])["screen_on_time"].agg("sum").reset_index(name="total_screen_on_time"))
    df4 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "date"])["time"].agg("min").reset_index(name="first_screen_unlock_time"))
    df5 = (df_screen_state_processed[df_screen_state_processed.lockstate=="LOCKED"].groupby(["participant", "date"])["time"].agg("max").reset_index(name="last_screen_lock_time"))

    df_list = [df1, df2, df3, df4, df5]

    df = df1.merge(df2, how="right")
    for next_df in df_list[2:]:
        df = df.merge(next_df, on=["participant", "date"], how="inner")
    
    df= df.fillna(0)
    df = df.sort_values(["participant", "date"]).reset_index(drop=True)

    df["first_screen_unlock_time"] = pd.to_datetime(df["first_screen_unlock_time"], format='%H:%M:%S')
    # df["first_screen_unlock_time"] = round((df["first_screen_unlock_time"].dt.hour * 60 + df["first_screen_unlock_time"].dt.minute)/60, 2)
    # decided to use hour for first screen on time
    # df["first_screen_unlock_time"] = df["first_screen_unlock_time"].dt.hour

    df["last_screen_lock_time"] = pd.to_datetime(df["last_screen_lock_time"], format='%H:%M:%S')
    # df["last_screen_lock_time"] = round((df["last_screen_lock_time"].dt.hour * 60 + df["last_screen_lock_time"].dt.minute)/60, 2)
    # decided to use hour for last screen on time
    # df["last_screen_lock_time"] = df["last_screen_lock_time"].dt.hour
    
    #saving the file
    df.to_csv(os.path.join(featurePath, featureFilename), header=True, index=False)
    print("End")


if __name__ == "__main__":
    dataPath1 = "/csv/backup_frigg1"
    dataPath2 = "/csv/backup"
    featurePath = "/csv/features"

    strTime = time.time()
    getIosScreenFeatures(dataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}")

    # strTime = time.time()
    # getIosScreenFeatures(dataPath2, featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}")