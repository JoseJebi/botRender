#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from openai import OpenAI

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

token = "8085222960:AAH6TDXo5-vYTniLrrbbh_VDIKAHG9fdL_w"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

lista_nombre = {'diana', 'alejandro', 'daniel'}
# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def contratar(update:Update, context:CallbackContext) -> None:
    keyboard = [["Moto","Coche"]]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True,one_time_keyboard=True)
    await update.message.reply_text("Elige tipo de vehículo:",reply_markup=reply_markup)

async def opciones(update:Update, context:CallbackContext) -> None:
    text = update.message.text
    keyboard = ""
    print(text)
    if text == "Moto":
        keyboard = [["> 50cc","<50cc"]]

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    texto=update.message.text

    if texto.lower() in lista_nombre:
        await update.message.reply_text("Estás en la clase")    #update.message.text
    else:
        await update.message.reply_text("No te reconozco")

    logger.info(texto)

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /bye is issued."""
    await update.message.reply_text("Hasta la proximaaaaaa")

async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the message "ia" is issued."""
    await update.message.reply_text("ia")

async def deepseek(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    texto=update.message.text

    logger.info(update.effective_user.name + ": " + texto)
    logger.info("Esperando a Deepseek...")

    completion = client.chat.completions.create(

        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    respuesta = completion.choices[0].message.content

    await update.message.reply_text(respuesta)

    logger.info("Deepseek: " + respuesta)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("bye", bye))
    application.add_handler(CommandHandler("contratar", contratar))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, opciones))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()