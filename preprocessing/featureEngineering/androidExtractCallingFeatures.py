"""
####################################################################################################
Script for extracting below call related features using android call data

Feature1: Number of Missed calls in a daily section
Feature2: Number of Dialled but not recieved calls in daily sections
Feature3: Number of Incoming calls in a daily section
Feature4: Number of Outgoing calls in a daily section
Feature5: Total number of calling events in a daily section
Feature6: Min duration of Incoming calls in a daily section
Feature7: Min duration of Outgoing calls in a daily section
Feature8: Max duration of Incoming calls in a daily section
Feature9: Max duration of Outgoing calls in a daily section
Feature10: Total duration of Incoming call in a daily section
Feature11: Total duration of Outgoing calls in a daily section
Feature12: Total duration of any calls in a daily section

*call durations are in minutes
*check for call_hold condition in between calls, not implemented in the code.

input/output file names need to be specifed in the code below #config
####################################################################################################
"""

from imports import *

def getAndroidCallingFeatures(dataPath, featurePath):
    """
    dataPath: path to folder which has android call data
    featurePath: path to store the extracted features
    """
    print("Begin extraction - Calling features")

    # config
    dataFilename = "calls__callDate_callDurationS_callType_phoneNumberHash_android.csv"
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "android_call_features_" + dataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(dataPath, dataFilename))):
        sys.exit(f"{dataFilename} file does not exist in {dataPath} folder \nscript aborted")

    # Call android data
    header_list = ["id", "participantId", "attribute", "calltimestamp", "callDuration", "callType", "phoneNumberHash",  "timestamp", "uploadtimestamp", "id1"]
    #read android file
    call = pd.read_csv(os.path.join(dataPath, dataFilename), sep="|", header=None)
    call.columns = header_list

    #change time to Halifax time
    call["calltimestamp"] = pd.to_datetime(call["calltimestamp"], utc=True)
    call["calltimestamp"] = pd.to_datetime(call["calltimestamp"]).dt.tz_convert(tz='America/Halifax')
    call["calltimestamp"] = pd.to_datetime(call["calltimestamp"], utc=False)

    #add some new columns to help extract features
    call["date"] = call["calltimestamp"].dt.date
    call["time"] = call["calltimestamp"].dt.strftime('%H:%M:%S')

    #Drop duplicates and sort as per timestamp
    call = call.sort_values(["participantId", "calltimestamp"]).reset_index(drop=True)
    call.drop_duplicates(subset=["participantId", "calltimestamp", "callType"], keep="last", inplace=True)
    call.drop(["id", "attribute", "phoneNumberHash", "timestamp",  "uploadtimestamp", "id1"], axis=1, inplace=True)

    #keeping only those rows which indicate calling events
    call = call[call["callType"].isin(['missed', 'rejected', 'incoming', 'outgoing'])]
    
    #checking if there are any rows with negative call durations
    call = call[call["callDuration"] >= 0]

    # missed rejected incoming outgoing
    df1 = (call[call["callType"]=="missed"].groupby(["participantId", "date"]).size().reset_index(name="no_of_missed_calls"))
    df2 = (call[call["callType"]=="rejected"].groupby(["participantId", "date"]).size().reset_index(name="no_of_rejected_calls"))
    df3 = (call[call["callType"]=="incoming"].groupby(["participantId", "date"]).size().reset_index(name="no_of_incoming_calls"))
    df4 = (call[call["callType"]=="outgoing"].groupby(["participantId", "date"]).size().reset_index(name="no_of_outgoing_calls"))
    df5 = (call[call["callType"].isin(["missed", "rejected", "incoming", "outgoing"])].groupby(["participantId", "date"]).size().reset_index(name="total_no_of_calls"))

    df6 = (call[call["callType"]=="incoming"].groupby(["participantId", "date"])["callDuration"].agg("min").reset_index(name="min_duration_of_single_incoming_call"))
    df7 = (call[call["callType"]=="outgoing"].groupby(["participantId", "date"])["callDuration"].agg("min").reset_index(name="min_duration_of_single_outgoing_call"))
    df8 = (call[call["callType"]=="incoming"].groupby(["participantId", "date"])["callDuration"].agg("max").reset_index(name="max_duration_of_single_incoming_call"))
    df9 = (call[call["callType"]=="outgoing"].groupby(["participantId", "date"])["callDuration"].agg("max").reset_index(name="max_duration_of_single_outgoing_call"))

    df10 = (call[call["callType"]=="incoming"].groupby(["participantId", "date"])["callDuration"].agg("sum").reset_index(name="total_duration_of_incoming_calls"))
    df11 = (call[call["callType"]=="outgoing"].groupby(["participantId", "date"])["callDuration"].agg("sum").reset_index(name="total_duration_of_outgoing_calls"))
    df12 = (call[call["callType"].isin(["incoming", "outgoing"])].groupby(["participantId", "date"])["callDuration"].agg("sum").reset_index(name="total_duration_of_all_calls"))

    df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

    df1[['key1', 'key2']] = df1[["participantId", "date"]]
    df2[['key1', 'key2']] = df2[["participantId", "date"]]
    df3[['key1', 'key2']] = df3[["participantId", "date"]]
    df4[['key1', 'key2']] = df4[["participantId", "date"]]
    df5[['key1', 'key2']] = df5[["participantId", "date"]]
    df6[['key1', 'key2']] = df6[["participantId", "date"]]
    df7[['key1', 'key2']] = df7[["participantId", "date"]]
    df8[['key1', 'key2']] = df8[["participantId", "date"]]
    df9[['key1', 'key2']] = df9[["participantId", "date"]]
    df10[['key1', 'key2']] = df10[["participantId", "date"]]
    df11[['key1', 'key2']] = df11[["participantId", "date"]]
    df12[['key1', 'key2']] = df12[["participantId", "date"]]

    df = df1.merge(df2, how="outer")
    for next_df in df_list[2:]:
        df = df.merge(next_df, how="outer")

    df= df.fillna(0)
    df = df.sort_values(["participantId", "date"]).reset_index(drop=True)

    # Dropping the key values used for outer joins
    df.drop(['key1', 'key2'], axis=1, inplace=True)
    df = df[(df.total_no_of_calls > 0) & (df.total_duration_of_all_calls > 0)].reset_index(drop=True)

    # save the file
    df = df.round(decimals=2)
    df.to_csv(os.path.join(featurePath, featureFilename), header=True, index=False)
    
    print("Extraction of Call features compelted")


if __name__ == "__main__":
    # config
    dataPath1 = "../../data/allNoLoc"
    # dataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"

    strTime = time.time()
    getAndroidCallingFeatures(dataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}\n")

    # strTime = time.time()
    # getAndroidCallingFeatures(dataPath2, featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}\n")