from imports import *
"""
Mobility Features
Stay points
Destination points 
Entropy
Normalized Entroy
Percentage
Radius of Gyration
Location Variance
"""

def get_stayPoints(df, roaming_distance=50, minimum_stay=10, number_jobs=1):
    """
    method returns the total number of stay points for the given location points
    uses the logic used in Microsoft paper
    """
    # Parameters
    roaming_distance = meters2degrees(roaming_distance) # 50 meters converted to degrees
#     minimum_stay  # minutes
#     number_jobs   # number of parallel jobs

    # Set index 
    df = df.reset_index().set_index(["participant", "timestamp"])

    # Call helper-function to process entire df in one go
    df_stops = process_data(df=df, 
                            roam_dist=roaming_distance, 
                            min_stay=minimum_stay, 
                            n_jobs=number_jobs,
                            print_output="notebook")
    df_stops = pd.concat(df_stops)

    # Only keep users with more than one stop
    df_stops = (df_stops
        .groupby("user_id").filter(lambda x: len(x) > 1)
        .set_index(["user_id"]))

    return df_stops


def get_clusters(df_stops, linkage_method = 'complete', distance=100):
    """
    method returns the total number of clusters for the given stay points for the given location points
    uses the logic used in Microsoft paper
    need to see if i can merge this with above method
    """
    # Clustering parameters
    # linkage_method = 'centroid'/'complete'
    distance = meters2degrees(distance)

    # Cluster stoplocations on a per user basis
    df_clusters = (df_stops.groupby('user_id')
                  .apply(lambda x: 
                         cluster_stoplocations(x, linkage_method, distance))
                  .reset_index())

    return df_clusters


def getIosMobilityFeatures(dataPath, featurePath):
    print("Begin extraction - Screen features")
    
    dataFilename = "Location_decrypted_temp.csv"
    date = datetime.now().strftime("%Y%m%d_%I%M%S%p")
    featureFilename = "ios_mobility_features_" + dataPath.split("/")[-1] + "_" + date + ".csv"

    if not (os.path.exists(os.path.join(dataPath, dataFilename))):
        sys.exit("{dataFilename} file does not exist in {dataPath} folder")

    # read file with a header
    location = pd.read_csv(os.path.join(dataPath, dataFilename), sep="|")

    #change time to Halifax time
    location["timestamp"] = pd.to_datetime(location["timestamp"], utc=True)
    location["timestamp"] = pd.to_datetime(location["timestamp"]).dt.tz_convert(tz='America/Halifax')
    location["timestamp"] = pd.to_datetime(location["timestamp"], utc=False)

    #add new columns to help extract features
    # location["date"] = pd.to_datetime(location["timestamp"]).dt.date
    # location["weekday"] = pd.to_datetime(location["timestamp"]).dt.weekday    # Monday=0, Sunday=6
    # location["time"] = pd.to_datetime(location["timestamp"]).dt.strftime('%H:%M:%S')

    # sort data, remove duplicates and drop unecessary columns
    location = location.sort_values(["participant", "timestamp"]).reset_index(drop=True)
    location.drop_duplicates(subset=["participant", "timestamp", "latitude", "longitude", "address"], keep="last", inplace=True)
    location.drop(["id", "attribute", "address", "uploadtimestamp"], axis=1, inplace=True)

    df_stops = get_stayPoints(location)
    df_clusters = get_clusters(df_stops)
    

if __name__ == "__main__":
    dataPath1 = "/csv/backup_frigg1"
    dataPath2 = "/csv/backup"
    featurePath = "/csv/features"

    strTime = time.time()
    getIosMobilityFeatures(dataPath1, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}")

    strTime = time.time()
    # getIosMobilityFeatures(dataPath2, featurePath)
    endTime = time.time()
    print(f"run time: {round((endTime - strTime)/60, 2)}")