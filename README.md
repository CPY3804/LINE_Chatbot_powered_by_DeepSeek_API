# LINE-Chatbot-powered-by-DeepSeek
Introduction：用Ai輔助，在本地架設deepseek model，或是用API的LINE聊天機器人，之後可以依據需求加上回答特定問題或建立AI背景。

Feature：
  - 本地架設
  1. LINE Developers創立官方帳號，利用message API取得 CHANNEL SECRET 與 CHANNEL ACCESS TOKEN。
  2. 依據顯卡選擇適合的 DeepSeek model：DeepSeek-R1-Distill-Qwen-7B。
  3. 運行後端Cloudflare、Ngrok。
  4. 成本是顯卡，之後運行不用花錢。

  - 使用api
  1.  LINE Developers創立官方帳號，利用message API取得 CHANNEL SECRET 與 CHANNEL ACCESS TOKEN。
  2.  DeepSeek公開平台拿到Authtoken。
  3.  運行後端。
  4.  不需要高階顯卡，成本只有所使用的token。
     
Tech Stack：
  - python 3.11.11
  - anaconda
  - torch2.6 + cu126 (GPU rtx 4070)
  - FastAPI
  - LineMessageAPI

Tools Used：
  - ChatGPT
  - HugginFace
  - Cloudflare
  - ngrok
  
Optional：
  - 下載模型的時候，可以去huggingface尋找模型正確的名稱才能下載，要注意GPU、與RAM的大小選擇合適的模型。
  - Cloudflare、Ngrok卡巴斯基會報告有漏洞可鑽，測試完就關閉不用擔心。
  - 本地架設模型測試LINE回復需1分鐘，自己還未解決耗時過長的問題。
  - 使用DeepSeekAPI，每百萬token 25元，可以直接買兩美金，再縮短模型使用的token來控制成本。
  
References：
  - https://huggingface.co/
