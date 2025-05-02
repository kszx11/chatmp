"""
chatmp.py -- MicroPython Pico W basic ChatGPT client
Connects to Wi-Fi, prompts for user input, sends to OpenAI ChatCompletion,
and prints assistant responses. Maintains a short history window.
"""
import network
import time
import ujson
import urequests
import sys
import config 
import wifi

# ----------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------
settings = config.read_config_settings()

API_KEY = settings["api_key"]
MODEL_NAME = settings["model_name"]

TEMPERATURE   = 0.7
TOP_P         = 1.0
MAX_TOKENS    = 200
HISTORY_LIMIT = 6  # number of user/assistant exchanges to keep

wlan = wifi.connect_wifi()
if not wlan:
    print("Failed to connect to Wi-Fi.")
    sys.exit(1)


# ----------------------------------------------------------------
# UTILITY FUNCTIONS
# ----------------------------------------------------------------
def call_openai(api_key, history):
    # trim history: keep system + last HISTORY_LIMIT*2 messages
    if len(history) > HISTORY_LIMIT * 2 + 1:
        history = [history[0]] + history[-HISTORY_LIMIT*2:]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = {
        "model":       MODEL_NAME,
        "messages":    history,
        "temperature": TEMPERATURE,
        "top_p":       TOP_P,
        "max_tokens":  MAX_TOKENS,
    }
    try:
        resp = urequests.post(url, headers=headers, data=ujson.dumps(body))
    except Exception as e:
        print("Network/API error:", e)
        return None
    if resp.status_code != 200:
        print("HTTP Error", resp.status_code, resp.text)
        resp.close()
        return None
    data = resp.json()
    resp.close()
    try:
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Invalid response format:", e)
        return None

# ----------------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------------
def main():    
    # Initialize conversation history with a system prompt
    system_msg = {
        "role": "system",
        "content": "You are ChatGPT, a helpful assistant."
    }
    history = [system_msg]
    print("\nWelcome to MicroPython ChatGPT!")
    print("Type your messages below. 'quit' to exit.")
    while True:
        try:
            user_input = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat.")
            break
        if not user_input:
            continue
        if user_input.lower() in ('quit','exit'):
            print("Goodbye!")
            break
        # Add user message
        history.append({"role": "user", "content": user_input})
        # Call OpenAI
        reply = call_openai(API_KEY, history)
        if reply is None:
            print("[Error] No response.")
            continue
        # Print and store assistant reply
        print(f"\n{reply}")
        history.append({"role": "assistant", "content": reply})

if __name__ == '__main__':
    main()
    
