import pandas as pd
import os
import numpy as np
import pytz
import datetime

data_path = "/home/mmh/initial_analysis/all_data"

def get_screen_data():
    #jupyter notebooks for each feature extraction file.

    return df

def get_call_duration(participantId):
    pass

def get_mobility_data(participantId):
    pass

def get_sleep_estimate_data(participantId):
    pass




def generate_data_circle_packing():
    participants = fetch_participants()
    for participant in participants:
        print(participant)

        #screen usage

        #sleep estimate

        #distance travelled

        #call duration



if __name__ == '__main__':
    df = get_screen_data()
    df.to_csv(os.path.join(data_path, "muzz"), index=False)
    print('ok')