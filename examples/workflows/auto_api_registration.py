import asyncio
import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()

SITE_SIGNUP_URL = os.getenv("SITE_SIGNUP_URL", "https://example.com/signup")
API_SETTINGS_URL = os.getenv("API_SETTINGS_URL", "https://example.com/settings/api")
EMAIL_ADDRESS = os.getenv("REG_EMAIL", "user@example.com")
EMAIL_PASSWORD = os.getenv("REG_EMAIL_PASSWORD", "password")

TASK = f"""
1. Navigate to {SITE_SIGNUP_URL}.
2. Register a new account with email {EMAIL_ADDRESS} and a secure password of your choice.
3. Check the inbox for {EMAIL_ADDRESS} using IMAP and open the verification link in the message.
4. Once verified, visit {API_SETTINGS_URL} and create a new API key.
5. Save the generated API key locally using Python.
"""

browser = Browser()
agent = Agent(task=TASK, llm=ChatOpenAI(model='gpt-4o'), browser=browser)

async def main():
    history = await agent.run(max_steps=50)
    api_key = agent.browser.ctx.shared_state.get("api_key")
    if api_key:
        keys_path = os.path.join(os.path.dirname(__file__), "api_keys.json")
        try:
            with open(keys_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        domain = SITE_SIGNUP_URL.split('/')[2]
        data[domain] = api_key
        with open(keys_path, "w") as f:
            json.dump(data, f, indent=2)
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

