import json
import pandas as pd
from processJSON import Process

class JSON():

    def __init__(self, array_of_data):
        self.data = array_of_data
    
    def write(self):

        with open("json.json", "w") as file:
            file.write("[")
            for i in range(len(self.data)):
                json.dump(self.data[i], file)
                if i != (len(self.data) - 1):
                    file.write(',\n')
            file.write("]")
    
    def to_csv(self):

        self.write()

        with open("json.json", "r") as json_file:
            json_data = json.load(json_file)
        #print(json_data)

        df = pd.DataFrame()
        for i in json_data:
            if df.empty:
                df = pd.DataFrame.from_dict(i)
            else:
                temp = pd.DataFrame.from_dict(i)
                df = pd.concat([df, temp])
        df['Capacity'] = pd.Series([])
        #print(df)
        process = Process()
        for r in range(len(df)):
            row = df.iloc[r]
            multiply = process.room_name(row.name)
            
            if row['high_season'] != -1:
                row['high_season'] = row['high_season'] * multiply
            if row['mid_season'] != -1:
                row['mid_season'] = row['mid_season'] * multiply
            if row['low_season'] != -1:
                row['low_season'] = row['low_season'] * multiply
            
            row.to_frame()
            df.iloc[r] = row
        
        area = df.loc[:, ["name", "destination", "area"]]
        area.to_csv("area.csv", index=False)

        room_type = df.loc[:,  ['package_type','conservation_fees','high_season','mid_season','low_season', 'Capacity']]
        room_type.to_csv("room_type.csv")