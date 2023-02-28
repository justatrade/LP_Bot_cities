import os
from random import choice


def read_cities(user_id, bot):

    def read_file(file_name) -> list:
        cities_list = []
        try:
            with open(file_name, 'r', newline='\r\n', encoding='utf-8') as f:
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    cities_list.append(line)
                return cities_list
        except (FileNotFoundError, IOError) as e:
            print(e)
            bot.send_message(user_id, 'Something goes wrong, try later '
                                      'or contact support, please')

    user_list = []
    files = ['cities.csv']
    if str(user_id) in os.listdir('./users'):
        files.append(f'./users/{user_id}')
        user_list = read_file(files[1])
    common_cities_list = read_file(files[0])
    return common_cities_list, user_list


def available_letter(word: str) -> str:
    for i in word[::-1].lower():
        if i not in ('ь', 'ы', 'ъ', 'ё'):
            return i


def compare_cities(all_cities, user_named, city, user_id, bot) -> str:  # Compare user's city with
    # available and replying with a city, if possible
    if city == '':  # The only way of a blank city - is the beginning of a game
        bot_city = choice(all_cities)
        save_already_named(user_id, bot_city, bot)
        return bot_city
    else:
        if city.title() in all_cities and city not in user_named:
            result_set = set(all_cities)
            result_set.symmetric_difference_update(set(user_named))
            result_set.symmetric_difference_update(([city]))
            for each in result_set:
                if each[0].lower() == available_letter(city):
                    bot_city = each
                    save_already_named(user_id, bot_city, bot)
                    save_already_named(user_id, city, bot)  # add to user's named
                    return bot_city  # If we found corresponding city
            return '1'  # If not - user wins
        return bot.get_state(user_id)


def save_already_named(user_id, bot_city, bot):  # saving city that is already used for this user
    try:
        with open(f'./users/{user_id}', 'a', newline='', encoding='utf-8') as f:
            f.writelines(f'{bot_city.title()}\r\n')
    except (FileNotFoundError, IOError) as e:
        print(e)
        bot.send_message(user_id, 'Critical error. '
                                  'Please, start the game again')


def play_cities(user_id, city, bot) -> str:  # Choosing available cities
    all_cities, user_named = read_cities(user_id, bot)
    bot_city = compare_cities(all_cities, user_named, city, user_id, bot)
    return bot_city
