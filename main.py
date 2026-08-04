import os
import threading
from flask import Flask
import google.generativeai as genai
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# --- [ 1. سيرفر Flask المدمج لفتح Port على Render ] ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot is Running Successfully!'


def run():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = threading.Thread(target=run)
  t.daemon = True
  t.start()


keep_alive()

# --- [ 2. إعدادات البوت والذكاء الاصطناعي ] ---

BOT_TOKEN = os.getenv(
    'BOT_TOKEN', '8835723305:AAE0_aNTcjtfIM3ItDHx9y7MCaYzvPCvcYo'
)
SIM_API_KEY = os.getenv('SIM_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

bot = telebot.TeleBot(BOT_TOKEN)

# إعداد نموذج الذكاء الاصطناعي (Gemini)
ai_model = None
if GEMINI_API_KEY:
  try:
    genai.configure(api_key=GEMINI_API_KEY)
    system_instruction = (
        'أنت مساعد ذكي ولطيف متكامل داخل بوت تفعيل الأرقام. '
        'تحدث مع المستخدمين بأسلوب محترم وودود. '
        'مطور هذا البوت هو المبرمج والمطور: أحمد علي الصالحي (الملقب بـ كرستا'
        ' نتار LR1999081). '
        'يدعم البوت الشحن عبر حاسب/جيب الكريمي ومحفظة جوالي وفودافون كاش'
        ' والعملات الرقمية. '
        'إذا سألك أحد عن المطور أو أرقام الشحن، أجبهم بالمعلومات المتوفرة'
        ' بوضوح.'
    )
    ai_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction,
    )
    print('✅ تم تفعيل نموذج الذكاء الاصطناعي بنجاح!')
  except Exception as e:
    print(f'❌ خطأ في إعداد الذكاء الاصطناعي: {e}')


# --- [ 3. لوحات الأزرار الشفافة ] ---


def main_keyboard():
  markup = InlineKeyboardMarkup()
  markup.row_width = 1

  btn_buy = InlineKeyboardButton(
      '📱 طلب رقم واتساب (تلقائي)', callback_data='buy_whatsapp'
  )
  btn_prices = InlineKeyboardButton(
      '💎 أسعار النقاط والأرقام', callback_data='show_prices'
  )
  btn_recharge = InlineKeyboardButton(
      '💳 طرق الشحن (الكريمي / جوالي)', callback_data='recharge_methods'
  )
  btn_balance = InlineKeyboardButton(
      '💰 حسابي والرصيد', callback_data='my_balance'
  )
  btn_dev = InlineKeyboardButton(
      '👨‍💻 مطور البوت (كرستا نتار)', callback_data='dev_info'
  )
  btn_support = InlineKeyboardButton(
      '💬 التواصل مع الدعم', url='https://t.me/zzszz'
  )

  markup.add(
      btn_buy, btn_prices, btn_recharge, btn_balance, btn_dev, btn_support
  )
  return markup


def recharge_keyboard():
  markup = InlineKeyboardMarkup()
  markup.row_width = 1

  btn_kuraimi = InlineKeyboardButton(
      '🏦 بنك الكريمي (حاسب / جيب)', callback_data='pay_kuraimi'
  )
  btn_jawali = InlineKeyboardButton(
      '📱 محفظة جوالي (Jawali)', callback_data='pay_jawali'
  )
  btn_crypto = InlineKeyboardButton(
      '🌐 عملات رقمية (USDT / TON)', callback_data='pay_crypto'
  )
  btn_confirm = InlineKeyboardButton(
      '📩 إرسال إشعار التحويل للدعم', url='https://t.me/zzszz'
  )
  btn_back = InlineKeyboardButton(
      '🔙 رجوع للقائمة الرئيسية', callback_data='main_menu'
  )

  markup.add(btn_kuraimi, btn_jawali, btn_crypto, btn_confirm, btn_back)
  return markup


def back_keyboard():
  markup = InlineKeyboardMarkup()
  btn_back = InlineKeyboardButton(
      '🔙 رجوع لشاشات الشحن', callback_data='recharge_methods'
  )
  markup.add(btn_back)
  return markup


# --- [ 4. معالجة الأوامر والأزرار ] ---


@bot.message_handler(commands=['start'])
def send_welcome(message):
  welcome_text = (
      f'👋 **أهلاً بك يا {message.from_user.first_name} في بوت الأرقام'
      ' المطور!**\n\n'
      '👑 **المطور:** أحمد علي الصالحي *(كرستا نتار LR1999081)*\n\n'
      '✨ **مميزات البوت:**\n'
      '• تفعيل أرقام واتساب فورية ⚡\n'
      '• شحن عبر الكريمي (حاسب/جيب)، جوالي، والعملات الرقمية 💳\n'
      '• ذكاء اصطناعي للرد على استفساراتك المباشرة 🤖\n\n'
      '👇 **اختر الخدمة المطلوبة من القائمة أو تحدث مع الذكاء الاصطناعي:**'
  )
  bot.send_message(
      message.chat.id,
      welcome_text,
      parse_mode='Markdown',
      reply_markup=main_keyboard(),
  )


