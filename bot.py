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

async def date(update, context):
  dialog.mode = 'date'
  msg = load_message('date')
  await send_photo(update, context, 'date')
  await send_text(update, context, msg)
  await send_text_buttons(update, context, msg, {
    'date_grande': 'Аріана Гранде',
    'date_robbie': 'Марго Роббі',
    'date_zendaya': 'Зендея',
    'date_gosling': 'Райан Гослінг',
    'date_hardy': 'Том Харді',
  })

async def date_button(update, context):
  query = update.callback_query.data
  await update.callback_query.answer()
  await send_photo(update, context, query)
  await send_text(update, context, 'Гарний вибір. \uD83D\uDE05 Ваша задача запросити хлопця/дівчину на побачення за 5 повідомлинь ❤️')
  prompt = load_prompt(query)
  chatgpt.set_prompt(prompt)

async def date_dialog(update, context):
  text = update.message.text
  my_message = await send_text(update, context, 'prints...')
  answer = await chatgpt.add_message(text)
  await my_message.edit_text(answer)

async def message(update, context):
  dialog.mode = 'message'
  msg = load_message('message')
  await send_photo(update, context, 'message')
  await send_text_buttons(update, context, msg, {
    'message_next': 'send message',
    'message_date': 'invite on a date',
  })
  dialog.list.clear()

async def message_dialog(update, context):
  text = update.message.text
  dialog.list.append(text)

async def message_button(update, context):
  query = update.callback_query.data
  await update.callback_query.answer()

  prompt = load_prompt(query)
  user_chat_history = '\n\n'.join(dialog.list) 
  my_message = await send_text(update, context, "I'm thinking about options...'")
  answer = await chatgpt.send_question(prompt, user_chat_history)
  await my_message.edit_text(answer)

async def hello(update, context):
  if dialog.mode == 'gpt':
    await gpt_dialog(update, context)
  elif dialog.mode == 'date':
    await date_dialog(update, context)
  elif dialog.mode == 'message':
    await date_dialog(update, context)

dialog = Dialog()
dialog.mode = None
dialog.list = []

chatgpt = ChatGptService(token='gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T')



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern='^date_.*'))
app.add_handler(CallbackQueryHandler(message_button, pattern='^message_.*'))
app.run_polling()
