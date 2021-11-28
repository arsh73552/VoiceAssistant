import os
import speech_recognition as sr
import datetime
import playsound
import webbrowser
from gtts import gTTS
import urllib.request
import re
from googlesearch import search
import subprocess

def say(string):
    my_speech = gTTS(text=string, lang='en') # Use gtts to get speech from a string.
    my_speech.save("welcome.mp3") # save speech as welcome.mp3.
    playsound.playsound('welcome.mp3') # Play the saved speech
    os.remove('welcome.mp3') # Remove the file where we saved speech
    print(string) # Print user's speech

def input_audio():    # user_input Audio
    r = sr.Recognizer()
    with sr.Microphone() as source: # Use Default microphone as input source.
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold=0.5 # Wait for 0.5 of pause in speech seconds till termination
        audio = r.listen(source)  # Listen to users audio.
    try:
        print(r.recognize_google(audio).lower()) # Print users audio.
        return r.recognize_google(audio).lower() # Return users audio as text to main function.
    except:
        return 'fail';   # In case audio isn't understandable.

def greetings():
    say("Good morning, how may i help you?") #Greets the user.

if __name__ == '__main__':
    greetings()
    affirmations=["yes","yeah","ya","yup","yep"] # Affirmations in case user agrees to a certain request/question.
    while True:   #Infinite loop till the user terminates by saying exit() or the audio isn't understandable.
        user_input=input_audio() #Save user audio in a variable called user_input.
        print("Processing...")

        if user_input=='fail':
            print("Couldn't Understand.")
            exit()   #EXIT if input fails

        if "google" in user_input:
            unwanted_words=["google"] # List of unwanted_words words while googling.
            counter=0
            query=" ".join([word for word in user_input.split() if word not in unwanted_words]) # Remove the list of unwanted words.
            say(f"Showing results related to {query}") # Use the say function to give user output.
            for j in search(query, tld="co.in", num=10, stop=10, pause=2): # Searches for the first link when you google the query.
                webbrowser.open(j,new=0) # opens first link
                break
            say("Would you like another link?")
            inp=input_audio()
            if 'yes' in inp: # Open the second link from the top if the user wants another link
                for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                    if counter==1:
                        webbrowser.open(j,new=0)
                    counter=counter+1

        elif "time" in user_input:
            time=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}") #Tells current time.

        elif "youtube" in user_input:
            unwanted_words=["youtube","search","for","on"] # List of unwanted_words words while searching on youtube.
            a="+".join([word for word in user_input.split() if word not in unwanted_words]) # Removing unwanted words.
            url='https://www.youtube.com/results?search_query='+a # forming a URL using the list of remaining words.
            webbrowser.open(url,new=0)  #Searches stuff on youtube

        elif "twitter" in user_input:
            webbrowser.open('https://twitter.com/home',new=0) #Opens twitter

        elif "facebook" in user_input:
            webbrowser.open('https://www.facebook.com/',new=0) #Opens facebook

        elif "open" in user_input or "launch" in user_input: # open applications
            unwanted_words=["open", "launch"] # List of unwanted words
            query=" ".join([word for word in user_input.split() if word not in unwanted_words]) # Remove list of unwanted words.
            application_dict={"calculator":"calc","file explorer":"explorer","notepad":"notepad","paint":"mspaint","microsoft paint":"mspaint","command prompt":"cmd","cmd":"cmd"}
            subprocess.call("start "+ application_dict[query],shell = True)  #Using a dictionary  open required application
            say("{} has been opened".format(query))

        elif "music" in user_input:
            say("What kind of music would you like to listen to?") # Ask music preference.
            bad_words=["music","songs","play"] # List of unwanted words.
            minput=input_audio() #Get response
            b="+".join([word for word in minput.split() if word not in bad_words]) # Make
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + b)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode()) # Get 11 digit code found after every YT vid
            webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0],new=0) #Plays music off YT

        elif "exit" in user_input:
            exit() #Exits.

        else:
            say("I couldn't quite understand that!")
            say("Would you like me to prepare a google search for the same though?")
            einp=input_audio()
            if any(word in einp for word in affirmations):
                unwanted_words=["google"] # List of unwanted words
                counter=0
                query=" ".join([word for word in user_input.split() if word not in unwanted_words]) # Remove unwanted words
                say(f"Showing results related to {query}")
                for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                    webbrowser.open(j,new=0)
                    break
                say("Would you like another link?")
                einp=input_audio()
                if any(word in einp for word in affirmations):
                    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                        if counter==1:
                            webbrowser.open(j,new=0)
                        counter=counter+1   #Prepare google search for text.

        say("Would that be all?")
        user_input=input_audio()

        if any(word in user_input for word in affirmations):
            exit() #exit
        else:
            say("How may i help you?") #loop
