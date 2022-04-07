import json
import time
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()
config = dotenv_values(".env")

webhook_url = config['WEBHOOK_URL']
lodestone_api_url = config['LODESTONE_BASE_API_URL']
endpoints = ["topics", "notices", "maintenance", "updates", "status", "developers"]

def postWebhook(webhook_data):
    print("Processing API request...")
    response = requests.post(
        webhook_url, json=webhook_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to Guilded returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return response

def getPosts():
    for endpoint in endpoints:
        print("Processing", endpoint, "endpoint...")
        # Do request
        endpoint_url = lodestone_api_url + endpoint + "?locale=eu"
        response = requests.get(endpoint_url)
        json_data = response.json()
        response_id = ""
        url = ""
        title = ""
        response_time = ""
        image = "https://img.finalfantasyxiv.com/lds/promo/h/j/38ANLXxLs-RiE9KlJpW0awtygY.png"
        description = ""
        webhook_data = {}
        if "id" in json_data[0]:
            response_id = json_data[0]['id']
            with open(f'latest_{endpoint}.json') as infile:
                data = json.load(infile)
                if(data['id'] == response_id):
                    print('Post already exists, skipping...')
                    continue
                else:
                    with open(f'latest_{endpoint}.json', 'w') as outfile:
                        data = {
                            "id": response_id
                        }
                        json.dump(data, outfile)
                        if "url" in json_data[0]:
                            url = json_data[0]['url']
                        if "title" in json_data[0]:
                            title = json_data[0]['title']
                        if "time" in json_data[0]:
                            response_time = json_data[0]['time']
                        if "image" in json_data[0]:
                            image = json_data[0]['image']
                        if "description" in json_data[0]:
                            description = json_data[0]['description']

                        webhook_data = {
                                "embeds": [
                                    {
                                        "author": {
                                            "name": "The Lodestone"
                                        },
                                        "title": title,
                                        "url": url,
                                        "description": description,
                                        "image":{
                                            "url": image
                                        },
                                        "footer":{
                                            "icon_url":"https://ffxiv.gamerescape.com/w/images/4/48/Mob15_Icon.png",
                                            "text": f"Posted at {response_time}"
                                        }
                                    }
                                ]
                            }
                        postWebhook(webhook_data)
                        print("Created new webhook post for", endpoint, "endpoint")

def main():
    while(True):
        print("Polling data...")
        getPosts()
        print("Waiting for next poll...")
        time.sleep(1200)

main()