import requests
import os
from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")
# recipient_phone_number = os.getenv("RECEIPIENT_PHONE_NUMBER")

class whatsapp:
    def send_reminder(self, message_text, recipient_phone_number):
        url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "yes_button",
                                "title": "Yes"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "no_button",
                                "title": "No"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "graph_button",
                                "title": "Generate Graph"
                            }
                        }
                    ]
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Failed to send message: {response.status_code}")
            response_data = response.json()
            print(response_data)
        
        message_id = response.json().get("messages")[0].get("id")

        return {"status": response.status_code, "message_id": message_id}

    def send_text(self, message_text, recipient_phone_number):
        url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            'messaging_product': 'whatsapp',
            'to': recipient_phone_number,
            'type': 'text',
            'text': {
                'body': message_text
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        message_id = response.json().get("messages")[0].get("id")

        return {"status": response.status_code, "message_id": message_id}
    
    def send_images(self, image_bytecode, recipient_phone_number):
        send_url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
        media_id = self.__upload_image(image_bytecode)["message_id"]

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "image",
            "image": {
                "id": media_id
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(send_url, headers=headers, json=payload)
        return {"status": response.status_code, "media_id": media_id}


    def receive(self, data):
        message_data = data['entry'][0]['changes'][0]['value']['messages'][0]

        message_id = message_data['context']['id']
        timestamp = message_data['timestamp']
        text_body = message_data['interactive']['button_reply']['id']

        extracted_data = {
            'replied_id': message_id,
            'timestamp': timestamp,
            'text': text_body
        }

        return extracted_data
    
    def __upload_image(self, image_data):
        # image_data = base64.b64decode(image_base64)
        upload_url = f"https://graph.facebook.com/v13.0/{phone_number_id}/media"

        files = {
            'file': ('image.jpg', image_data, 'image/jpeg')
        }

        payload = {
            "messaging_product": "whatsapp"
        }

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(upload_url, headers=headers, files=files, data=payload)

        media_id = response.json().get('id')
        
        return {"status": response.status_code, "message_id": media_id}


