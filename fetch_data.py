from flask.json import jsonify
import pandas as pd
from data_reformat import handle_recursive_dict
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient

class App:
  __conf = {
    "MONGODB_HOST" : '172.17.7.3',
    "MONGODB_PORT" : 27017,
    "DBS_NAME" : 'prosit',
    "COLLECTION_NAME" : 'entries',
    "MONGO_USER" : "",
    "MONGO_PASS" : ""
  }
  __setters = ["username", "password"]

  @staticmethod
  def config(name):
    return App.__conf[name]

  @staticmethod
  def set(name, value):
    if name in App.__setters:
      App.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")

def create_ssh():
  App.set("username", "mmh")    # set new username value
  App.set("password", "Healthy48Density") # this raises NameError
  server = SSHTunnelForwarder(
      App.config("MONGODB_HOST"),
      ssh_username = App.config("username"),
      ssh_password = App.config("password"),
      remote_bind_address=('127.0.0.1', 27017)
  )
  
  server.start()
  connection = MongoClient('127.0.0.1', server.local_bind_port)
  return server, connection

def fetch_participants():
    server, connection = create_ssh()
    connection = MongoClient('127.0.0.1', server.local_bind_port)
    collection = connection[App.config("DBS_NAME")][App.config("COLLECTION_NAME")]
    #mongo query to fetch participant data for an attribute
    participants = collection.distinct("participantId")
    # participant_device = {}
    # Device_data = fetch_data(None, "Device", True)
      # df = pd.DataFrame(Device_data)
      # df['device'] = df.iloc[:, -2] + "_" + df.iloc[:, -1]
      # print(participant, df['device'].unique().tolist())
      # Devices = df.iloc[:,-2].unique().tolist()
      # participant_device[participant] = Devices

    connection.close()
    return participants


def fetch_data(participantId, attribute, allparticipants=False):
    App.set("username", "mmh")    # set new username value
    App.set("password", "Healthy48Density") # this raises NameError

    # FIELDS = {"participantId":"PROSIT001", "attribute":"Brightness"}

    server = SSHTunnelForwarder(
        App.config("MONGODB_HOST"),
        ssh_username = App.config("username"),
        ssh_password = App.config("password"),
        remote_bind_address=('127.0.0.1', 27017)
    )
    
    server.start()

    connection = MongoClient('127.0.0.1', server.local_bind_port)
    collection = connection[App.config("DBS_NAME")][App.config("COLLECTION_NAME")]
    #mongo query to fetch participant data for an attribute
    if allparticipants:
      info = collection.find({"attribute": attribute}, {"_id": 0, "participantId": 1, "start_time": 1, "entries": 1})  
    else:
      info = collection.find({"attribute": attribute, "participantId":participantId.upper()}, {"_id": 0, "participantId": 1, "start_time": 1, "entries": 1})
    
    connection.close()
    data = []
    if info is not None:
      for d in info:
        data_instance = handle_recursive_dict(d)
        data += (data_instance)
    # df = pd.DataFrame(data)
    # print("from here", df[df.columns[-2]].unique())
    return data



def test():
  connection = create_ssh()
  collection = connection[App.config("DBS_NAME")][App.config("COLLECTION_NAME")]
  
  participants = collection.distinct("participantId")
  # info = collection.find({"$or": [{"attribute":"Device"}, {"attribute":"systemInfo"}]}, {"_id": 0, "participantId": 1, "start_time": 1, "entries": 1})
  # db.inventory.find( { $or: [ { quantity: { $lt: 20 } }, { price: 10 } ] } )
  print(participants)
  # data = []
  # if data is not None:
  #   for d in info:
  #     # print(d)
  #     data_instance = handle_recursive_dict(d)
  #     # print(data_instance)
  #     data += (data_instance)
  #   df = pd.DataFrame(data, encoding='utf-8')
  #   print(df.iloc[:, -2].unique())
    # print(df.groupby([df.columns[0], df.columns[-2]]).size())
  connection.close()


if __name__ == "__main__":
    data = fetch_data("PROSIT001", "Brightness", allparticipants=False)
    # df = pd.DataFrame(data)
    # df['device'] = df.iloc[:, -2] + "_" + df.iloc[:, -1]
    # print(df['device'].unique().tolist())
    print(data[:10])
    # participants = fetch_participants(); print("from fetch_data", participants);
    # test()
   
