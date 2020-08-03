from googletrans import Translator

translator = Translator()

text = translator.translate("Hi.", dest="ko")

print(text.text)
