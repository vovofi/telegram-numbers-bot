import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الخاص بك
BOT_TOKEN = os.getenv("BOT_TOKEN", "8835723305:AAE0_aNTcjtfIM3ItDHx9y7MCaYzvPCvcYo")
SIM_API_KEY = os.getenv("SIM_API_KEY", "")

bot = telebot.TeleBot(BOT_TOKEN)

# قائمة الأزرار الرئيسية
def main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    
    btn_buy = InlineKeyboardButton("📱 طلب رقم واتساب (تلقائي)", callback_data="buy_whatsapp")
    btn_prices = InlineKeyboardButton("💎 أسعار النقاط والأرقام", callback_data="show_prices")
    btn_balance = InlineKeyboardButton("💰 حسابي والرصيد", callback_data="my_balance")
    btn_support = InlineKeyboardButton("👨‍💻 التواصل مع الدعم", url="https://t.me/zzszz")
    
    markup.add(btn_buy, btn_prices, btn_balance, btn_support)
    return markup

# القائمة الفرعية (أزرار عند الضغط على الأسعار)
def prices_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    
    btn_recharge = InlineKeyboardButton("⚡ شحن نقاط تلقائي وفوري", callback_data="recharge")
    btn_back = InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")
    
    markup.add(btn_recharge, btn_back)
    return markup

# أمر التشغيل الرئيسي /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"👋 **أهلاً بك يا {message.from_user.first_name} في بوت الأرقام المطور!**\n\n"
        "✨ **مميزات البوت:**\n"
        "• تفعيل أرقام واتساب وفوري ⚡\n"
        "• شحن رصيد تلقائي وسريع 💎\n"
        "• دعم فني متواجد لمساعدتك 👨‍💻\n\n"
        "👇 **اختر الخدمة المطلوبة من القائمة أدناه:**"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_keyboard())

# التحكم بالأزرار الشفافة
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    # زر عرض الأسعار
    if call.data == "show_prices":
        prices_text = (
            "💸 | **أسعار نقاط وأرقام البوت** 🌐\n\n"
            "💎 **10,000 نقطة** = $1\n"
            "💎 **20,000 نقطة** = $2\n"
            "💎 **50,000 نقطة** = $5\n"
            "💎 **100,000 نقطة** = $10\n\n"
            "----------------------------\n"
            "• **طرق الدفع المتوفرة:**\n"
            "فودافون كاش، زين كاش، كروت، والعملات الرقمية (USDT $ BTC $ TON)\n"
            "----------------------------\n"
            "🎁 **هدية نقاط إضافية عند الشحن الفوري!** 🔥"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=prices_text,
            parse_mode="Markdown",
            reply_markup=prices_keyboard()
        )

    # زر الرجوع للقائمة الرئيسية
    elif call.data == "main_menu":
        welcome_text = (
            f"👋 **الرجوع للقائمة الرئيسية**\n\n"
            "👇 **اختر الخدمة التي تريدها من الأسفل:**"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )

    # زر الرصيد
    elif call.data == "my_balance":
        bot.answer_callback_query(call.id, "💰 رصيدك الحالي: 0 $", show_alert=True)

    # زر طلب الرقم
    elif call.data == "buy_whatsapp":
        if not SIM_API_KEY:
            bot.answer_callback_query(call.id, "⚠️ لم يتم ربط مفتاح API لموقع 5sim بعد!", show_alert=True)
            return
        bot.answer_callback_query(call.id, "⏳ جاري جلب الرقم...")

    # زر الشحن
    elif call.data == "recharge":
        bot.answer_callback_query(call.id, "تواصل مع الدعم لشحن حسابك فوراً 🚀", show_alert=True)

print("🚀 البوت الاحترافي يعمل الآن بنجاح...")
bot.infinity_polling()

