import os
import uvicorn
from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv
from gradio.external_utils import conversational_wrapper
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

# 載入 .env 環境變數
load_dotenv()

# FastAPI 應用初始化
app = FastAPI()

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def call_deepseek_api(message: str):
    """呼叫 DeepSeek API 取得回應"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }


    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一個股市分析師嘎偉老蘇。嘎偉老蘇最常說的就是嘎偉老蘇大獲全勝、多蛙VV叫。嘎偉老蘇有一首童謠：一二一，拜登基，殺爆台股，殺台積"},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }



    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API 請求失敗: {e}")
        return None


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    api_response = call_deepseek_api(user_message)

    if api_response and 'choices' in api_response:
        ai_reply = api_response['choices'][0]['message']['content']
    else:
        ai_reply = "抱歉，我暫時無法處理您的請求，請稍後再試。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_reply)
    )


@app.get("/")
async def root():
    return {"message": "LINE Bot 服務運行中！請設定 Webhook URL 為 /callback"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
