import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 115)
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
   engine.runAndWait()
