# This notebook is meant for extracting Call related features from ios and android users
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

import pandas as pd
import os
import numpy as np
import pytz
import datetime
from tqdm import tqdm
import time
# pd.set_option('display.max_rows', None)

# CONFIG variables
data_path1 = "../data/rawData/backup_frigg1"
data_path2 = "../data/rawData/backup"
feature_path = "../data/processedData"

print("Begin")

# Call IOS data
header_list = ["id", "participant", "attribute", "callevent", "timestamp", "uploadtimestamp"]
#read ios file
df_call_ios1 = pd.read_csv(os.path.join(data_path1, "Call.csv"), sep="|", header=None)
df_call_ios1.columns = header_list
df_call_ios1 = df_call_ios1[["participant", "timestamp", "callevent"]]
df_call_ios1['device'] = "ios"

df_call_ios2 = pd.read_csv(os.path.join(data_path2, "Call.csv"), sep="|", header=None)
df_call_ios2.columns = header_list
df_call_ios2 = df_call_ios2[["participant", "timestamp", "callevent"]]
df_call_ios2['device'] = "ios"

df_call_ios = pd.concat([df_call_ios1, df_call_ios2], ignore_index=True)



#change time to Halifax time
df_call_ios["timestamp"] = pd.to_datetime(df_call_ios["timestamp"], utc=True)
df_call_ios["timestamp"] = pd.to_datetime(df_call_ios["timestamp"]).dt.tz_convert('America/Halifax')

#add some new columns to help extract features
df_call_ios["date"] = df_call_ios["timestamp"].dt.date
df_call_ios["time"] = df_call_ios["timestamp"].dt.strftime('%H:%M:%S')

# decided to not include this here
# df_call_ios["weekday"] = df_call_ios["timestamp"].dt.dayofweek
# df_call_ios["week"] = df_call_ios["timestamp"].dt.isocalendar().week
# df_call_ios["MinuteOfTheDay"] = (df_call_ios.timestamp - df_call_ios.timestamp.dt.floor('d')).astype('timedelta64[m]')

#divide the day into 3 sections
# df_call_ios["dailysection"] = df_call_ios["timestamp"].dt.hour.apply(lambda x: 1 if (x >= 0 and x < 8) else (2 if (x >= 8 and x < 16) else(3 if (x >= 16 and x < 24) else -1)))
# df_call_ios["dailysection"] = df_call_ios["timestamp"].dt.hour.apply(lambda x: 1 if (x >= 7 and x < 19) else 2)
df_call_ios["dailysection"] = 1
df_call_ios = df_call_ios[df_call_ios["dailysection"] != -1]

# filtering_df = df_call_ios.groupby(["participant", "date"]).size().reset_index().groupby("participant").size().reset_index(name="noOfDays")
# filtering_df = filtering_df[(filtering_df.noOfDays >= 21) & (filtering_df.noOfDays <= 35)]
# filtered_participants = filtering_df.participant.unique().tolist()

#filter the df to take only the required participants
# df_call_ios = df_call_ios[df_call_ios.participant.isin(filtered_participants)]

#Drop duplicates and sort as per timestamp
df_call_ios.drop_duplicates(inplace=True)
df_call_ios = df_call_ios.sort_values(["participant", "timestamp"]).reset_index(drop=True)

#keeping only those rows which indicate calling events
df_call_ios = df_call_ios[df_call_ios.callevent.isin(['CALL_INCOMING', 'CALL_CONNECTED', 'CALL_DISCONNECTED',
       'CALL_DIALING', 'CALL_ON_HOLD'])]

df_call_ios_processed = pd.DataFrame()

"""
filter over participant, date, daily_section:
check if df is not empty
remove duplicates
add first and last rows
append to processed_df
****call duration for features is in minutes****
""" 
participants = df_call_ios.participant.unique()
# participants = ["PROSIT0004","PROSIT001", "PROSIT00A"]

for participant in tqdm(participants):
    df_call_ios_participant = df_call_ios[df_call_ios.participant == participant].copy()
    dates = df_call_ios_participant.date.unique()

    for i, date in enumerate(dates):
        df_call_ios_participant_date = df_call_ios_participant[df_call_ios_participant.date == date].copy()
        
        for dailysection in df_call_ios_participant_date.dailysection.unique():
            
            df_call_ios_participant_date_dailysection = df_call_ios_participant_date[df_call_ios_participant_date.dailysection == dailysection].copy()
