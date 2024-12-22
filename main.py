import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)  # Исправлено на __name__

# Запускаем опрос
poll_question_1 = "Какой ваш любимый язык программирования?"
poll_options_1 = ["Python", "Java", "C++", "JavaScript"]

poll_question_2 = "Какой фреймворк для веб-разработки вам нравится?"
poll_options_2 = ["Django", "Flask", "React", "Angular"]

user_responses = {}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте /poll, чтобы начать опрос.')


def poll(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in poll_options_1]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(poll_question_1, reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Сохраняем ответ пользователя
    user_responses[query.from_user.id] = user_responses.get(query.from_user.id, {})

    if 'programming_language' in user_responses[query.from_user.id]:  # Если уже задан первый вопрос
        user_responses[query.from_user.id]['framework'] = query.data
        framework_button(update, context)  # Переход к обработке фреймворка
    else:  # Обработка первого вопроса
        user_responses[query.from_user.id]['programming_language'] = query.data
        keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in poll_options_2]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Вы выбрали: {query.data}. Теперь выберите фреймворк.", reply_markup=reply_markup)


def framework_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Сохраняем ответ о фреймворке
    user_responses[query.from_user.id]['framework'] = query.data
    # Формируем сообщение с результатами
    selected_language = user_responses[query.from_user.id]['programming_language']
    selected_framework = user_responses[query.from_user.id]['framework']

    query.edit_message_text(
        text=f"Вы выбрали язык: {selected_language}, фреймворк: {selected_framework}. Спасибо за участие в опросе!")


def main() -> None:
    # Вставьте свой токен сюда
    updater = Updater("7853917364:AAHsZVeu18uMrMdkG4-mJ-mMdk1WXQlYQnE")  # Замените на свой токен

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


if __name__ == '__main__':  # Исправлено на __name__ == '__main__'
    main()
