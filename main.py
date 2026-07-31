import os
import telebot
import requests

# التوكن الخاص ببوتك
BOT_TOKEN = os.getenv("BOT_TOKEN", "8835723305:AAE0_aNTcjtfIM3ItDHx9y7MCaYzvPCvcYo")
SIM_API_KEY = os.getenv("SIM_API_KEY", "")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"أهلاً بك يا {message.from_user.first_name} في بوت الأرقام الوهمية! 📱\n\n"
        "اختر الخدمة التي تريدها من القائمة أسفله:"
    )
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_buy = telebot.types.InlineKeyboardButton("طلب رقم واتساب 🟢", callback_data="buy_whatsapp")
    btn_balance = telebot.types.InlineKeyboardButton("حسابي والرصيد 💰", callback_data="my_balance")
    
    markup.add(btn_buy)
    markup.add(btn_balance)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "my_balance":
        bot.answer_callback_query(call.id, "رصيدك الحالي: 0 ريال يمني (تواصل مع الدعم للشحن)")
        
    elif call.data == "buy_whatsapp":
        if not SIM_API_KEY:
            bot.answer_callback_query(call.id, "⚠️ يرجى إضافة مفتاح API لموقع الأرقام أولاً.")
            bot.send_message(call.message.chat.id, "⚠️ لم يتم ربط موقع الأرقام بعد. يرجى تزويد البوت بمفتاح API من موقع 5sim.")
            return

        bot.answer_callback_query(call.id, "جاري طلب الرقم...")
        bot.send_message(call.message.chat.id, "⏳ جاري جلب الرقم من المزود، انتظر لحظة...")
        
        headers = {
            'Authorization': f'Bearer {SIM_API_KEY}',
            'Accept': 'application/json',
        }
        
        try:
            url = 'https://5sim.net/v1/user/buy/activation/russia/any/whatsapp'
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if response.status_code == 200:
                phone_number = data.get('phone', 'غير معروف')
                order_id = data.get('id', 'غير معروف')
                
                msg = (
                    f"✅ **تم تجهيز رقمك بنجاح!**\n\n"
                    f"📱 **الرقم:** `{phone_number}`\n"
                    f"🆔 **رقم الطلب:** `{order_id}`\n\n"
                    f"قم بنسخ الرقم وضعه في الواتساب، واطلب كود التفعيل."
                )
                bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
            else:
                bot.send_message(call.message.chat.id, "❌ خطأ: لا توجد أرقام متوفرة حالياً أو الرصيد غير كافٍ في موقع الأرقام.")
        except Exception:
            bot.send_message(call.message.chat.id, "❌ حدث خطأ أثناء الاتصال بسيرفر الأرقام.")

print("البوت يعمل الآن بنجاح على السيرفر...")
bot.infinity_polling()
