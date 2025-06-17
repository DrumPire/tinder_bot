from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

TOKEN = '7512240165:AAFNxz62TMDXdn9_Ggj9c0pzQ-IwxSG_RF8'

# тут будемо писати наш код :)

async def start(update, context):
  await send_photo(update, context, 'main')
  msg = load_message('main')
  await send_text(update, context, msg)
  await show_main_menu(update, context, {
    'start':  'головне меню бота',
    'profile':  'генерація Tinder-профілю 😎',
    'opener':  'повідомлення для знайомства 🥰',
    'message':  'листування від вашого імені 😈',
    'date':  'листування із зірками 🔥',
    'gpt':  'поставити запитання чату GPT 🧠'
  })

async def gpt(update, context):
  dialog.mode = 'gpt'
  await send_photo(update, context, 'gpt')
  msg = load_message('gpt')
  await send_text(update, context, msg)

async def gpt_dialog(update, context):
  text = update.message.text
  prompt = load_prompt('gpt')
  answer = await chatgpt.send_question(prompt, text) 
  await send_text(update, context, answer)

async def hello(update, context):
  if dialog.mode == 'gpt':
    await gpt_dialog(update, context)

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token='gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T')



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
# app.add_handler(CallbackQueryHandler(buttons_nandler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
