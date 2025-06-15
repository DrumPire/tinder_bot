from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

TOKEN = '7512240165:AAFNxz62TMDXdn9_Ggj9c0pzQ-IwxSG_RF8'

# тут будемо писати наш код :)

async def start(update, context):

  # await send_photo(update, context, "avatar_main")
  # await send_text(update, context, "Hello User")
  msg = load_message('main')
  await send_photo(update, context, 'avatar_main')
  await send_text(update, context, msg)


async def hello(update, context):
  # await send_text(update, context, "Hello" + update.message.text)
  await send_text_buttons(update, context, "Hello" + ' ' + update.message.from_user.username, {
    'start': 'START',
    'stop': 'STOP' 
  })

async def buttons_nandler(update, context):

  query = update.callback_query.data
  if query == 'start':
    await send_text(update, context, 'Started')
  elif query == 'stop':
    await send_text(update, context, 'Stoped')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(buttons_nandler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
