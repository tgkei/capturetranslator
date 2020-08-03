from googletrans import Translator


class Ocr_translator:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def translate(self, txt):
        translator = Translator()

        text = translator.translate(txt, src=self.src, dest=self.dest)

        return text.text
