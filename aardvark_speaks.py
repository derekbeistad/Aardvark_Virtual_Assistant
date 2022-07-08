import pyttsx3

# Text to Speech Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[33].id)


def aardvark_says(text):
    """
    Takes a string as input and converts it to audio
    :param text:
    :return:
    """
    engine.say(text)
    engine.runAndWait()