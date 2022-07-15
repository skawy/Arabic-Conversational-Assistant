import requests
import json
import os

def resume_conversation(sender_id):

    url = f"https://9d4b-104-248-131-192.eu.ngrok.io/conversations/{sender_id}/tracker/events"
    headers = {"Content-Type": "application/json"}
    data = [{"event": "resume"}]
    
    # If The printed text is None then there is no user with this sender_id
    # response = requests.post(url=url, data=json.dumps(data), headers=headers).text
    # response_dict = json.loads(response)
    # print(response_dict["latest_message"]["text"])

    return requests.post(url=url, data=json.dumps(data), headers=headers)



file = open('paused_ids.txt', 'r')
lines = file.readlines()

for line in lines:
    resume_conversation(line.strip())


os.remove("paused_ids.txt")