#             df_call_ios_participant_date_dailysection["recorded_instances"] = df_call_ios_participant_date_dailysection.shape[0]
            
            if df_call_ios_participant_date_dailysection.shape[0] > 1:
                
                #first_event in a daily section
                first_event = df_call_ios_participant_date_dailysection.iloc[:1, :].copy()
                first_event.lockstate = "CALL_CONNECTED"
                
                #last_event in a daily section
                last_event = df_call_ios_participant_date_dailysection.iloc[-1:, :].copy()
                last_event.lockstate = "CALL_DISCONNECTED"
                  
                #Daily_sections (x >= 0 and x < 8):1 | (x >= 8 and x < 16):2 | (x >= 16 and x < 24):3
                date_str = first_event.date.item().strftime("%Y%m%d")
                if dailysection == 1:
                    start_time_str =  date_str + "000000"
                    first_event.timestamp = pd.to_datetime(start_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
#                     last_time_str = date_str + "075959"
                    last_time_str = date_str + "235959"
                    last_event.timestamp = pd.to_datetime(last_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
                    
#                 elif dailysection == 2:
#                     start_time_str =  date_str + "080000"
#                     first_event.timestamp = pd.to_datetime(start_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
#                     last_time_str = date_str + "155959"
#                     last_event.timestamp = pd.to_datetime(last_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
                    
#                 elif dailysection == 3:
#                     start_time_str =  date_str + "160000"
#                     first_event.timestamp = pd.to_datetime(start_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
#                     last_time_str = date_str + "235959"
#                     last_event.timestamp = pd.to_datetime(last_time_str, format='%Y%m%d%H%M%S').tz_localize('America/Halifax')
                 
                df_call_ios_participant_date_dailysection = pd.concat([first_event, df_call_ios_participant_date_dailysection, last_event], ignore_index=True)
                df_call_ios_participant_date_dailysection["duration"] = 0
                df_call_ios_participant_date_dailysection["calltype"] = ""
                
                #logic to call_type and duration_time
                df_call_ios_participant_date_dailysection["callevent_roll1"] = df_call_ios_participant_date_dailysection.callevent.shift(-1)
                df_call_ios_participant_date_dailysection["timestamp_roll1"] = df_call_ios_participant_date_dailysection.timestamp.shift(-1)
                df_call_ios_participant_date_dailysection["callevent_roll2"] = df_call_ios_participant_date_dailysection.callevent.shift(-2)
                df_call_ios_participant_date_dailysection["timestamp_roll2"] = df_call_ios_participant_date_dailysection.timestamp.shift(-2)

                index = (df_call_ios_participant_date_dailysection["callevent"] == "CALL_INCOMING" ) & (df_call_ios_participant_date_dailysection["callevent_roll1"] == "CALL_DISCONNECTED" )
                df_call_ios_participant_date_dailysection.loc[index, "duration"] = (df_call_ios_participant_date_dailysection[index]["timestamp_roll1"] - df_call_ios_participant_date_dailysection[index]["timestamp"]).astype('timedelta64[m]')
                df_call_ios_participant_date_dailysection.loc[index, "calltype"] = "missed"
                df_call_ios_participant_date_dailysection.loc[index, "start_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp"].dt.time
                df_call_ios_participant_date_dailysection.loc[index, "end_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll1"].dt.time

                index = (df_call_ios_participant_date_dailysection["callevent"] == "CALL_DIALING" ) & (df_call_ios_participant_date_dailysection["callevent_roll1"] == "CALL_DISCONNECTED" )
                df_call_ios_participant_date_dailysection.loc[index, "duration"] = (df_call_ios_participant_date_dailysection[index]["timestamp_roll1"] - df_call_ios_participant_date_dailysection[index]["timestamp"]).astype('timedelta64[m]')
                df_call_ios_participant_date_dailysection.loc[index, "calltype"] = "rejected"
                df_call_ios_participant_date_dailysection.loc[index, "start_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp"].dt.time
                df_call_ios_participant_date_dailysection.loc[index, "end_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll1"].dt.time

                index = (df_call_ios_participant_date_dailysection["callevent"] == "CALL_INCOMING" ) & (df_call_ios_participant_date_dailysection["callevent_roll1"] == "CALL_CONNECTED" ) & (df_call_ios_participant_date_dailysection["callevent_roll2"] == "CALL_DISCONNECTED")
                df_call_ios_participant_date_dailysection.loc[index, "duration"] = (df_call_ios_participant_date_dailysection[index]["timestamp_roll2"] - df_call_ios_participant_date_dailysection[index]["timestamp_roll1"]).astype('timedelta64[m]')
                df_call_ios_participant_date_dailysection.loc[index, "calltype"] = "incoming"
                df_call_ios_participant_date_dailysection.loc[index, "start_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll1"].dt.time
                df_call_ios_participant_date_dailysection.loc[index, "end_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll2"].dt.time

                index = (df_call_ios_participant_date_dailysection["callevent"] == "CALL_DIALING" ) & (df_call_ios_participant_date_dailysection["callevent_roll1"] == "CALL_CONNECTED" ) & (df_call_ios_participant_date_dailysection["callevent_roll2"] == "CALL_DISCONNECTED")
                df_call_ios_participant_date_dailysection.loc[index, "duration"] = (df_call_ios_participant_date_dailysection[index]["timestamp_roll2"] - df_call_ios_participant_date_dailysection[index]["timestamp_roll1"]).astype('timedelta64[m]')
                df_call_ios_participant_date_dailysection.loc[index, "calltype"] = "outgoing"
                df_call_ios_participant_date_dailysection.loc[index, "start_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll1"].dt.time
                df_call_ios_participant_date_dailysection.loc[index, "end_time"] = df_call_ios_participant_date_dailysection.loc[index, "timestamp_roll2"].dt.time
                
                df_call_ios_participant_date_dailysection["date_num"] = i+1
                
                df_call_ios_processed = pd.concat([df_call_ios_processed, df_call_ios_participant_date_dailysection], ignore_index=True)
                
#             break
#         break
#     break

#checking if there are any rows with negative call durations
# df_call_ios_processed[df_call_ios_processed.duration < 0]
df_call_ios_processed = df_call_ios_processed[df_call_ios_processed.duration >= 0]

# missed rejected incoming outgoing
df1 = (df_call_ios_processed[df_call_ios_processed.calltype=="missed"].groupby(["participant", "device", "date", "date_num"]).size().reset_index(name="no_of_missed_calls"))
df2 = (df_call_ios_processed[df_call_ios_processed.calltype=="rejected"].groupby(["participant", "device", "date", "date_num"]).size().reset_index(name="no_of_rejected_calls"))
df3 = (df_call_ios_processed[df_call_ios_processed.calltype=="incoming"].groupby(["participant", "device", "date", "date_num"]).size().reset_index(name="no_of_incoming_calls"))
df4 = (df_call_ios_processed[df_call_ios_processed.calltype=="outgoing"].groupby(["participant", "device", "date", "date_num"]).size().reset_index(name="no_of_outgoing_calls"))
df5 = (df_call_ios_processed[df_call_ios_processed.calltype.isin(["missed", "rejected", "incoming", "outgoing"])].groupby(["participant", "device", "date", "date_num"]).size().reset_index(name="total_no_of_calls"))

df6 = (df_call_ios_processed[df_call_ios_processed.calltype=="incoming"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("min").reset_index(name="min_duration_of_single_incoming_call"))
df7 = (df_call_ios_processed[df_call_ios_processed.calltype=="outgoing"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("min").reset_index(name="min_duration_of_single_outgoing_call"))
df8 = (df_call_ios_processed[df_call_ios_processed.calltype=="incoming"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("max").reset_index(name="max_duration_of_single_incoming_call"))
df9 = (df_call_ios_processed[df_call_ios_processed.calltype=="outgoing"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("max").reset_index(name="max_duration_of_single_outgoing_call"))

df10 = (df_call_ios_processed[df_call_ios_processed.calltype=="incoming"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("sum").reset_index(name="total_duration_of_incoming_calls"))
df11 = (df_call_ios_processed[df_call_ios_processed.calltype=="outgoing"].groupby(["participant", "device", "date", "date_num"])["duration"].agg("sum").reset_index(name="total_duration_of_outgoing_calls"))
df12 = (df_call_ios_processed[df_call_ios_processed.calltype.isin(["incoming", "outgoing"])].groupby(["participant", "device", "date", "date_num"])["duration"].agg("sum").reset_index(name="total_duration_of_all_calls"))

df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

df1[['key1','key2','key3','key4']]=df1[["participant", "device", "date", "date_num"]]
df2[['key1','key2','key3','key4']]=df2[["participant", "device", "date", "date_num"]]
df3[['key1','key2','key3','key4']]=df3[["participant", "device", "date", "date_num"]]
df4[['key1','key2','key3','key4']]=df4[["participant", "device", "date", "date_num"]]
df5[['key1','key2','key3','key4']]=df5[["participant", "device", "date", "date_num"]]
df6[['key1','key2','key3','key4']]=df6[["participant", "device", "date", "date_num"]]
df7[['key1','key2','key3','key4']]=df7[["participant", "device", "date", "date_num"]]
df8[['key1','key2','key3','key4']]=df8[["participant", "device", "date", "date_num"]]
df9[['key1','key2','key3','key4']]=df9[["participant", "device", "date", "date_num"]]
df10[['key1','key2','key3','key4']]=df10[["participant", "device", "date", "date_num"]]
df11[['key1','key2','key3','key4']]=df11[["participant", "device", "date", "date_num"]]
df12[['key1','key2','key3','key4']]=df12[["participant", "device", "date", "date_num"]]

df_call_ios = df1.merge(df2, how="right")
for next_df in df_list[2:]:
    df_call_ios = df_call_ios.merge(next_df, how="outer")

df_call_ios= df_call_ios.fillna(0)
df_call_ios = df_call_ios.sort_values(["participant", "date"]).reset_index(drop=True)

# Dropping the key values used for outer joins
df_call_ios.drop(['key1','key2','key3', 'key4'], axis=1, inplace=True)
df_call_ios = df_call_ios[(df_call_ios.total_no_of_calls > 0) & (df_call_ios.total_duration_of_all_calls > 0)].reset_index(drop=True)

df_call_ios = df_call_ios.round(decimals=2)
df_call_ios.to_csv(os.path.join(feature_path, "ios_calling_features"), header=True, index=False)

print("End")