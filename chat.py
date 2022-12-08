import requests as rq
import uuid
import json
from config import *
from openai_async import Chat
import asyncio

rq.packages.urllib3.disable_warnings()

async def chatgpt(text, access_token):
    try:
        resp = rq.post("https://chat.openai.com/backend-api/conversation", 
            headers={
                "Authorization": "Bearer " + access_token,
                "User-Agent": UA,
            },
            json={
                "action": "next",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "content_type": "text",
                            "parts": [
                                text
                            ]
                        }
                    }
                ],
                "parent_message_id": str(uuid.uuid4()),
                "model": "text-davinci-002-render"
            },
            verify=False,
            proxies=PROXY,
            timeout=3
        )
    except Exception as e:
        print(f"ChatGPT could not complete the request: {repr(e)}")
        receiver = Chat.Chatbot(api_key=OPENAI_KEY, conversation_id=uuid.uuid4())
        prompt = text
        response = await receiver.get_chat_response(model="text-davinci-003", prompt=str(prompt),
                                                max_tokens=int(1000))
        ai_res = response["choices"][0]["text"]
    else:
        ai_res = json.loads(resp.text.split("data: ")[-2])["message"]["content"]["parts"][0]
    
    return ai_res

def get_chat_token():
    if not AUTHORIZATION:
        print("Please edit this script to insert your __Secure-next-auth.session-token cookie found at https://chat.openai.com/chat")
        raise ValueError("No valid OpenAI API key found")
    headers = {
        "User-Agent": UA
    }   
    res = rq.get("https://chat.openai.com/api/auth/session", headers=headers, cookies={"__Secure-next-auth.session-token": AUTHORIZATION}, verify=False, proxies=PROXY)
    if res.status_code != 200:
        print("Failed to get session")
        return ValueError("Failed to get session")
    return res.json()["accessToken"]


if __name__ == "__main__":
    try:
        token = get_chat_token()
    except Exception as e:
        print(e)
    asyncio.run(chatgpt("aa", token))