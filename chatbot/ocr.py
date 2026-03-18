import easyocr

reader = easyocr.Reader(["en", "hi"])

def extract_text_from_image(image_path):
    result = reader.readtext(image_path)
    return " ".join([i[1] for i in result])
