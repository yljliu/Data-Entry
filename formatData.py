from google import genai
from google.genai import types
from google.genai.errors import ClientError
import json
import time

class Format:

    """ Create class that utilizes parsed text from the image and API key """
    def __init__(self, data: str, client: genai.Client):
        self.data = data
        self.client = client

    """ Give Gemini AI the instructions on how to format the data """
    def system_instructions(self):
        instructions = """Organize the following safari camp data into JSON format. 
        I want a clear breakdown of the room rates by season, type of room, and occupancy. Include the destination, area, type of package, and conservation fees. 

        For example:
        {
            "safari_camp": {
                "name": "Saruni Samburu",
                "destination": "Samburu, Northern Kenya",
                "area": "Kalama Conservancy",
                "package_type": "Ground Package (includes game drives)",
                "conservation_fees": 130,  
                "high_season": {
                        "villa_double_occupancy": 1000,
                        "villa_single_occupancy": 1180,
                        "honeymoon_villa": 1000,
                        "family_villa_per_unit_up_to_4_pax": 4000
                },
                "mid_season": {
                        "villa_double_occupancy": 900,
                        "villa_single_occupancy": 1030,
                        "honeymoon_villa": 900,
                        "family_villa_per_unit_up_to_4_pax": 3600  
                },
                "low_season": {
                        "villa_double_occupancy": 800,
                        "villa_single_occupancy": 920,
                        "honeymoon_villa": 800,
                        "family_villa_per_unit_up_to_4_pax": 3200     
                },              
            }
        }

        Notes: Please use the exact keys as the above. Please keep the data structured the exact same way.
        If conservation fees are not listed, set the value to "N/A".
        Only use the keys "high_season", "mid_season", and "low_season" for room rates.
        If a room rate is not provided for a particular season, include the room name with a value of -1.
        If you find both ground package and full board package in the same text, separate them into 2 json objects and give me the array of the JSON objects. Otherwise, return me a JSON object in a square bracket
        """
        return instructions

    """ Call Gemini AI """
    def organize(self):

        times_slept = 0
        sleep_time = 2

        while True:
            try:
                response = self.client.models.generate_content(
                    model = "gemini-2.0-flash",
                    contents = ["Can you format the following text: " + self.data],
                    config = types.GenerateContentConfig(
                        system_instruction = self.system_instructions()
                    )
                )
                return response.text
            except ClientError as e:
                times_slept = times_slept + 1

                if times_slept > 6:
                    print("Tried to ask Gemini 6 times; exiting program")
                    return "Resource Exhausted"
                
                time.sleep(sleep_time)
                sleep_time = sleep_time * 2.1

    """ Format the json data from Gemini API """        
    def format_json_data(self, json_data: str):

        lines = json_data.splitlines()

        """ The first element is equal to  ```json; we want to get rid of that """
        if lines[0] == "```json":
            lines.pop(0)

        """ The last element is equal to  ```; we want to get rid of that """
        if lines[len(lines) - 1] == "```":
            lines.pop()

        """ Join the lines together, separated by a new line """
        result = "\n".join(lines)
        
        # for i in range(3):
        #     json_data.pop()
        # for i in range(7):
        #     json_data.pop(0)

        return result
        
    """ Calls the previous methods; returns a dictionary of the data we receive from Gemini """
    def format_data(self):

        times_slept = 0
        sleep_time = 2.0

        while True:
            try:
                json_data = self.organize()
                #print(json_data)
                if json_data == "Resource Exhausted":
                    return "Resource Exhausted"
                
                else:
                    json_data = self.format_json_data(json_data)
                    list_of_JSON = json.loads(json_data)
                    return list_of_JSON
                
            except json.JSONDecodeError as e:
                times_slept = times_slept + 1

                if times_slept > 3:
                    return "Failed to decode JSON data 3 times, manually check this data"
                
                time.sleep(sleep_time)
                sleep_time = sleep_time * 3.2
                
                