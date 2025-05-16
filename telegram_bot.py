from telegram.ext import Application, MessageHandler, filters
import requests 
from bs4 import BeautifulSoup

def get_dividiend(code):
    url = "https://finance.naver.com/item/main.nhn?code=" + code
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, "html5lib")
    tags = soup.select("#_dvr")
    if tags:
        dividend = tags[0].text
        return dividend
    return "정보를 찾을 수 없습니다."

# message handler
async def echo(update, context):
    user_id = update.effective_chat.id
    user_text = update.message.text
    dividend = get_dividiend(user_text)
    text = f"배당수익률: {dividend}"
    await context.bot.send_message(chat_id=user_id, text=text)

def main():
    # token
    with open("./token.txt") as f:
        lines = f.readlines()
        token = lines[0].strip()
    
    # 애플리케이션 빌더 사용
    application = Application.builder().token(token).build()
    
    # 메시지 핸들러 등록
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # 봇 실행
    application.run_polling()

if __name__ == "__main__":
    main()