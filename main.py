from toImage import Convert
from parseText import Parse
from google import genai
from toJSON import JSON
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
""" Turn PDF into images; extract text from images """
def getTextFromImage():

    convert = Convert(tes_path= r"C:\Program Files\Tesseract-OCR\tesseract.exe", pdf_path= r"C:\Users\Chubb\Downloads\2025 Soroi Silver Non-Resident Contracted Rates1.pdf")
    texts = convert.imageTexts()
    return texts

""" Return dictionary of data from texts extracted from each image """
def getDataFromText(texts: list[str]):

    formatted_data = []
    for i in texts:

        """ Return dictionary of the data we found from the text """
        parse = Parse(text = i, client = client)
        datas = parse.format()
        #print(datas)
        if datas == "Resource Exhausted":
            print("We will stop the program here, here is the current data we have successfully retrieved")
            break

        elif datas == "Failed to convert data":
            print("Failed to convert data")

        else:
            for data in datas:
                formatted_data.append(data["safari_camp"])


    return formatted_data

def toCSV(data):
    json = JSON(data)
    json.to_csv()

def main():

    texts = getTextFromImage()
    data = getDataFromText(texts = texts)
    toCSV(data)

if __name__ == '__main__':
    main()