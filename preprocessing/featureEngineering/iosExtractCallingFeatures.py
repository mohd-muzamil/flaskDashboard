"""
####################################################################################################
Script for extracting below call related features using IOS call data
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

# Filtered participantIds from another notebook. Only data from these will be analysed
filteredParticipantIds = []
filteredParticipantIds = ['iPROSITC0003','iPROSITC0007','iPROSITC0010','iPROSITC0019','iPROSITC0022','iPROSITC0030','iPROSITC0037','iPROSITC0041','iPROSITC0043','iPROSITC0048','iPROSITC0052','iPROSITC0057','iPROSITC0059','iPROSITC0061','iPROSITC0063','iPROSITC0067','iPROSITC0072','iPROSITC0074','iPROSITC0078','iPROSITC0083','iPROSITC0086','iPROSITC0087','iPROSITC0088','iPROSITC0090','iPROSITC0094','iPROSITC0096','iPROSITC0100','iPROSITC0102','iPROSITC0108','iPROSITC0110','iPROSITC0117','iPROSITC0121','iPROSITC0122','iPROSITC0124','iPROSITC0138','iPROSITC0146','iPROSITC0154','iPROSITC0155','iPROSITC0170','iPROSITC0181','iPROSITC0185','iPROSITC0189','iPROSITC0204','iPROSITC0208','iPROSITC0215','iPROSITC0219','iPROSITC0222','iPROSITC0226','iPROSITC0234','iPROSITC0244','iPROSITC0247','iPROSITC0253','iPROSITC0261','iPROSITC0270','iPROSITC0278','iPROSITC0292','iPROSITC0297','iPROSITC0309','iPROSITC0312','iPROSITC0323','iPROSITC0329','iPROSITC0331','iPROSITC0332','iPROSITC0333','iPROSITC0337','iPROSITC0345','iPROSITC0346','iPROSITC0350','iPROSITC0387','iPROSITC0389','iPROSITC0390','iPROSITC0399','iPROSITC0405','iPROSITC0408','iPROSITC0411','iPROSITC0425','iPROSITC0429','iPROSITC0430','iPROSITC0431','iPROSITC0439','iPROSITC0445','iPROSITC0447','iPROSITC0448','iPROSITC0451','iPROSITC0455','iPROSITC0456','iPROSITC0464','iPROSITC0474','iPROSITC0505','iPROSITC0506','iPROSITC0509','iPROSITC0510','iPROSITC0511','iPROSITC0513','iPROSITC0516','iPROSITC0526','iPROSITC0528','iPROSITC0529','iPROSITC0530','iPROSITC0531','iPROSITC0546','iPROSITC0560','iPROSITC0561','iPROSITC0569','iPROSITC0573','iPROSITC0580','iPROSITC0583','iPROSITC0586','iPROSITC0592','iPROSITC0595','iPROSITC0596','iPROSITC0599','iPROSITC0622','iPROSITC0625','iPROSITC0636','iPROSITC0640','iPROSITC0861','iPROSITC0876','iPROSITC0878','iPROSITC0890','iPROSITC0909','iPROSITC0919','iPROSITC0926','iPROSITC0928','iPROSITC0942','iPROSITC0961','iPROSITC0974','iPROSITC0978','iPROSITC0980','iPROSITC0981','iPROSITC0984','iPROSITC0992','iPROSITC0996','iPROSITC1005','iPROSITC1014','iPROSITC1018','iPROSITC1025','iPROSITC1026','iPROSITC1027','iPROSITC1029','iPROSITC1030','iPROSITC1031','iPROSITC1033','iPROSITC1034','iPROSITC1036','iPROSITC1037','iPROSITC1038','iPROSITC1039','iPROSITC1040','iPROSITC1041','iPROSITC1044','iPROSITC1046','iPROSITC1057','iPROSITC1061','iPROSITC1062','iPROSITC1066','iPROSITC1070','iPROSITC1079','iPROSITC1080','iPROSITC1086','iPROSITC1089','iPROSITC1090','iPROSITC1097','iPROSITC1100','iPROSITC1101','iPROSITC1104','iPROSITC1109','iPROSITC1110','iPROSITC1111','iPROSITC1119','iPROSITC1122','iPROSITC1126','iPROSITC1128','iPROSITC1135','iPROSITC1136','iPROSITC1137','iPROSITC1140','iPROSITC1153','iPROSITC1158','iPROSITC1174','iPROSITC1187','iPROSITC1192','iPROSITC1193','iPROSITC1221','iPROSITC1222','iPROSITC1223','iPROSITC1224','iPROSITC1227','iPROSITC1237','iPROSITC1240','iPROSITC1244','iPROSITC1261','iPROSITC1272','iPROSITC1293','iPROSITC1297','iPROSITC1299','iPROSITC1304','iPROSITC1317','iPROSITC1325','iPROSITC1326','iPROSITC1343','iPROSITC1369','iPROSITC1372','iPROSITC1379','iPROSITC1412','iPROSITC1413','iPROSITC1422','iPROSITC1424','iPROSITC1428','iPROSITC1501','iPROSITC1502','iPROSITC1512','iPROSITC1516','iPROSITC1526','iPROSITC1529','iPROSITC1548','iPROSITC1550','iPROSITC1553','iPROSITC1555','iPROSITC1562','iPROSITC1564','iPROSITC1602','iPROSITC1615','iPROSITC1621','iPROSITC1623','iPROSITC1627','iPROSITC1629','iPROSITC1635','iPROSITC1639','iPROSITC1642','iPROSITC1663','iPROSITC1666','iPROSITC1671','iPROSITC1678','iPROSITC1684','iPROSITC1685','iPROSITC1705','iPROSITC1712','iPROSITC1722','iPROSITC1742','iPROSITC1748','iPROSITC1754','iPROSITC1756','iPROSITC1761','iPROSITC1762','iPROSITC1763','iPROSITC1764','iPROSITC1785','iPROSITC1795','iPROSITC1798','iPROSITC1803','iPROSITC1807','iPROSITC1809','iPROSITC1810','iPROSITC1823','iPROSITC1826','iPROSITC1827','iPROSITC1835','iPROSITC1844','iPROSITC1861','iPROSITC1863','iPROSITC1864','iPROSITC1865','iPROSITC1874','iPROSITC1877','iPROSITC1898','iPROSITC1911','iPROSITC1914','iPROSITC1926','iPROSITC1942','iPROSITC1966','iPROSITC1979','iPROSITC1980','iPROSITC1983','iPROSITC1985','iPROSITC1996','iPROSITC1999','iPROSITC2002','iPROSITC2029','iPROSITC2037','iPROSITC2059','iPROSITC2065','iPROSITC2069','iPROSITC2076','iPROSITC2096','iPROSITC2111','iPROSITC2117','iPROSITC2129','iPROSITC2134','iPROSITC2135','iPROSITC2156','iPROSITC2162','iPROSITC2170','iPROSITC2195','iPROSITC2202','iPROSITC2203','iPROSITC2207','iPROSITC2219','iPROSITC2239','iPROSITC2247','iPROSITC2259','iPROSITC2264','iPROSITC2265','iPROSITC2267','iPROSITC2269','iPROSITC2271','iPROSITC2278','iPROSITC2303','iPROSITC2306','iPROSITC2315','iPROSITC2323','iPROSITC2330','iPROSITC2332','iPROSITC2333','iPROSITC2360','iPROSITC2382','iPROSITC2384','iPROSITC2394','iPROSITC2928','iPROSITC2964','iPROSITC2986','iPROSITC3001','iPROSITC3014','iPROSITC3025','iPROSITC3029','iPROSITC3031','iPROSITC3035','iPROSITC3037','iPROSITC3038','iPROSITC3044','iPROSITC3053','iPROSITC3070','iPROSITC3071','iPROSITC3076','iPROSITC3078','iPROSITC3079','iPROSITC3101','iPROSITC3102','iPROSITC3110','iPROSITC3111','iPROSITC3114','iPROSITC3117','iPROSITC3121','iPROSITC3124','iPROSITC3148','iPROSITC3150','iPROSITC3169','iPROSITC3172','iPROSITC3196','iPROSITC3201','iPROSITC3213','iPROSITC3214','iPROSITC3217','iPROSITC3219','iPROSITC3221','iPROSITC3226','iPROSITC3227','iPROSITC3229','iPROSITC3230','iPROSITC3233','iPROSITC3234','iPROSITC3235','iPROSITC3244','iPROSITC3249','iPROSITC3259','iPROSITC3261','iPROSITC3279','iPROSITC3282','iPROSITC3305']


def getIosCallingFeatures(inputDataPath, featurePath):
    """
    inputDataPath: path to folder which has ios call data
    featurePath: path to store the extracted features
    """
    print("Begin extraction - Calling features")

    # config
    dataFilename = "Call_ios.csv"
    timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "ios_call_features_" + inputDataPath.split("/")[-1] + "_" + timestamp + ".csv"

    if not (os.path.exists(os.path.join(inputDataPath, dataFilename))):
        sys.exit(f"{dataFilename} file does not exist in {inputDataPath} folder \nscript aborted")

    # Call IOS data
    header_list = ["id", "participantId", "attribute", "callType", "timestamp", "uploadtimestamp", "id1"]
    #read ios file
    call = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep="|", header=None, names=header_list)

    # drop unecessary columns
    call.drop(["id", "attribute", "uploadtimestamp", "id1"], axis=1, inplace=True)

    # keep only filtered participantIds
    if len(filteredParticipantIds)!=0:
        call = call[call["participantId"].isin(filteredParticipantIds)]

    #change time to Halifax time
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=True)
    call["timestamp"] = pd.to_datetime(call["timestamp"]).dt.tz_convert(tz='America/Halifax')
    call["timestamp"] = pd.to_datetime(call["timestamp"], utc=False)

    #add some new columns to help extract features
    call["date"] = call["timestamp"].dt.date
    call["time"] = call["timestamp"].dt.strftime('%H:%M:%S')

    #Drop duplicates and sort as per timestamp
    call = call.sort_values(["participantId", "timestamp"]).reset_index(drop=True)
    call.drop_duplicates(subset=["participantId", "timestamp", "callType"], keep="last", inplace=True)

    #keeping only those rows which indicate calling events
    call = call[call.callType.isin(['CALL_INCOMING', 'CALL_CONNECTED', 'CALL_DISCONNECTED', 'CALL_DIALING', 'CALL_ON_HOLD'])]

    call_processed = pd.DataFrame()

    """
    filter over participantId, date, daily_section:
    check if df is not empty
    remove duplicates
    add first and last rows
    append to processed_df
    ****call duration for features is in minutes****
    """ 
    participantIds = call.participantId.unique()
    # participantIds = ["PROSIT0004","PROSIT001", "PROSIT00A"]
    for participantId in tqdm(participantIds):
        call_participantId = call[call.participantId == participantId].copy()
        dates = call_participantId.date.unique()
        for i, date in enumerate(dates):
            call_participantId_date = call_participantId[call_participantId.date == date].copy()
                
            if call_participantId_date.shape[0] > 1:
                #first_event in a daily section
                first_event = call_participantId_date.iloc[:1, :].copy()
                first_event.callType = "CALL_CONNECTED"

                #last_event in a daily section
                last_event = call_participantId_date.iloc[-1:, :].copy()
                last_event.callType = "CALL_DISCONNECTED"
                
                call_participantId_date = pd.concat([first_event, call_participantId_date, last_event], ignore_index=True)
                call_participantId_date["duration"] = 0
                call_participantId_date["calltype"] = ""
                
                #logic to call_type and duration_time
                call_participantId_date["callType_roll1"] = call_participantId_date.callType.shift(-1)
                call_participantId_date["timestamp_roll1"] = call_participantId_date.timestamp.shift(-1)
                call_participantId_date["callType_roll2"] = call_participantId_date.callType.shift(-2)
                call_participantId_date["timestamp_roll2"] = call_participantId_date.timestamp.shift(-2)

                index = (call_participantId_date["callType"] == "CALL_INCOMING" ) & (call_participantId_date["callType_roll1"] == "CALL_DISCONNECTED" )
                call_participantId_date.loc[index, "duration"] = (call_participantId_date[index]["timestamp_roll1"] - call_participantId_date[index]["timestamp"]).astype('timedelta64[m]')
                call_participantId_date.loc[index, "calltype"] = "missed"
                call_participantId_date.loc[index, "start_time"] = call_participantId_date.loc[index, "timestamp"].dt.time
                call_participantId_date.loc[index, "end_time"] = call_participantId_date.loc[index, "timestamp_roll1"].dt.time

                index = (call_participantId_date["callType"] == "CALL_DIALING" ) & (call_participantId_date["callType_roll1"] == "CALL_DISCONNECTED" )
                call_participantId_date.loc[index, "duration"] = (call_participantId_date[index]["timestamp_roll1"] - call_participantId_date[index]["timestamp"]).astype('timedelta64[m]')
                call_participantId_date.loc[index, "calltype"] = "rejected"
                call_participantId_date.loc[index, "start_time"] = call_participantId_date.loc[index, "timestamp"].dt.time
                call_participantId_date.loc[index, "end_time"] = call_participantId_date.loc[index, "timestamp_roll1"].dt.time

                index = (call_participantId_date["callType"] == "CALL_INCOMING" ) & (call_participantId_date["callType_roll1"] == "CALL_CONNECTED" ) & (call_participantId_date["callType_roll2"] == "CALL_DISCONNECTED")
                call_participantId_date.loc[index, "duration"] = (call_participantId_date[index]["timestamp_roll2"] - call_participantId_date[index]["timestamp_roll1"]).astype('timedelta64[m]')
                call_participantId_date.loc[index, "calltype"] = "incoming"
                call_participantId_date.loc[index, "start_time"] = call_participantId_date.loc[index, "timestamp_roll1"].dt.time
                call_participantId_date.loc[index, "end_time"] = call_participantId_date.loc[index, "timestamp_roll2"].dt.time

                index = (call_participantId_date["callType"] == "CALL_DIALING" ) & (call_participantId_date["callType_roll1"] == "CALL_CONNECTED" ) & (call_participantId_date["callType_roll2"] == "CALL_DISCONNECTED")
                call_participantId_date.loc[index, "duration"] = (call_participantId_date[index]["timestamp_roll2"] - call_participantId_date[index]["timestamp_roll1"]).astype('timedelta64[m]')
                call_participantId_date.loc[index, "calltype"] = "outgoing"
                call_participantId_date.loc[index, "start_time"] = call_participantId_date.loc[index, "timestamp_roll1"].dt.time
                call_participantId_date.loc[index, "end_time"] = call_participantId_date.loc[index, "timestamp_roll2"].dt.time
                
                call_processed = pd.concat([call_processed, call_participantId_date], ignore_index=True)

    #checking if there are any rows with negative call durations
    # call_processed[call_processed.duration < 0]
    # call_processed = call_processed[call_processed["duration"] >= 0]

    # missed rejected incoming outgoing
    df1 = (call_processed[call_processed.calltype=="missed"].groupby(["participantId", "date"]).size().reset_index(name="no_of_missed_calls"))
    df2 = (call_processed[call_processed.calltype=="rejected"].groupby(["participantId", "date"]).size().reset_index(name="no_of_rejected_calls"))
    df3 = (call_processed[call_processed.calltype=="incoming"].groupby(["participantId", "date"]).size().reset_index(name="no_of_incoming_calls"))
    df4 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participantId", "date"]).size().reset_index(name="no_of_outgoing_calls"))
    df5 = (call_processed[call_processed.calltype.isin(["missed", "rejected", "incoming", "outgoing"])].groupby(["participantId", "date"]).size().reset_index(name="total_no_of_calls"))

    df6 = (call_processed[call_processed.calltype=="incoming"].groupby(["participantId", "date"])["duration"].agg("min").reset_index(name="min_duration_of_single_incoming_call"))
    df7 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participantId", "date"])["duration"].agg("min").reset_index(name="min_duration_of_single_outgoing_call"))
    df8 = (call_processed[call_processed.calltype=="incoming"].groupby(["participantId", "date"])["duration"].agg("max").reset_index(name="max_duration_of_single_incoming_call"))
    df9 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participantId", "date"])["duration"].agg("max").reset_index(name="max_duration_of_single_outgoing_call"))

    df10 = (call_processed[call_processed.calltype=="incoming"].groupby(["participantId", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_incoming_calls"))
    df11 = (call_processed[call_processed.calltype=="outgoing"].groupby(["participantId", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_outgoing_calls"))
    df12 = (call_processed[call_processed.calltype.isin(["incoming", "outgoing"])].groupby(["participantId", "date"])["duration"].agg("sum").reset_index(name="total_duration_of_all_calls"))

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
    inputDataPath1 = "../../data/allNoLoc"
    # inputDataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"

    strTime = time.time()
    getIosCallingFeatures(inputDataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}\n")

    # strTime = time.time()
    # getIosCallingFeatures(inputDataPath2, featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}\n")