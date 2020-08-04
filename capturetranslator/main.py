from capture.capture import Capture
from translator.translator import Ocr_translator
from argparse import ArgumentParser

if __name__ == "__main__":
    # parsing cli input
    parser = ArgumentParser(description="Capture string of image and translate it")
    parser.add_argument("-src", "--source", default="en")
    parser.add_argument("-des", "--destination", default="ko")
    args = parser.parse_args()

    src = args.source
    des = args.destination

    # capture the image and detect string
    string = Capture.to_str()
    string = string.replace("-\n", "")
    string = string.replace("\n", " ")
    print(string)

    # translate
    translator = Ocr_translator(src, des)
    text = translator.translate(string)
    print(text)
