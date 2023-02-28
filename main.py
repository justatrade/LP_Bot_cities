import telebot
import config
import handlers as h

# По боту я предлагаю пока сделать следующее
# 1. Вынести в отдельный репозиторий, так мне кажется будт легче
# 2. Оставить в боте только функционал по городам
# 3. Не надо се упаковывать в функцию main
# 4. Разнести хэндлеры и логику по разным файлам
# 5. Для хэндлеров написать докстринги, что этот хэндлер делает


def main():
    bot = telebot.TeleBot(config.BOT_TOKEN)
    h.all_handlers(bot)
    try:
        bot.infinity_polling(allowed_updates=['chat_member',
                                              'my_chat_member',
                                              'message'])
    except KeyboardInterrupt:
        bot.stop_polling()


if __name__ == '__main__':
    main()