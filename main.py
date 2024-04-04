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
        
        # Остальной код

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
