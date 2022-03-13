# Fcai_conversational-bot
Conversational AI bot using Rasa opensource 


# To Run Voice Bot:
	# Install Libraries:
		1- pip install SpeechRecognition
		2- pip install playsound
		3- pip install pipwin
		4- pipwin install pyaudio
		5- pip install gTTS
		6- pip install requests
		
	# Run these commands:
		1 - run these commands in terminal => rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
		2 - open another terminal and run this command => rasa run actions
		3 - run the voice_bot.py from ide or terminal 
		
	# Run The Custom Components:
	>> In "virtual_environment_Path"\lib\site-packages\rasa\nlu\registry.py
	>> You Should Add The following Code
	```
	sys.path.insert(1, folder_path)
	
	from reverse import Reverse , Print_Reversed
	```
	and add Reverse,Print_Reversed to component_classes list in registry.py 
