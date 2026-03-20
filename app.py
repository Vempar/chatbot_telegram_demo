import os
from datetime import date
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telegram_bot_calendar.base import max_date, min_date
import components.token as token   
import components.globals as globals

telegram_token=os.getenv("TOKEN")
#telegram_token="PUT YOUR PERSONAL TOKEN HERE"


#menu inicio con las opciones de turno


async def start_command(update,context):
    # Definimos el teclado de respuesta
    markup = ReplyKeyboardMarkup(globals.reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    #configuramos el comando start para escribir una respuesta
    await update.message.reply_text(
        globals.texto_start,
        reply_markup=markup
    )

async def help_command(update,context):
    #configuramos el comando help para escribir una respuesta
    
    await update.message.reply_text(globals.help_text)



#detecta fotos enviadas
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Gracias por la foto!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    markup = ReplyKeyboardMarkup(globals.reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    if text == "📄 Download_demo" or text.lower() == "download demo":
        await update.message.reply_document(document="./assets/demo.txt")
        await update.message.reply_text('¡Aquí tienes tu archivo!')
        await update.message.reply_text("¿En qué más puedo ayudarte?", reply_markup=markup)
    elif text == "premio" or text.lower() == "premio":
        await update.message.reply_text(globals.premio) 
        await update.message.reply_text("¿En qué más puedo ayudarte?", reply_markup=markup)
    elif text == "❓ Help":
        await help_command(update, context)
    else:
        await update.message.reply_text("Lo siento, todavía no sé hacer eso. ", reply_markup=markup)
#configuramos el logging para que muestre los errores
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.WARNING)
logger = logging.getLogger(__name__)
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    bot = Application.builder().token(telegram_token).build()
    #funcion que responde al usuario con echo
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    bot.add_handler(CommandHandler("start", start_command))
    bot.add_handler(CommandHandler("help", help_command))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_command))
    bot.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
