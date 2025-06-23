from toImage import Convert
from parseText import Parse
from google import genai
from returnCSV import CSV
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
""" Turn PDF into images; extract text from images """
def getTextFromImage():

    convert = Convert(tes_path= r"C:\Program Files\Tesseract-OCR\tesseract.exe", pdf_path= r"C:\Users\Chubb\Downloads\UTF-8''2025-Saruni-Basecamp-Rack-Rates.pdf")
    texts = convert.imageTexts()
    return texts

""" Return dictionary of data from texts extracted from each image """
def getDataFromText(texts: list[str]):

    formatted_data = []
    for i in texts:

        """ Return dictionary of the data we found from the text """
        parse = Parse(text = i, client = client)
        data = parse.format()
        print(data)
        if data == "Resource Exhausted":
            print("We will stop the program here, here is the current data we have successfully retrieved")
            break

        elif data == "Failed to convert data":
            print("Failed to convert data")

        else:
            formatted_data.append(data["safari_camp"])

    return formatted_data

def create_dataframes(data):
    
    csv = CSV(data)
    csv.create_accomodation_df()
    csv.create_room_type_df()

def main():

    texts = getTextFromImage()
    data = getDataFromText(texts = texts)
    create_dataframes(data)

if __name__ == '__main__':
    main()