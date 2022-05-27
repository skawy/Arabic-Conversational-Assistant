""" Read Read me file """

# import  libraries
import playsound
import requests
import speech_recognition as sr
#from gtts import gTTS
import os


def post_and_get(message):
    """ send and get rasa and user messages from localhost server """
    request = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
    print("الرد: ", end='')
    bot_message = ''
    for i in request.json():
        bot_message = i['text']
        print(f"{bot_message}")
    return bot_message


# def speak(bot_message):
#     """ convert rasa's response message to voice """
#     file_name = "bot_response.mp3"
#
#     tts = gTTS(text=bot_message, lang='ar')
#     tts.save(file_name)  # save converted text as mp3
#
#     # Playing the converted file
#     playsound.playsound(file_name)
#     os.remove(file_name)


def recognize(bot_message):
    """ recognize user's message and convert it to text """
    while "شكرا" not in bot_message:
        message = ''
        recognizer = sr.Recognizer()  # initialize recognizer
        with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
            print("تكلم :")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.pause_threshold = 0.7
            audio = recognizer.listen(source)  # listen to the source
            try:
                message = recognizer.recognize_google(audio,
                                                      language='ar-eg')  # use recognizer to convert our audio into text part.
                print("طلبك : {}".format(message))
            except:
                print("مش سامعك")  # In case of voice not recognized  clearly
                # speak('مش سامعك')

        if len(message) != 0:
            bot_message = post_and_get(message)  # get rasa bot response
            # speak(bot_message)  # convert rasa bot response to text


def main():
    """ main function let the bot to start the conversation """
    bot_message = ''
    while "شكرا" not in bot_message:
        message = input()
        bot_message = post_and_get(message)
    # speak(bot_message)
    # recognize(bot_message)


if __name__ == '__main__':
    main()