@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
  # عرض الأسعار
  if call.data == 'show_prices':
    prices_text = (
        '💸 | **أسعار النقاط والأرقام** 🌐\n\n'
        '💎 **10,000 نقطة** = $1 (أو ما يعادلها بالريال)\n'
        '💎 **20,000 نقطة** = $2\n'
        '💎 **50,000 نقطة** = $5\n'
        '💎 **100,000 نقطة** = $10\n\n'
        '----------------------------\n'
        '• **طرق الشحن المتوفرة:**\n'
        '🏦 بنك الكريمي (حاسب / جيب)\n'
        '📱 محفظة جوالي\n'
        '🌐 العملات الرقمية (USDT $ TON)\n'
        '----------------------------\n'
        '🎁 **هدية نقاط إضافية عند الشحن الفوري!** 🔥'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=prices_text,
        parse_mode='Markdown',
        reply_markup=recharge_keyboard(),
    )

  # قائمة طرق الشحن
  elif call.data == 'recharge_methods':
    recharge_text = (
        '💳 **اختر طريقة الشحن التي تناسبك:**\n\n'
        'قم باختيار إحدى المحافظ أدناه لتحصل على رقم الحساب وإرشادات التحويل.'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=recharge_text,
        parse_mode='Markdown',
        reply_markup=recharge_keyboard(),
    )

  # تفاصيل حساب الكريمي
  elif call.data == 'pay_kuraimi':
    kuraimi_text = (
        '🏦 **الشحن عبر بنك الكريمي (حاسب / جيب):**\n\n'
        '• **اسم الحساب:** أحمد علي الصالحي (كرستا نتار)\n'
        '• **رقم الحساب المميز / المميز:** `اكتب_رقم_حسابك_هنا`\n\n'
        '📌 **خطوات الشحن:**\n'
        '1. قم بتحويل المبلغ المطلوب لحساب الكريمي.\n'
        '2. التقط صورة لإشعار التحويل أو انسخ رقم السند.\n'
        '3. اضغط على زر **إرسال إشعار التحويل للدعم** بالأسفل وسيتم إضافة'
        ' النقاط لحسابك فوراً.'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=kuraimi_text,
        parse_mode='Markdown',
        reply_markup=back_keyboard(),
    )

  # تفاصيل محفظة جوالي
  elif call.data == 'pay_jawali':
    jawali_text = (
        '📱 **الشحن عبر محفظة جوالي (Jawali):**\n\n'
        '• **اسم المحفظة:** أحمد علي الصالحي\n'
        '• **رقم المحفظة / الهاتف:** `اكتب_رقم_جوالك_هنا`\n\n'
        '📌 **خطوات الشحن:**\n'
        '1. قم بتحويل المبلغ إلى رقم المحفظة أعلاه.\n'
        '2. أرسل صورة السند أو رقم العملية للدعم الفني لتفعيل النقاط.'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=jawali_text,
        parse_mode='Markdown',
        reply_markup=back_keyboard(),
    )

  # الشحن بالعملات الرقمية
  elif call.data == 'pay_crypto':
    crypto_text = (
        '🌐 **الشحن عبر العملات الرقمية (USDT / TON):**\n\n'
        '• **شبكة TRC20 (USDT):** `اكتب_عنوان_محفظتك_هنا`\n'
        '• **شبكة TON:** `اكتب_عنوان_محفظتك_هنا`\n\n'
        'أرسل صورة الإشعار للدعم بعد إتمام العملية.'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=crypto_text,
        parse_mode='Markdown',
        reply_markup=back_keyboard(),
    )

  # الرجوع للقائمة الرئيسية
  elif call.data == 'main_menu':
    welcome_text = (
        '👋 **الرجوع للقائمة الرئيسية**\n\n'
        '👇 **اختر الخدمة التي تريدها من الأسفل:**'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=welcome_text,
        parse_mode='Markdown',
        reply_markup=main_keyboard(),
    )

  # باقي الأزرار
  elif call.data == 'my_balance':
    bot.answer_callback_query(
        call.id, '💰 رصيدك الحالي: 0 $', show_alert=True
    )

  elif call.data == 'dev_info':
    dev_text = (
        '👨‍💻 **معلومات مطور البوت:**\n\n'
        '• **الاسم:** أحمد علي الصالحي\n'
        '• **اللقب:** كرستا نتار (LR1999081)\n'
        '• **الدعم:** @zzszz'
    )
    bot.answer_callback_query(call.id, dev_text, show_alert=True)

  elif call.data == 'buy_whatsapp':
    if not SIM_API_KEY:
      bot.answer_callback_query(
          call.id,
          '⚠️ لم يتم ربط مفتاح API لموقع 5sim بعد!',
          show_alert=True,
      )
      return
    bot.answer_callback_query(call.id, '⏳ جاري جلب الرقم...')


# --- [ 5. الذكاء الاصطناعي للرد الشات ] ---
@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
  if not ai_model:
    bot.reply_to(
        message,
        '🤖 مرحباً بك! يرجى اختيار أحد الخيارات من القائمة الرئيسية.',
    )
    return

  bot.send_chat_action(message.chat.id, 'typing')
  try:
    response = ai_model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    print(f'AI Error: {e}')
    bot.reply_to(message, 'حدث خطأ بسيط في معالجة الرد، يرجى إعادة المحاولة.')


print('🚀 البوت المطور جاهز مع خدمات الدفع والذكاء الاصطناعي...')
bot.infinity_polling()
