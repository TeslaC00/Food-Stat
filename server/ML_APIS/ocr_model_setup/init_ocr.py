import easyocr

def initialize_reader():
    # Initialize the reader with English language support
    reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a compatible GPU
    print("OCR Reader Initialized!")
    return reader
