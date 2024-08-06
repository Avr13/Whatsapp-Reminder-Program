from messages import whatsapp
from process_routine import reg_routine
from analyze import graph

from datetime import datetime, time, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

phone_numbers = ["+918697340722","+917417768031"]
reminders = []
loaded = False
eod_graph = False

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_whatsapp_messages())

async def send_whatsapp_messages():
    global loaded, reminders
    while True:
        now = datetime.now()
        eod = datetime.combine(now, time.max)
        if eod - timedelta(minutes=2)<=now or not loaded:
            loaded = True
            eod_graph = False
            reminders=reminders + reg_routine().load()

        if reminders:
            reminder =  reminders[0]
            if reminder["start_time"]<now:
                    for number in phone_numbers:
                        send_message = whatsapp().send_reminder("REMINDER \n" + reminder["task"], number)
                        if number != "+918697340722":
                            reminder["message_id"] = send_message["message_id"]

        if now>=eod - timedelta(hours=2) and not eod_graph:
            all_graphs = graph().generate()
            for number in phone_numbers:   
                for graphs in all_graphs:
                    sent_image = whatsapp().send_images(graphs, number)
                    # whatsapp().send_text(message_text=sent_image["media_id"], recipient_phone_number=number)
            eod_graph = True

        print(reminders)
        await asyncio.sleep(10)

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return JSONResponse(content=int(challenge))

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    if "messages" in data['entry'][0]['changes'][0]['value']:
        reply_data = whatsapp().receive(data=data)

        if reply_data["text"] == "graph_button":
            all_graphs = graph().generate()
            for number in phone_numbers:   
                for graphs in all_graphs:
                    sent_image = whatsapp().send_images(graphs, number)
                    # whatsapp().send_text(message_text=sent_image["media_id"], recipient_phone_number=number)

        else:
            for reminder in reminders:
                if reminder["message_id"] == reply_data["replied_id"]:
                    if reply_data["text"] == "yes_button":
                        reg_routine().add_to_excel(data={"Task":reminder["task"], "Datetime": datetime.now(), "Status": 1})
                    else:
                        reg_routine().add_to_excel(data={"Task":reminder["task"], "Datetime": datetime.now(), "Status": 0})
                    reminders.remove(reminder)

                if datetime.now()>reminder["end_time"]:
                    reg_routine().add_to_excel(data={"Task":reminder["task"], "Datetime": datetime.now(), "Status": 0})
                    for number in phone_numbers:
                        whatsapp().send_text("Marking the task as undone", number)
                    reminders.remove(reminder)
                    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
