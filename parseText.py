from google import genai
from google.genai import types
from formatData import Format
from google.genai.errors import ClientError
import time

class Parse:

    """Initiate our class with text, convert all text to lower case"""
    def __init__(self, text: str, client: genai.Client):
        self.text = text
        self.client = client

    """ System instructions on what to extract from the text we found from our image """
    def system_instructions(self):
        instructions = """You are given a rate sheet for a safari camp. Please extract the following structured information:

                1. Name of the safari camp
                2. Destination of the safari camp (e.g. Masai Mara, Lake Nakuru)
                3. Area of the safari camp (e.g. Narok, Aruba Dam)
                4. Type of package: If the rate includes game drives, label it as a ground package. If it only includes meals/accommodation without game drives, label it as a full-board package.
                5. List each room type with its per-person nightly rate, organized by High Season, Mid Season, and Low Season. 
                   Exclude child rates. If a room type does not explicitly say 'honeymoon' or 'family', and there’s a separate single occupancy rate, then:
                Create two versions of the room:
                        -One for double occupancy (using the shared rate)
                        -One for single occupancy (using the single rate)
                6. Include conservation or park/reserve entry fees (e.g. Masai Mara Reserve fees), and specify if they vary by season. Ignore Child Fees"""

        
        return instructions

    """ Ask the AI to parse our text: if successful, return the parsed text otherwise if we exhaust our resources, exit the program """
    def parse(self):
        
        times_slept = 0
        sleep_time = 2
        while True:
            try:
                response = self.client.models.generate_content(
                    model = "gemini-2.0-flash",
                    contents = ["Can you extract the safari rates from this text: " + self.text],
                    config = types.GenerateContentConfig(
                        system_instruction = self.system_instructions()
                    )
                )
                return response.text
            except ClientError as e:
                times_slept = times_slept + 1

                if times_slept > 6:
                    print("Tried to ask Gemini 6 times; exiting program\n")
                    return "Resource Exhausted"
                
                time.sleep(sleep_time)
                sleep_time = sleep_time * 2.05
        

    """ Format the data we parsed into a dictionary """
    def format(self):

        text = self.parse()

        if text == "Resource Exhausted":
            print("Resouce Exhausted, please lower the amount of images you are inputting into the program")
            return "Resource Exhausted"
        
        else:
            format = Format(data = text, client = self.client)

            """ 
            Get the actual data from Gemini 
            
                1. If we have exhausted the Gemini API, return that
                2. If we Failed to convert our data, return failure
                3. IF we succeed, return the dictionary

            """
            data_in_dictionary = format.format_data()
            if data_in_dictionary == "Resource Exhausted":
                return "Resource Exhausted"
            elif data_in_dictionary == "Failed to decode JSON data 3 times, manually check this data":
                return "Failed to convert data"
            else:
                return data_in_dictionary

        