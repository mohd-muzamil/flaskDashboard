# This notebook is meant for extracting screen related features.
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


#### Feature Engineering - "Screenstate (LOCKED/UNLOCKED)"

import pandas as pd
import os
import numpy as np
import pytz
import datetime
from tqdm import tqdm
# pd.set_option('display.max_rows', None)

# config variables
data_path1 = "../data/rawData/backup_frigg1"
data_path2 = "../data/rawData/backup"
feature_path = "../data/processedData"

print("Begin")

header_list = ["id", "participant", "attribute", "lockstate", "timestamp", "uploadtimestamp"]
#read ios file
df_screen_state_ios1 = pd.read_csv(os.path.join(data_path1, "Lock_state.csv"), sep="|")
df_screen_state_ios1.columns = header_list
df_screen_state_ios1['device'] = "ios"

df_screen_state_ios2 = pd.read_csv(os.path.join(data_path2, "Lock_state.csv"), sep="|")
df_screen_state_ios2.columns = header_list
df_screen_state_ios2['device'] = "ios"

df_screen_state_ios = pd.concat([df_screen_state_ios1, df_screen_state_ios2], ignore_index=True)

# df_screen_state_ios = df_screen_state_ios[df_screen_state_ios.participant.isin(filtered_participants)]

#read android file
# df_screen_state_android = pd.read_csv(os.path.join(data_path, "powerState_Covid_data.csv"), sep="|")
# df_screen_state_android.columns = header_list
# df_screen_state_android['device'] = "android"
# df_screen_state_android = df_screen_state_android[df_screen_state_android.participant.isin(filtered_participants)]

#keep only screen_on and screen_off states in android data and change the value to Locked and unlocked
# df_screen_state_android = df_screen_state_android[(df_screen_state_android.lockstate == "screen_on") | (df_screen_state_android.lockstate == "screen_off")]
# df_screen_state_android.loc[(df_screen_state_android.lockstate == "screen_on"), "lockstate"] = "UNLOCKED"
# df_screen_state_android.loc[(df_screen_state_android.lockstate == "screen_off"), "lockstate"] = "LOCKED"

#concat ios and android data into one single df
# df_screen_state = pd.concat([df_screen_state_ios, df_screen_state_android], axis=0)
df_screen_state = df_screen_state_ios.copy()
df_screen_state.drop(["id", "attribute", "uploadtimestamp"], axis=1, inplace=True)

#change time to Halifax time
df_screen_state["timestamp"] = pd.to_datetime(df_screen_state["timestamp"], utc=True)
df_screen_state["timestamp"] = pd.to_datetime(df_screen_state["timestamp"]).dt.tz_convert(tz='America/Halifax')
df_screen_state["timestamp"] = pd.to_datetime(df_screen_state["timestamp"], utc=False)

#add some new columns to help extract features
df_screen_state["date"] = df_screen_state["timestamp"].dt.date
df_screen_state["time"] = df_screen_state["timestamp"].dt.strftime('%H:%M:%S')

# decided not to use these here
# df_screen_state["weekday"] = df_screen_state["timestamp"].dt.dayofweek
# df_screen_state["week"] = df_screen_state["timestamp"].dt.isocalendar().week

#divide the day into 3 sections
# df_screen_state["dailysection"] = df_screen_state["timestamp"].dt.hour.apply(lambda x: 1 if (x >= 0 and x < 8) else (2 if (x >= 8 and x < 16) else(3 if (x >= 16 and x < 24) else -1)))
# df_screen_state["dailysection"] = df_screen_state["timestamp"].dt.hour.apply(lambda x: 1 if (x >= 7 and x < 19) else 2)
df_screen_state["dailysection"] = 1
df_screen_state = df_screen_state[df_screen_state["dailysection"] != -1]


filtering_df = df_screen_state.groupby(["participant", "date"]).size().reset_index().groupby("participant").size().reset_index(name="noOfDays")
filtering_df = filtering_df[(filtering_df.noOfDays >= 7)]
# filtering_df = filtering_df[(filtering_df.noOfDays >= 7) & (filtering_df.noOfDays <= 35)]
filtered_participants = filtering_df.participant.unique().tolist()
# filtering_df

#filter the df to take only the required participants
df_screen_state = df_screen_state[df_screen_state.participant.isin(filtered_participants)]

#Drop duplicates and sort as per timestamp
df_screen_state.drop_duplicates(inplace=True)
df_screen_state = df_screen_state.sort_values(["participant", "timestamp"]).reset_index(drop=True)

#keeping only those rows which indicate screen usage
df_screen_state = df_screen_state[(df_screen_state.lockstate == "LOCKED") | (df_screen_state.lockstate == "UNLOCKED")]

df_screen_state_processed = pd.DataFrame()

