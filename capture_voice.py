import speech_recognition as sr


def listen_from_mic():
    """Transcribe audio recorded from the microphone.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether the API request was successful
    "error":   `None` if no error occurred, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "command": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # speech_recognition Setup
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source, phrase_time_limit=15)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "command": None
    }

    # try to recognize text from the mic
    try:
        response["command"] = recognizer.recognize_google(voice).lower()
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response