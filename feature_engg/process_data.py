# This Script is used to query the data filter-> ["participantId", "attribute"]
# returns the data in the form of 2D list, with data as a str with "|" seperator.
#----------------------#

from pymongo import MongoClient
import pandas as pd
import datetime
import sys


def handle_recursive_dict(doc):
    post = None
    participant = None
    start_time = None
    delta_time = None
    actual_time = None

    if isinstance(doc, dict):
        data = []
        for key, value in sorted(doc.items())[::-1]:
            if key == "participantId":
                participant = value

            elif key == "start_time":
                start_time = value

            elif key == "entries":
                for val in value:
                    delta_time, entry = next(iter(val.items()))
                    actual_time = start_time + \
                        datetime.timedelta(days=0, seconds=int(delta_time))
                    if type(entry) is list:
                        post = "|".join(map(
                            str, [participant, actual_time, "|".join(str(x) for x in entry)]))
                    else:
                        post = "|".join(map(
                            str, [participant, actual_time, str(entry)]))
                    data.append([post])
            else:
                print("Invalid attribute")
                sys.exit()
        return data


def connect_to_db():
    # Establishsing the connection to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.prosit  # database-> prosit
    collection = db.entries  # collection-> entries
    return collection


def fetch_participants():
    collection = connect_to_db()
    data = collection.distinct("participantId")
    return data


def fetch_data(attribute=None, participantId=None, allparticipants=False):
    collection = connect_to_db()
    # mongo db query
    data = []
    if allparticipants and (attribute is not None):
        data = collection.find({"attribute": attribute}, {
            "_id": 0, "participantId": 1, "start_time": 1, "entries": 1})

    elif (participantId is not None) and (attribute is not None):
        data = collection.find({"participantId": participantId, "attribute": attribute}, {
            "_id": 0, "participantId": 1, "start_time": 1, "entries": 1})

    else:
        print("parameter mission")

    queried_data = []
    for i, doc in enumerate(data):
        queried_data += handle_recursive_dict(doc)

    # print(f"queried data is: ", queried_data)
    return queried_data


if __name__ == "__main__":
    data = fetch_participants()
    # data = fetch_data(participantId="PROSIT001", attribute="Brightness", allparticipants=True)
    # data = fetch_data(attribute="Brightness", allparticipants=True)
    print(len(data))
    print("ok")
