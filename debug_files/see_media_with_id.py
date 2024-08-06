import requests
import os
from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")
media_id = "1404322560234430"
url = f'https://graph.facebook.com/v14.0/{media_id}'

# Set up the headers with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Make a GET request to the WhatsApp Business API to fetch media information
response = requests.get(url, headers=headers)

if response.status_code == 200:
    media_info = response.json()
    media_url = media_info.get('url')
    
    # Download the media
    media_response = requests.get(media_url, headers=headers)
    if media_response.status_code == 200:
        with open('media_file.jpg', 'wb') as f:
            f.write(media_response.content)
        print("Media downloaded successfully.")
    else:
        print("Failed to download media.")
else:
    print(f"Failed to fetch media information. Status code: {response.status_code}, Error: {response.text}")
