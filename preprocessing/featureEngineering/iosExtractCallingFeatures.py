# This script is meant for extracting Call related features from ios user data.
# <br>format of the features will be as below.
# <li>Feature1: Number of Missed calls in a daily section
# <li>Feature2: Number of Dialled but not recieved calls in daily sections
# <li>Feature3: Number of Incoming calls in a daily section
# <li>Feature4: Number of Outgoing calls in a daily section
# <li>Feature5: Total number of calling events in a daily section
# <li>Feature6: Min duration of Incoming calls in a daily section
# <li>Feature7: Min duration of Outgoing calls in a daily section
# <li>Feature8: Max duration of Incoming calls in a daily section
# <li>Feature9: Max duration of Outgoing calls in a daily section
# <li>Feature10: Total duration of Incoming call in a daily section
# <li>Feature11: Total duration of Outgoing calls in a daily section
# <li>Feature12: Total duration of any calls in a daily section
    
# <br>prticipant, device, date, weekday, week, dailysection, date_num, recorded_instances, no_missed_calls

# ****NOTES****
# <br>call duration is in minutes
# <br>check for call_hold condition in between calls, not implemented in the code.

from imports import *

def getIosCallingFeatures(dataPath, featurePath):
    """
    dataPath: path to folder which has ios call data
    featurePath: path to store the extracted features
    """
    print("Begin extraction - Calling features")

    dataFilename = "Call.csv"
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "ios_call_features_" + dataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(dataPath, dataFilename))):
        sys.exit("{dataFilename} file does not exist in {dataPath} folder")

    # Call IOS data
    header_list = ["id", "participant", "attribute", "callevent", "timestamp", "uploadtimestamp"]
    #read ios file
    call = pd.read_csv(os.path.join(dataPath, dataFilename), sep="|", header=None)
    call.columns = header_list
    call['device'] = "ios"

    #change time to Halifax time
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=True)
    call["timestamp"] = pd.to_datetime(call["timestamp"]).dt.tz_convert(tz='America/Halifax')
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=False)

    #add some new columns to help extract features
    call["date"] = call["timestamp"].dt.date
    call["time"] = call["timestamp"].dt.strftime('%H:%M:%S')

    #Drop duplicates and sort as per timestamp
    call = call.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    call.drop_duplicates(subset=["participant", "timestamp", "callevent"], keep="last", inplace=True)
    call.drop(["id", "attribute", "uploadtimestamp"], axis=1, inplace=True)

    #keeping only those rows which indicate calling events
    call = call[call.callevent.isin(['CALL_INCOMING', 'CALL_CONNECTED', 'CALL_DISCONNECTED', 'CALL_DIALING', 'CALL_ON_HOLD'])]

    call_processed = pd.DataFrame()

    """
    filter over participant, date, daily_section:
    check if df is not empty
    remove duplicates
    add first and last rows
    append to processed_df
    ****call duration for features is in minutes****
    """ 
    participants = call.participant.unique()
    # participants = ["PROSIT0004","PROSIT001", "PROSIT00A"]
    for participant in tqdm(participants):
        call_participant = call[call.participant == participant].copy()
        dates = call_participant.date.unique()
        for i, date in enumerate(dates):
            call_participant_date = call_participant[call_participant.date == date].copy()
                
            if call_participant_date.shape[0] > 1:
                #first_event in a daily section
                first_event = call_participant_date.iloc[:1, :].copy()
                first_event.lockstate = "CALL_CONNECTED"
                x
                #last_event in a daily section
                last_event = call_participant_date.iloc[-1:, :].copy()
                last_event.lockstate = "CALL_DISCONNECTED"
                
                call_participant_date = pd.concat([first_event, call_participant_date, last_event], ignore_index=True)
                call_participant_date["duration"] = 0
                call_participant_date["calltype"] = ""
                
                #logic to call_type and duration_time
                call_participant_date["callevent_roll1"] = call_participant_date.callevent.shift(-1)
                call_participant_date["timestamp_roll1"] = call_participant_date.timestamp.shift(-1)
                call_participant_date["callevent_roll2"] = call_participant_date.callevent.shift(-2)
                call_participant_date["timestamp_roll2"] = call_participant_date.timestamp.shift(-2)

                index = (call_participant_date["callevent"] == "CALL_INCOMING" ) & (call_participant_date["callevent_roll1"] == "CALL_DISCONNECTED" )
                call_participant_date.loc[index, "duration"] = (call_participant_date[index]["timestamp_roll1"] - call_participant_date[index]["timestamp"]).astype('timedelta64[m]')
                call_participant_date.loc[index, "calltype"] = "missed"
                call_participant_date.loc[index, "start_time"] = call_participant_date.loc[index, "timestamp"].dt.time
                call_participant_date.loc[index, "end_time"] = call_participant_date.loc[index, "timestamp_roll1"].dt.time

                index = (call_participant_date["callevent"] == "CALL_DIALING" ) & (call_participant_date["callevent_roll1"] == "CALL_DISCONNECTED" )
                call_participant_date.loc[index, "duration"] = (call_participant_date[index]["timestamp_roll1"] - call_participant_date[index]["timestamp"]).astype('timedelta64[m]')
                call_participant_date.loc[index, "calltype"] = "rejected"
                call_participant_date.loc[index, "start_time"] = call_participant_date.loc[index, "timestamp"].dt.time
                call_participant_date.loc[index, "end_time"] = call_participant_date.loc[index, "timestamp_roll1"].dt.time

                index = (call_participant_date["callevent"] == "CALL_INCOMING" ) & (call_participant_date["callevent_roll1"] == "CALL_CONNECTED" ) & (call_participant_date["callevent_roll2"] == "CALL_DISCONNECTED")
                call_participant_date.loc[index, "duration"] = (call_participant_date[index]["timestamp_roll2"] - call_participant_date[index]["timestamp_roll1"]).astype('timedelta64[m]')
                call_participant_date.loc[index, "calltype"] = "incoming"
                call_participant_date.loc[index, "start_time"] = call_participant_date.loc[index, "timestamp_roll1"].dt.time
                call_participant_date.loc[index, "end_time"] = call_participant_date.loc[index, "timestamp_roll2"].dt.time

                index = (call_participant_date["callevent"] == "CALL_DIALING" ) & (call_participant_date["callevent_roll1"] == "CALL_CONNECTED" ) & (call_participant_date["callevent_roll2"] == "CALL_DISCONNECTED")
                call_participant_date.loc[index, "duration"] = (call_participant_date[index]["timestamp_roll2"] - call_participant_date[index]["timestamp_roll1"]).astype('timedelta64[m]')
                call_participant_date.loc[index, "calltype"] = "outgoing"
                call_participant_date.loc[index, "start_time"] = call_participant_date.loc[index, "timestamp_roll1"].dt.time
                call_participant_date.loc[index, "end_time"] = call_participant_date.loc[index, "timestamp_roll2"].dt.time
                
                call_processed = pd.concat([call_processed, call_participant_date], ignore_index=True)

    #checking if there are any rows with negative call durations
    # call_processed[call_processed.duration < 0]
    # call_processed = call_processed[call_processed["duration"] >= 0]

    # missed rejected incoming outgoing
    df1 = (call_processed[call_processed.calltype=="missed"].groupby(["participant", "date"]).size().reset_index(name="no_of_missed_calls"))
    df2 = (call_processed[call_processed.calltype=="rejected"].groupby(["participant", "date"]).size().reset_index(name="no_of_rejected_calls"))
    df3 = (call_processed[call_processed.calltype=="incoming"].groupby(["participant", "date"]).size().reset_index(name="no_of_incoming_calls"))
    df4 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participant", "date"]).size().reset_index(name="no_of_outgoing_calls"))
    df5 = (call_processed[call_processed.calltype.isin(["missed", "rejected", "incoming", "outgoing"])].groupby(["participant", "date"]).size().reset_index(name="total_no_of_calls"))

    df6 = (call_processed[call_processed.calltype=="incoming"].groupby(["participant", "date"])["duration"].agg("min").reset_index(name="min_duration_of_single_incoming_call"))
    df7 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participant", "date"])["duration"].agg("min").reset_index(name="min_duration_of_single_outgoing_call"))
    df8 = (call_processed[call_processed.calltype=="incoming"].groupby(["participant", "date"])["duration"].agg("max").reset_index(name="max_duration_of_single_incoming_call"))
    df9 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participant", "date"])["duration"].agg("max").reset_index(name="max_duration_of_single_outgoing_call"))

    df10 = (call_processed[call_processed.calltype=="incoming"].groupby(["participant", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_incoming_calls"))
    df11 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participant", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_outgoing_calls"))
    df12 = (call_processed[call_processed.calltype.isin(["incoming", "outgoing"])].groupby(["participant", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_all_calls"))

    df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

    df1[['key1', 'key2']] = df1[["participant", "date"]]
    df2[['key1', 'key2']] = df2[["participant", "date"]]
    df3[['key1', 'key2']] = df3[["participant", "date"]]
    df4[['key1', 'key2']] = df4[["participant", "date"]]
    df5[['key1', 'key2']] = df5[["participant", "date"]]
    df6[['key1', 'key2']] = df6[["participant", "date"]]
    df7[['key1', 'key2']] = df7[["participant", "date"]]
    df8[['key1', 'key2']] = df8[["participant", "date"]]
    df9[['key1', 'key2']] = df9[["participant", "date"]]
    df10[['key1', 'key2']] = df10[["participant", "date"]]
    df11[['key1', 'key2']] = df11[["participant", "date"]]
    df12[['key1', 'key2']] = df12[["participant", "date"]]

    df = df1.merge(df2, how="outer")
    for next_df in df_list[2:]:
        df = df.merge(next_df, how="outer")

    df= df.fillna(0)
    df = df.sort_values(["participant", "date"]).reset_index(drop=True)

    # Dropping the key values used for outer joins
    df.drop(['key1', 'key2'], axis=1, inplace=True)
    df = df[(df.total_no_of_calls > 0) & (df.total_duration_of_all_calls > 0)].reset_index(drop=True)

    # save the file
    df = df.round(decimals=2)
    df.to_csv(os.path.join(featurePath, featureFilename), header=True, index=False)
    print("End")


if __name__ == "__main__":
    dataPath1 = "/csv/backup_frigg1"
    dataPath2 = "/csv/backup"
    featurePath = "/csv/features"

    strTime = time.time()
    getIosCallingFeatures(dataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}")

    # strTime = time.time()
    # getIosCallingFeatures(dataPath2, featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}")``