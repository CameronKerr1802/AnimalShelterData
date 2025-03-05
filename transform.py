import pandas as pd

import datetime as dt
import os

def transform(csv):
    data = pd.read_csv(f"rawdata/{csv}")

    data.columns = map(str.lower, data.columns)
    data.columns = data.columns.str.replace("_", " ")
    data = data[data["animal type"] == "DOG"]
    

    if "intake total" in data.columns:
        data = data.drop("intake total", axis=1)
    if "tag type" in data.columns:
        data = data.drop("tag type", axis=1)
    if "outcome subtype" in data.columns:
        data = data.drop("outcome subtype", axis=1)

    data = data.drop(["animal type", "kennel number", "council district", "kennel status", "activity number", "activity sequence", "source id", "census tract",
            "reason", "staff id", "due out", "receipt number", "service request number", "outcome condition", "chip status",
            "animal origin", "additional information", "year", "hold request", "month"],axis=1)

    data[["animal id", "animal breed", "intake type", "intake subtype", "intake condition", 
        "outcome type","impound number"]] = data[["animal id", "animal breed","intake type", "intake subtype", "intake condition", 
                                                  "outcome type","impound number"]].astype("string")
    
    #if ("2015" in csv or "2018" in csv or"2021-2022" in csv):
        #data["intake date"] = (data["intake date"].apply(lambda x: dt.datetime.strptime(x,'%m/%d/%Y %H:%M:%S %p').date())).astype("datetime64[ns]")
        #data["outcome date"] = (data["outcome date"].apply(lambda x: dt.datetime.strptime(x,'%m/%d/%Y %H:%M:%S %p').date())).astype("datetime64[ns]")
    data['intake date'] = data['intake date'].str.partition(" ")[0]
    data['outcome date'] = data['outcome date'].str.partition(" ")[0]
    data["outcome date"] = data['outcome date'].fillna(data["intake date"])

    
    if data['intake time'].str.contains(" ").all():
        data['intake time'] = data['intake time'].str.partition(" ")[2]
    if data['outcome time'].str.contains(" ").all():
        data['outcome time'] = data['outcome time'].str.partition(" ")[2]
        
    if data["intake time"].str.contains(".").all():
        data["intake time"] = data["intake time"].str.partition(".")[0]
    if data["outcome time"].str.contains(".").all():
        data["outcome time"] = data["outcome time"].str.partition(".")[0]

    try:
        data['intake time'] = data['intake time'].apply(lambda x: dt.datetime.strptime(x, '%I:%M:%S %p').strftime('%H:%M:%S'))
    except ValueError:
        0
    try:
        data['outcome time'] = data['outcome time'].apply(lambda x: dt.datetime.strptime(x, '%I:%M:%S %p').strftime('%H:%M:%S'))
    except ValueError:
        0
    
    data = data.rename(columns={"animal id":"animal_id", "animal breed":"breed", "intake type":"intake_type", 
                                "intake subtype":"intake_subtype", "intake date":"intake_date", "intake time":"intake_time", "intake condition":"intake_condition", 
                                "outcome type":"outcome", "outcome date":"outcome_date", "outcome time":"outcome_time", "impound number":"impound_num"})



    data['intake_subtype'] = data['intake_subtype'].fillna('OTHER')
    data['intake_subtype'] = data['intake_subtype'].str.replace('CRUELT - DEAD ON ARRIVAL', 'CRUELTY')
    data['intake_subtype'] = data['intake_subtype'].str.replace('QUARANTINE - DEAD ON ARRIVAL', 'QUARANTINE')
    data['intake_subtype'] = data['intake_subtype'].str.replace('KEEP SAFE - DEAD ON ARRIVAL', 'KEEP SAFE')
    data['intake_subtype'] = data['intake_subtype'].str.replace('- DEAD ON ARRIVAL', 'DEAD ON ARRIVAL')


    data.to_csv(f'transformed_data/Final_{csv}', index=False)

files = os.listdir("rawdata")
for file in files:
    transform(file)

df_append = pd.DataFrame()

transformed_files = os.listdir("transformed_data")
for tfile in transformed_files:
    df_temp = pd.read_csv(f"transformed_data/{tfile}")
    df_append = df_append._append(df_temp, ignore_index=True)

df_append = df_append[df_append.columns[[10,0,1,2,3,4,5,6,7,8, 9]]]
#df_append[df_append["impound_num"].duplicated()]["impound_num"] = df_append[df_append["impound_num"].duplicated()]["impound_num"].apply(lambda x: f"{x}1")
df_append.to_csv("Dallas_AS_2014-2024.csv", index=False)
