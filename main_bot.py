
from telegram.ext import Updater, CommandHandler

# Обработчик команды /start
def start(update, context):
    update.message.reply_text('Привет! Я бот. Как могу помочь?')

def main():
    # Инициализация Updater с токеном вашего бота
    updater = Updater("AAFsjUt2-j0KNtcb-90pTeehCg33H7-HsQc", update_queue=True)

    # Получение диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчика для команды /start
    dp.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()

    # Ожидание остановки бота (Ctrl + C)
    updater.idle()

if __name__ == '__main__':
    main()
