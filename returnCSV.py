from pandas import DataFrame
from processJSON import Process


class CSV:

    def __init__(self, data):
        self.data = data

    def create_accomodation_df(self):
        
        accomodation_data = []
        for dictionary in self.data:
            row = [dictionary["name"], dictionary["destination"], dictionary["area"]]
            accomodation_data.append(row)
        
        df_accomodation = DataFrame(accomodation_data, columns = ["Name", "Destination", "Area"])
        df_accomodation.to_csv("accomodations.csv")

    def create_room_type_df(self):

        room_type_data = []
        for dictionary in self.data:

            """If it's a ground package, we need to add data to the second half of the dataframe"""
            if "ground" in dictionary["package_type"].lower():
                
                """ Transform our data so that we can get a dictionary of a room type and its respective rates """
                process = Process()
                dictionary_season = process.get_season(dictionary)
                rates = process.transform_season(dictionary_season)
                conservation_fee = process.find_conservation_fee(dictionary)

                for key in rates:
                    try:
                        row = [key, process.find_capacity(key), dictionary["name"], "", "", "", "", rates[key][0], rates[key][1], rates[key][2], conservation_fee]
                        room_type_data.append(row)
                    except Exception as e:
                        print(str(e))
                        message = "Manually Check this Lodge: " + dictionary["name"]
                        row = [message]
                        room_type_data.append(row)

            #"""If it's not a ground package aka FULL package, add it here"""
            else:
                """ Transform our data so that we can get a dictionary of a room type and its respective rates """
                process = Process()
                dictionary_season = process.get_season(dictionary)
                rates = process.transform_season(dictionary_season)
                conservation_fee = process.find_conservation_fee(dictionary)
                
                for key in rates:
                    try:
                        row = [key, process.find_capacity(key), dictionary["name"], rates[key][0], rates[key][1], rates[key][2], conservation_fee, "", "", "", ""]
                        room_type_data.append(row)
                    except Exception as e:
                        print(str(e))
                        message = "Manually Check this Lodge: " + dictionary["name"]
                        row = [message]
                        room_type_data.append(row)

        df_room_type = DataFrame(room_type_data, columns= ["Room Name", "Capacity", "Lodge Name", "Full-Board-High", "Full-Board-Medium", "Full-Board-Low", "Conservation-fee", "ground-package-high", "ground-package-medium", "ground-package-low", "Conservation-fee"])
        df_room_type.to_csv("room_type.csv")