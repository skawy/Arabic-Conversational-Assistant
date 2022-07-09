

<h1 align="center">
<img src="ARCA_Final_Logo.png" width="400" height = "400">
</h1>




<h2 align="center"><u>ARCA</u></h2>

<h2 align="center"><u>Intelligent Arabic Customer Service Assistant</u></h2>





## :surfer: Introduction

The purpose of this repository is to showcase a contextual AI assistant built with the open source Rasa framework.

ARCA is an alpha version giving FCAI students Academic Advising. It aims at helping each student identify his/her strengths and abilities to assist him/her in making decisions relevant to his/her studies and specialization and in overcoming any impediments at college.

The chatbot should be able to the following basic functionalities

- Helping you to make your own schedule

- knowing whether  you can study this subject or not

- which major is most suitable to you based on your grades

  

## :point_right: Installation

To install ARCA, please clone the repository and run:

```sh
cd FCAI_CU_Chatbot
pip install -r requirements.txt | pip3 install -r requirements.txt
```

This will install the bot and all of its requirements.
Note that this bot should be used with python 3.6 or 3.7.



## 🤖 To run ARCA

Use `rasa train` to train a model

Then, to run, first set up your action server in one terminal window:
```bash
rasa run actions 
```

Finally, in the second terminal window you can run and start your conversation	

```bash
rasa shell
```

Note that this bot should be used with Rasa 2.8



## :blue_book: Overview of the files

`data/core/` - contains stories 

`data/nlu` - contains NLU training data

`actions` - contains custom action code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble



## :sound: To Run Voice Bot (optional)

Use `rasa train` to train a model

These are the needed dependencies 

```bash
pip install SpeechRecognition
pip install playsound
pip install pipwin
pipwin install pyaudio
pip install gTTS
pip install requests
```

First Terminal

```bash
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
```

Second Terminals

```bash
rasa run actions
```

Finally you can run the voice_bot.py from IIDE or terminal.

Note that the bot must be trained before running this python file.
