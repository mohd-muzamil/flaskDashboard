# This Script is to query the data filter-> "attribute":"Location: and restructure for futher processing....
#
#
#
#
#----------------------#

from multiprocessing import connection
from pymongo import MongoClient
import pandas as pd
import sys
import os, shutil


def write_output(line, filename):
#    print(line)
    f = open(filename, "a")
    f.write(line)
    f.close()


def handle_recursive_dict(doc, filename):
    if isinstance(doc, dict):
        post = ""
        for key, value in doc.items():
            if key != "value":
                if key == "attribute":
                  post += "|" + str(value).replace(" ", "_")
                else :
                  post += "|" + str(value)

            elif key == "value":
              if type(value) == list:
                post += "|" + "|".join(map(str, value))
              else:
                post += "|" + str(value)

            else:
                print("Invalid attribute")
                sys.exit()
        #print(post, "\n")
        write_output(f'{post[1:]}\n', filename)


def process_location():
    # Establishsing the connection to MongoDB
    myClient = MongoClient('mongodb://localhost:27017/')
    # databases = myClient.list_databases()
    databases = ["backup_frigg1"]

    for database in databases:
      db = myClient[database]  # database-> Social
      
      collections = db.list_collection_names()
      #collections = ["PROSIT000R"]         ########uncomment this lineand change value if single collection data is require. Makse sure its a list. commenting this line will fetch data for all the collections in database########

      # creating a data directory
      dirName = os.path.join("../data/rawData", database)
#      if os.path.exists(dirName):
#        shutil.rmtree(dirName)
      
      if not os.path.exists(dirName):
        os.mkdir(dirName)  

      collection_count = len(collections)
      for i, collection in enumerate(collections):
          connection = db[collection]  #collection-> different participants as collections
                  
#          attributes = connection.distinct("attribute")
#          ios attributes
#          all_ios_attributes = ["Accelerometer", "Analytics", "Brightness", "Call", "Device", "Gyroscope", "Heart_Event", "Heart_Rate", "Location", "Lock state", "Magnetometer", "Mindfulness", "Music", "Noise", "Power state", "Reachability", "Sleep", "Sleep_Noise", "Steps", "Survey", "Weather"]
          # android attributes
          # all_android_attributes = ["accelerometer_m_s2__x_y_z",  "bluetooth__bluetoothClass_bondState_deviceAdress_deviceName_id_type",  "calls__callDate_callDurationS_callType_phoneNumberHash",  "connectivity",  "debug",  "detectedActivityConfidence__inVehicle_onBicycle_onFoot_running_still_tilting_unknown_walking",  "gyroscope_rad_s__x_y_z",  "installedApps",  "light_lux",  "location__accuracyInM_altitudeAboveWGS84_bearingDeg_latitude_longitude_speedMperS",  "magnetometer_muT__x_y_z",  "notifications__action_flags_package",  "powerState",  "pressure_hPa",  "proximity_cm",  "rotationVector__cos_x_y_z",  "sensorAccuracy__accuracy_sensor",  "sms__numberLetters_phoneNumberHash_smsDate_smsType",  "soundPressureLevel_dB",  "stepCounter_sinceLastReboot",  "systemInfo",  "usageEvents"]

          attributes = ["Brightness", "Accelerometer", "Gyroscope", "Power state", "Rechability", "Sleep_Noise"]    ########uncomment this line and change value if single attribute data is required. Make sure its a list. commenting this will fetch data for all the attributes########
          
          for attribute in attributes:
            #things to change filename, participants list, filtes
            filename =  os.path.join(dirName, attribute.replace(" ", "_") + ".csv")  ########change this if data needs to be stored with a different filename#########
            # if os.path.exists(filename):
                # os.remove(filename)

            data = connection.find({'attribute':attribute})
            query_cnt = len(list(data.clone()))
            if query_cnt == 0:
              print(f"Query dose not fetch any documents for collection[{i+1}/{collection_count}]:{collection} and attribute:{attribute}")
            else:
              print(f"Query returned {query_cnt} documents for collection[{i+1}/{collection_count}]:{collection} and attribute:{attribute}!")

            for doc in data:
              #print(doc)
              handle_recursive_dict(doc, filename=filename)


if __name__ == "__main__":
    process_location()
    print("ok")
#