"""
filter over participant, date, daily_section:
check if df is not empty
remove duplicates
add first and last rows
append to processed_df

""" 
participants = df_screen_state.participant.unique()
# participants = ["PROSIT0004","PROSIT001", "PROSIT00A"]
for participant in tqdm(participants):
    df_screen_state_participant = df_screen_state[df_screen_state.participant == participant].copy()
    dates = df_screen_state_participant.date.unique()

    for i, date in enumerate(dates):
        df_screen_state_participant_date = df_screen_state_participant[df_screen_state_participant.date == date].copy()
        
        for dailysection in df_screen_state_participant_date.dailysection.unique():
            df_screen_state_participant_date_dailysection = df_screen_state_participant_date[df_screen_state_participant_date.dailysection == dailysection].copy()
            df_screen_state_participant_date_dailysection["recorded_instances"] = df_screen_state_participant_date_dailysection.shape[0]
            
            if df_screen_state_participant_date_dailysection.shape[0] > 1:
                #add logic to remove duplicates using roll columns
                df_screen_state_participant_date_dailysection = df_screen_state_participant_date_dailysection[df_screen_state_participant_date_dailysection.lockstate != df_screen_state_participant_date_dailysection.lockstate.shift(1)]
                #first_event in a daily section
                first_event = df_screen_state_participant_date_dailysection.iloc[:1, :].copy()
                if first_event.lockstate.item() == "LOCKED":
                    first_event.lockstate = "UNLOCKED"
                elif first_event.lockstate.item() == "UNLOCKED":
                    first_event.lockstate = "LOCKED"
                
                #last_event in a daily section
                last_event = df_screen_state_participant_date_dailysection.iloc[-1:, :].copy()
                if last_event.lockstate.item() == "LOCKED":
                    last_event.lockstate = "UNLOCKED"
                elif last_event.lockstate.item() == "UNLOCKED":
                    last_event.lockstate = "LOCKED"
                  
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
                 
                df_screen_state_participant_date_dailysection = pd.concat([first_event, df_screen_state_participant_date_dailysection, last_event], ignore_index=True)
                df_screen_state_participant_date_dailysection["screen_on_time"] = 0
                df_screen_state_participant_date_dailysection["screen_off_time"] = 0
                
                #logic to calculate screen_time
                index = (df_screen_state_participant_date_dailysection.lockstate == "UNLOCKED" ) & (df_screen_state_participant_date_dailysection.lockstate.shift(-1) == "LOCKED" )
                df_screen_state_participant_date_dailysection.loc[index, "screen_on_time"] = (df_screen_state_participant_date_dailysection.timestamp.shift(-1)[index] - df_screen_state_participant_date_dailysection.timestamp[index]).astype('timedelta64[s]')
                
                index = (df_screen_state_participant_date_dailysection.lockstate == "LOCKED" ) & (df_screen_state_participant_date_dailysection.lockstate.shift(-1) == "UNLOCKED" )
                df_screen_state_participant_date_dailysection.loc[index, "screen_off_time"] = (df_screen_state_participant_date_dailysection.timestamp.shift(-1)[index] - df_screen_state_participant_date_dailysection.timestamp[index]).astype('timedelta64[s]')
                
                df_screen_state_participant_date_dailysection.screen_on_time = np.round(df_screen_state_participant_date_dailysection.screen_on_time / 60)    #use /60 here to convert time to minutes
                df_screen_state_participant_date_dailysection.screen_off_time = np.round(df_screen_state_participant_date_dailysection.screen_off_time / 60)  #use /60 here to convert time to minutes
                
                df_screen_state_participant_date_dailysection["date_num"] = i+1
                
                df_screen_state_processed = pd.concat([df_screen_state_processed, df_screen_state_participant_date_dailysection], ignore_index=True)
                
            # break
        # break
    # break

df_screen_state_processed[df_screen_state_processed.screen_on_time < 0]
# df_screen_state_processed = df_screen_state_processed[df_screen_state_processed.screen_on_time >= 0]

df1 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"]).size().reset_index(name="no_of_unlocks"))
df2 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["screen_on_time"].agg("max").reset_index(name="max_screen_on_time"))
df3 = (df_screen_state_processed[df_screen_state_processed.lockstate=="LOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["screen_off_time"].agg("max").reset_index(name="max_screen_off_time"))
df4 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["screen_on_time"].agg("sum").reset_index(name="total_screen_on_time"))
df5 = (df_screen_state_processed[df_screen_state_processed.lockstate=="LOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["screen_off_time"].agg("sum").reset_index(name="total_screen_off_time"))
df6 = (df_screen_state_processed[df_screen_state_processed.lockstate=="UNLOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["time"].agg("min").reset_index(name="first_screen_unlock_time"))
df7 = (df_screen_state_processed[df_screen_state_processed.lockstate=="LOCKED"].groupby(["participant", "device", "date", "dailysection", "date_num", "recorded_instances"])["time"].agg("max").reset_index(name="last_screen_lock_time"))

df = df1.merge(df2, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")
df = df.merge(df3, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")
df = df.merge(df4, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")
df = df.merge(df5, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")
df = df.merge(df6, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")
df = df.merge(df7, on=["participant", "device", "date", "dailysection", "date_num", "recorded_instances"], how="inner")

df[["participant", "date", "no_of_unlocks"]]

df["first_screen_unlock_time"] = pd.to_datetime(df["first_screen_unlock_time"], format='%H:%M:%S')
df["first_screen_unlock_time"] = df["first_screen_unlock_time"].dt.hour * 60 + df["first_screen_unlock_time"].dt.minute

df["last_screen_lock_time"] = pd.to_datetime(df["last_screen_lock_time"], format='%H:%M:%S')
df["last_screen_lock_time"] = df["last_screen_lock_time"].dt.hour * 60 + df["last_screen_lock_time"].dt.minute

# creating a data directory
dirName = os.path.join("../data/", "feature_files")
if not os.path.exists(dirName):
    os.mkdir(dirName)

df.to_csv(os.path.join(feature_path, "ios_screen_features"), header=True, index=False)

print("End")