import subprocess
import threading
from fastapi import FastAPI

app = FastAPI()

def start_bot():
    # Launches telegram_bot.py in a separate process
    subprocess.run(["python", "telegram_bot.py"])

@app.on_event("startup")
def startup_event():
    # Spawns process thread on app launch
    thread = threading.Thread(target=start_bot, daemon=True)
    thread.start()

@app.get("/")
def root():
    return {"status": "BOF Pro API is Live"}
