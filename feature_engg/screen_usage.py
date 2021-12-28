#total hours of screen time
#number of locks/unlocks
#Screen brightness levels
#good to have a filter to select the device which was used to collect the data.
import time
from process_data import *

def screen_usage(participantId=None):
    participants = fetch_participants()    
    data = fetch_data(attribute="Location", participantId="PROSIT001")
    data = [x[0].split("|") for x in data if x if not None]
    df = pd.DataFrame(data)
    print("jeni", df.info())
    # return participants


if __name__ == "__main__":
    start = time.time()    
    participants = screen_usage()
    # print(len(set(participants)), participants)
    end = time.time()
    print("run_time: ", round(end-start))


####NOTES####
#df with participants and screen features like Daily: screen_time, number_of_locks, number_of_unlocks:
# [participant, date, study_day_number, screen_on_time, number_of_locks, Number_of_unlocks]
# Attributes used

