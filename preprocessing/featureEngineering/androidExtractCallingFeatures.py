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

filteredParticipantIds = []
filteredParticipantIds = ['aPROSITC0060','aPROSITC0064','aPROSITC00D','aPROSITC00M','aPROSITC0103','aPROSITC0107','aPROSITC0116','aPROSITC0118','aPROSITC0119','aPROSITC0128','aPROSITC0130','aPROSITC0131','aPROSITC0134','aPROSITC0144','aPROSITC0175','aPROSITC0188','aPROSITC0200','aPROSITC0211','aPROSITC0229','aPROSITC0235','aPROSITC0237','aPROSITC0252','aPROSITC0260','aPROSITC0275','aPROSITC0279','aPROSITC0290','aPROSITC0295','aPROSITC0301','aPROSITC0303','aPROSITC0310','aPROSITC0326','aPROSITC0357','aPROSITC0376','aPROSITC0379','aPROSITC0398','aPROSITC0414','aPROSITC0416','aPROSITC0433','aPROSITC0436','aPROSITC0437','aPROSITC0457','aPROSITC0483','aPROSITC0497','aPROSITC0645','aPROSITC0739','aPROSITC0753','aPROSITC0774','aPROSITC0805','aPROSITC0838','aPROSITC0874','aPROSITC1063','aPROSITC1065','aPROSITC1069','aPROSITC1134','aPROSITC1147','aPROSITC1149','aPROSITC1154','aPROSITC1155','aPROSITC1156','aPROSITC1165','aPROSITC1170','aPROSITC1171','aPROSITC1172','aPROSITC1175','aPROSITC1182','aPROSITC1201','aPROSITC1204','aPROSITC1205','aPROSITC1208','aPROSITC1215','aPROSITC1226','aPROSITC1230','aPROSITC1233','aPROSITC1241','aPROSITC1242','aPROSITC1255','aPROSITC1271','aPROSITC1273','aPROSITC1277','aPROSITC1283','aPROSITC1302','aPROSITC1303','aPROSITC1306','aPROSITC1309','aPROSITC1312','aPROSITC1315','aPROSITC1322','aPROSITC1337','aPROSITC1349','aPROSITC1363','aPROSITC1368','aPROSITC1374','aPROSITC1378','aPROSITC1381','aPROSITC1387','aPROSITC1388','aPROSITC1392','aPROSITC1399','aPROSITC1402','aPROSITC1403','aPROSITC1419','aPROSITC1423','aPROSITC1425','aPROSITC1429','aPROSITC1430','aPROSITC1431','aPROSITC1433','aPROSITC1439','aPROSITC1444','aPROSITC1458','aPROSITC1462','aPROSITC1473','aPROSITC1489','aPROSITC1504','aPROSITC1536','aPROSITC1541','aPROSITC1542','aPROSITC1565','aPROSITC1568','aPROSITC1575','aPROSITC1604','aPROSITC1613','aPROSITC1618','aPROSITC1620','aPROSITC1628','aPROSITC1630','aPROSITC1638','aPROSITC1688','aPROSITC1694','aPROSITC1697','aPROSITC1699','aPROSITC1701','aPROSITC1709','aPROSITC1713','aPROSITC1718','aPROSITC1734','aPROSITC1745','aPROSITC1747','aPROSITC1770','aPROSITC1778','aPROSITC1780','aPROSITC1787','aPROSITC1791','aPROSITC1793','aPROSITC1796','aPROSITC1805','aPROSITC1818','aPROSITC1822','aPROSITC1840','aPROSITC1862','aPROSITC1873','aPROSITC1887','aPROSITC1893','aPROSITC1903','aPROSITC1905','aPROSITC1921','aPROSITC1928','aPROSITC1930','aPROSITC1941','aPROSITC1944','aPROSITC1949','aPROSITC1963','aPROSITC1986','aPROSITC2010','aPROSITC2019','aPROSITC2039','aPROSITC2044','aPROSITC2067','aPROSITC2089','aPROSITC2095','aPROSITC2098','aPROSITC2101','aPROSITC2102','aPROSITC2115','aPROSITC2130','aPROSITC2132','aPROSITC2143','aPROSITC2160','aPROSITC2177','aPROSITC2180','aPROSITC2185','aPROSITC2193','aPROSITC2226','aPROSITC2232','aPROSITC2237','aPROSITC2241','aPROSITC2255','aPROSITC2256','aPROSITC2268','aPROSITC2285','aPROSITC2292','aPROSITC2295','aPROSITC2298','aPROSITC2304','aPROSITC2348','aPROSITC2349','aPROSITC2353','aPROSITC2375','aPROSITC2392','aPROSITC2725','aPROSITC2742','aPROSITC2743','aPROSITC2780','aPROSITC2797','aPROSITC2825','aPROSITC2836','aPROSITC2848','aPROSITC2876','aPROSITC2954','aPROSITC2973','aPROSITC2987','aPROSITC2990','aPROSITC2992','aPROSITC2994','aPROSITC2998','aPROSITC3000','aPROSITC3020','aPROSITC3021','aPROSITC3036','aPROSITC3050','aPROSITC3058','aPROSITC3087','aPROSITC3097','aPROSITC3108','aPROSITC3129']

def getAndroidCallingFeatures(inputDataPath, featurePath):
    """
    inputDataPath: path to folder which has android call data
    featurePath: path to store the extracted features
    """
    print("Begin extraction - Calling features")

    # config
    dataFilename = "calls__callDate_callDurationS_callType_phoneNumberHash_android.csv"
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "android_call_features_" + inputDataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(inputDataPath, dataFilename))):
        sys.exit(f"{dataFilename} file does not exist in {inputDataPath} folder \nscript aborted")

    #read android file
    header_list = ["id", "participantId", "attribute", "timestamp", "callDuration", "callType", "phoneNumberHash", "timestamp1", "uploadtimestamp", "id1"]
    #read ios file
    call = pd.read_csv(os.path.join(inputDataPath, dataFilename), sep="|", header=None, names=header_list)

    # drop unecessary columns
    call.drop(["id", "attribute", "phoneNumberHash", "timestamp1",  "uploadtimestamp", "id1"], axis=1, inplace=True)

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
    inputinputDataPath1 = "../../data/allNoLoc"
    # inputinputDataPath2 = "/csv/backup"
    featurePath = "../../data/processedData/newIntermediateFiles"

    strTime = time.time()
    getAndroidCallingFeatures(inputinputDataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}\n")

    # strTime = time.time()
    # getAndroidCallingFeatures(inputinputDataPath2, featurePath)
    # endTime = time.time()
    # print(f"run time: {round((endTime - strTime)/60, 2)}\n")