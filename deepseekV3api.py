import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

app = Flask(__name__)

# 從環境變數獲取配置
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 初始化 LINE API 客戶端
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def call_deepseek_api(message):
    """調用 DeepSeek API 獲取回覆"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一個友善且樂於助人的AI助手"},
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


@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭
    signature = request.headers['X-Line-Signature']

    # 獲取請求內容
    body = request.get_data(as_text=True)
    app.logger.info("收到請求: " + body)

    # 處理 webhook 請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取用戶訊息
    user_message = event.message.text

    # 調用 DeepSeek API
    api_response = call_deepseek_api(user_message)

    # 處理回覆
    if api_response and 'choices' in api_response:
        ai_reply = api_response['choices'][0]['message']['content']
    else:
        ai_reply = "抱歉，我暫時無法處理您的請求，請稍後再試。"

    # 回覆用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_reply)
    )


@app.route('/')
def home():
    return "LINE Bot 服務運行中！請設定 Webhook URL 到 /callback"


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)