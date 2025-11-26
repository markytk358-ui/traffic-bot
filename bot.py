import requests
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8565634331:AAFOyrI_bZZliFGw5m_vQat0bLIC6qeQhUg"

class TrafficBot:
    def __init__(self):
        self.proxies = []
    
    def load_proxies(self):
        try:
            url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                self.proxies = [p.strip() for p in response.text.split('\n') if p.strip()][:20]
                print(f"تم تحميل {len(self.proxies)} بروكسي")
        except:
            self.proxies = []
    
    def visit_url(self, url):
        success = 0
        for i in range(5):
            try:
                proxy = random.choice(self.proxies) if self.proxies else None
                if proxy:
                    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                    response = requests.get(url, proxies=proxies, timeout=5)
                else:
                    response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    success += 1
                time.sleep(1)
            except:
                pass
        
        return {'success': success, 'total': 5}

bot = TrafficBot()
bot.load_proxies()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎊 أهلاً! أرسل رابط وسأزوره 5 مرات!")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    msg = await update.message.reply_text("🔄 جاري الزيارة...")
    result = bot.visit_url(url)
    
    await msg.edit_text(f"✅ النتائج: {result['success']}/{result['total']} نجحت")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

print("🤖 البوت يعمل!")
app.run_polling()
