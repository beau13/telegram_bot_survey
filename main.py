import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Запускаем опрос
poll_question = "Какой ваш любимый язык программирования?"
poll_options = ["Python", "Java", "C++", "JavaScript"]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте /poll, чтобы начать опрос.')

def poll(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in poll_options]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(poll_question, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Вы выбрали: {query.data}")

def main() -> None:
    # Вставьте свой токен here
    updater = Updater("7853917364:AAHsZVeu18uMrMdkG4-mJ-mMdk1WXQlYQnE")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("poll", poll))

    # Обработчик нажатий кнопок
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения
    updater.idle()

if __name__ == '__main__':
    main()
