from googletrans import Translator

translator = Translator()

text = translator.translate("I am lion.", dest="ko")

print(text.text)
