import telebot
import functions as f
import os


def all_handlers(bot: telebot.TeleBot):

    @bot.message_handler(commands=['cities', 'города'])
    def game_of_cities(msg):  # Orchestrator of Cities game
        '''
            Главная управляющая функция
        :param msg: Получаем объект сообщения для получения id чата и текста пользователя
        :return:
        '''
        if bot.get_state(msg.chat.id):  # Check, whether we are playing already
            if f.available_letter(
                    bot.get_state(msg.chat.id)) == msg.text.lower()[0]:
                response = f.play_cities(msg.chat.id, msg.text, bot)
            else:  # If user's first letter of a city is wrong
                response = bot.get_state(msg.chat.id)  # keep state with current city
        else:  # The beginning of a game
            response = f.play_cities(msg.chat.id, city='', bot=bot)
        if response == '1':
            stop_game_of_cities(msg)
            user_message = 'Congratulations! You won the game!'
        elif response == bot.get_state(msg.chat.id):
            named_cities(msg)
            user_message = 'Wrong city. The last was: ' + response
        else:
            bot.set_state(msg.chat.id, response)  # Setting user state, based on a name of a city
            next_letter = f.available_letter(response)  # Choosing available letter for the next
            # turn
            user_message = response + f' your move is on {next_letter}'
        bot.send_message(msg.chat.id, user_message)

    @bot.message_handler(commands=['cities_stop', 'города_стоп'])
    def stop_game_of_cities(msg):
        """
        Вызывается для окончания игры. Удаляет файл пользователя с использованными городами.
        :param msg:
        :return:
        """
        try:
            bot.delete_state(msg.chat.id)
            os.remove(f'./users/{msg.chat.id}')
            bot.send_message(msg.chat.id, 'The game is ended)')
        except (FileNotFoundError, FileExistsError, OSError) as e:
            print(e)
            bot.send_message(msg.chat.id, 'Something goes wrong, try later'
                                          ' or contact support, please')

    @bot.message_handler(commands=['/named_cities'])
    def named_cities(msg):
        """
        Функция для получения списка уже использованных в текущей игре городов
        :param msg:
        :return:
        """
        _, my_list = f.read_cities(msg.chat.id, bot)
        bot.send_message(msg.chat.id, ', '.join(my_list))

    @bot.message_handler(commands=['start'])
    def info_message(msg):
        """
        Функция для вывода справки
        :param msg:
        :return:
        """
        bot.send_message(msg.chat.id,
                         f'Available commands are: '
                         f'\n/wordcount /wc counting words put '
                         f'after the command'
                         f'\n/next_full_moon /next_moon /moon'
                         f' - put a date dd-mm-yyyy after the comand to'
                         f' see the next full moon date'
                         f'\n/cities /города - the cities game'
                         f'\n/named_cities - the list of cities which have'
                         f' been already named'
                         f'\n/cities_stop /города_стоп - stop playing')

    @bot.message_handler(content_types=['text'])
    def main_reply(msg):
        """
        Функция для обработки текстовых сообщений. Если файл пользователя присутствует, то любой
        текст воспринимается как попытка назвать слово. В противном случае, вызывается функция
        отображения справки
        :param msg:
        :return:
        """
        if os.path.isfile(f'./users/{msg.chat.id}'):
            game_of_cities(msg)
        else:
            info_message(msg)
