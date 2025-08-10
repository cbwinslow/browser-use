import asyncio
import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()

EMAIL_ADDRESS = os.getenv('REG_EMAIL', 'user@example.com')
EMAIL_PASSWORD = os.getenv('REG_EMAIL_PASSWORD', 'password')
WEBSITES_FILE = os.getenv('WEBSITES_FILE', 'websites.json')


def load_websites(path: str) -> list[dict]:
	try:
		with open(path) as f:
			data = json.load(f)
	except FileNotFoundError:
		return []
	return data.get('websites', [])


async def register_on_site(browser: Browser, signup_url: str, api_settings_url: str) -> str | None:
	task = f"""
    1. Navigate to {signup_url}.
    2. Sign up or log in using email {EMAIL_ADDRESS} and the provided password.
    3. Check the inbox for {EMAIL_ADDRESS} using IMAP and open the verification link if present.
    4. Visit {api_settings_url} and create a new API key.
    5. Store the key in `browser.ctx.shared_state[\"api_key\"]`.
    """
	agent = Agent(task=task, llm=ChatOpenAI(model='gpt-4o'), browser=browser)
	await agent.run(max_steps=50)
	return browser.ctx.shared_state.get('api_key')


async def main() -> None:
	websites = load_websites(WEBSITES_FILE)
	browser = Browser()
	keys: dict[str, str] = {}
	for site in websites:
		signup_url = site.get('signup_url')
		api_url = site.get('api_settings_url')
		if not signup_url or not api_url:
			continue
		api_key = await register_on_site(browser, signup_url, api_url)
		if api_key:
			domain = signup_url.split('/')[2]
			keys[domain] = api_key
	await browser.close()
	if keys:
		file_path = os.path.join(os.path.dirname(__file__), 'api_keys.json')

		def write_keys() -> None:
			with open(file_path, 'w') as f:
				json.dump(keys, f, indent=2)

		await asyncio.to_thread(write_keys)


if __name__ == '__main__':
	asyncio.run(main())
