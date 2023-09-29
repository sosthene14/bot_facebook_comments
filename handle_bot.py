import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from check_telegram_user_Id import check_telegram_user_id
from handle_comments import handle_comments

dotenv_path = './.env'
load_dotenv(dotenv_path)
TELEGRAM_TOKEN = os.getenv("TOKEN_TELEGRAM")
# Étapes de la conversation
USERNAME, POST_ID, MESSAGE, START_OVER, STOPPING = range(5)

user_data = {}


def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if check_telegram_user_id(user_id):
        print("Ouvert")
        update.message.reply_text("Bienvenue ! Veuillez saisir l'id de la publication\nEntrez stop pour quitter")
        return USERNAME
    else:
        update.message.reply_text("Accès refusé")
        return START_OVER


def check_post_id(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()
    if user_input.lower() == "stop":
        update.message.reply_text("Vous avez arreté la conversation /start pour reprendre ")
        return START_OVER
    user_data['post_id'] = user_input
    update.message.reply_text("Veuillez maintenant saisir le message ")
    print(f"Post ID: {user_data['post_id']}")
    return MESSAGE


def get_message(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.strip()
    if user_input.lower() == "stop":
        update.message.reply_text("Vous avez arreté la conversation /start pour reprendre ")
        return START_OVER
    user_data['message'] = user_input
    update.message.reply_text("Le processus a commencé en arrière plan, nous vous notifierons")
    responses = handle_comments(user_data["post_id"], user_data["message"])

    for response in responses:
        update.message.reply_text(response)
    update.message.reply_text("Veuillez saisir /start pour m'utiliser à nouveau")
    return START_OVER


def stop(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Vous avez arrêté la conversation. Vous pouvez à nouveau saisir /start pour "
                              "redémarrer.")
    return START_OVER


def start_over(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Vous avez redémarré la conversation.\n Veuillez saisir l'id de la publication.")
    return USERNAME


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, check_post_id)],
            POST_ID: [MessageHandler(Filters.text & ~Filters.command, get_message)],
            MESSAGE: [MessageHandler(Filters.text & ~Filters.command, get_message)],
            START_OVER: [CommandHandler('start', start)],
            STOPPING: [CommandHandler('stop', stop)]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
