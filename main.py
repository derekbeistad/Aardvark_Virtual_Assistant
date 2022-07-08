import os

# User Modules
from aardvark_speaks import aardvark_says
import handle_intent
import calculations
import capture_voice


def detect_intent(response):
    """
    Checks if detection was successful and executes command
    :param response:
    :return:
    """
    listen_successful = response['success']
    error = response['error']
    command = response['command']

    #check for error in response
    if not listen_successful:
        print(error)
        return error

    if command is None:
        return True

    #check for command
    if 'aardvark' in command:
        aardvark_command = command.replace('aardvark', '')

        #Check for keywords
        if 'volume' in command: # Change Computer Volume
            """adjusts volume with the command 'turn volume up' or 'turn volume down'"""
            adjust_volume = handle_intent.adjust_computer_volume(aardvark_command)
            aardvark_says(adjust_volume)
            return True

        elif 'time' in command:
            """Tells current time in 12 hour format"""
            time = handle_intent.get_time()
            print(time)
            aardvark_says(f"It is currently {time}")
            return True

        elif 'date' in command:
            """Tells current date"""
            date = handle_intent.get_date()
            print(date)
            aardvark_says(date)
            return True

        elif 'calculate' in command:
            """Calculates simple Math functions including:
            addition, subtraction, multiplication, division,
            powers, square roots, factorials, and log
            """
            if 'ad' in command:
                aardvark_command = aardvark_command.replace('ad','add')
            if 'for' in command:
                aardvark_command = aardvark_command.replace('for', '4')
            print("command:", command)
            calc_prompt = aardvark_command.replace('calculate ', '')
            calc_results = calculations.calculate(calc_prompt)
            result = str(calc_results[0])
            function = calc_results[1]
            print(function + ' = ' + result)
            aardvark_says(function + ' = ' + result)
            return True

        elif 'joke' in command: # Tells a joke
            """Tells a random dad joke"""
            joke_text = handle_intent.tell_joke()
            aardvark_says(joke_text)
            return True

        elif 'screenshot' in command: # Take a screenshot
            """captures and saves a screen shot of the
            current screen to the desktop"""
            handle_intent.take_screenshot()
            return True

        elif "news" in command: # Open Google News
            """Opens Google News in Google Chrome"""
            handle_intent.open_news()
            return True

        elif "directions" in command: # Open Directions in Google Maps
            """Opens up directions in Google Maps with Google Chrome"""
            to_location = aardvark_command.replace('give me directions to ', '')
            aardvark_says("Where are you leaving from?")
            print("where are you leaving from?")
            response = capture_voice.listen_from_mic()
            from_location = response['command']
            handle_intent.get_directions(from_location, to_location)
            return True

        elif 'play' in aardvark_command: # Play a song on YouTube
            """Opens up a youtube video in Google Chrome"""
            search_query = aardvark_command.replace('play', '').replace(' ', '+')
            handle_intent.play_song_on_youtube(search_query)
            return True

        elif 'tell me about' in aardvark_command: # Wiki Search with 2 sentence summary
            """Tells a 2 sentence summary about a topic via Wikipedia"""
            search_prompt = aardvark_command.replace('tell me about', '')
            wikipedia_summary = handle_intent.get_wikipedia_summary(search_prompt)
            print(wikipedia_summary)
            aardvark_says(wikipedia_summary)
            return True

        elif 'search for' in command: # Google search
            """Opens up a Google search for a term in Google Chrome"""
            key_words = aardvark_command.replace('search for', '')
            handle_intent.search_google(key_words)
            return True

        elif 'tell me the weather in' in aardvark_command: # Weather
            """Tells the current weather in a location queried"""
            location_text = aardvark_command.replace('tell me the weather in', '')
            weather = handle_intent.get_current_weather(location_text)
            handle_intent.print_weather_dict(weather)
            aardvark_says(f"The weather in {weather['weather_city']} is {weather['weather_category']}."
                          f"It is {weather['weather_temperature']} degrees fahrenheit with winds at"
                          f"{weather['weather_wind_speed']} miles per hour and {weather['weather_humidity']}"
                          f"humidity")
            return True

        elif "tell me the weather tomorrow in" in aardvark_command:  # Weather
            """Tells the current weather in a location queried"""
            location_text = aardvark_command.replace("tell me the weather tomorrow in", '')
            weather = handle_intent.get_tomorrow_weather(location_text)
            handle_intent.print_weather_dict(weather)
            aardvark_says(f"The weather tomorrow in {weather['weather_city']} will be {weather['weather_category']}."
                          f"It will be {weather['weather_temperature']} degrees fahrenheit with winds at"
                          f"{weather['weather_wind_speed']} miles per hour and {weather['weather_humidity']}"
                          f"humidity")
            return True

        elif 'quote' in aardvark_command or 'philosophy' in aardvark_command or 'philosophical' in aardvark_command:
            """Tells a Philosophical quote"""
            quote = handle_intent.get_quote()
            aardvark_says(quote)
            return True

        elif 'turn off' in aardvark_command:
            """Closes Aardvark"""
            aardvark_says("Goodbye dear friend")
            return False

        elif 'thank you' in aardvark_command:
            aardvark_says("You're welcome")
            return True

        elif 'hello' in aardvark_command or 'who are you' in aardvark_command:
            aardvark_says("Hello, I am an Aardvark, Can I help you?")
            return True

        else:
            return True
    return True


aardvark_is_on = True

# Open Instructions
os.system("open Aardvark_Virtual_Assistant_Instructions.pdf")

while aardvark_is_on:
    response = capture_voice.listen_from_mic()
    aardvark_is_on = detect_intent(response)
    if not aardvark_is_on:
        print("Closing")
