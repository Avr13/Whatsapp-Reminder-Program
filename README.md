# Whatsapp-Reminder_Program
This program will keep on reminding you your tasks everyday through whatsapp and generate graphs based on your task completions. Maintain your everyday routine.

Steps to run the code

## Activate Virtual Environment
```
python3 -m venv .venv

# 👇️ activate on Linux or MacOS
source .venv/bin/activate

# 👇️ deactivate virtual environment
deactivate

# 👇️ activate on Windows (cmd.exe)
.venv\Scripts\activate.bat

# 👇️ activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

```

## Run

1. Create conda environment with python = 3.11.5

2. Activate conda and install requirements.txt 

    ```pip install -r requirements.txt```

3. Fill in the routine.xlsx file with the task name and the time in hh:mm:ssm. This time will be used everyday to remind the tasks.

5. Run FastAPI server - in conda environment

    ```python main.py```

## Set your Account in Meta
1. Create an whatsapp app
 ```https://developers.facebook.com/apps/?show_reminder=true```
2. Use the temporary token/create a permanent access_token to use.
3. Set up the webhook either using ngrok on the port 8000 or using a cloud webserver link.
    - The callback url should be http://webserver_link/webhook
    - The verify token should be the same as you give in the .env file of the program
4. Allow message option

## Note
1. The formats of xlsx files are absolute. Do not change it
2. Send a message to the test number first in order to start sending message through the application. 
3. Wait for 2-3 days after registering the test number for the graphs to send on the number.

