from pdf2image import convert_from_path
from pytesseract import pytesseract
import cv2
import numpy

class Convert():

    """
    Class has instance variables: One path for pytesseract exe and one to our pdf file
    """
    def __init__(self, tes_path: str, pdf_path: str):
        self.tes_path = tes_path
        self.pdf_path = pdf_path

    """
    Returns an array of images that are black and white
    """
    def imageToGray(self):

        """Convert PDF into list of Pillow Images & add file path"""
        images = convert_from_path(self.pdf_path)
        pytesseract.tesseract_cmd = self.tes_path

        """ Return array of images """
        np_images = []

        """Convert Pillow Objects into Numpy Array; Afterwards, turn images into GRAYSCALE"""
        for image in images:

            """ Convert image into an array and set it to Gray Scale. If the pixel is above 120, set it to 0 (black). 
            If the pixel is below 120, set it to 255 (white).  We want to turn the background black, and the text white """
            image = numpy.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            threshold, image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY_INV)
            np_images.append(image)
            
        return np_images
        
    """ Return array of text of each image """
    def imageTexts(self):
        
        np_images = self.imageToGray()
        texts = []
        for image in np_images:
            text = pytesseract.image_to_string(image).lower()

            """ Only add Texts that contain our rates """
            if "high season" in text and "mid-season" in text and "low season" in text:
                texts.append(text)
        return texts
