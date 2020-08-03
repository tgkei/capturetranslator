from capture.capture import Capture
from translator.translator import Ocr_translator

if __name__ == "__main__":
    string = Capture.to_str()
    string = string.replace("-\n", "")
    string = string.replace("\n", " ")
    print(string)
    translator = Ocr_translator("en", "ko")
    text = translator.translate(string)
    print(text)
