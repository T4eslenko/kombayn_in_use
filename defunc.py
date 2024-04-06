from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sync import TelegramClient
import os
import time
import openpyxl
from telethon.tl.types import PeerChat, PeerChannel
 
def inviting(client, channel, users):
    client(InviteToChannelRequest(
        channel=channel,
        users=[users]
    ))

# Новая функция
def parsing_xlsx(client, index: int, id: bool, name: bool, file_name: str = 'users.xlsx'):
    all_participants = client.get_participants(index)

    # Создание нового документа Excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    
    # Запись заголовков столбцов
    headers = ['ID', 'Name', 'Username', 'First Name', 'Last Name', 'Participant Type']
    for col, header in enumerate(headers, start=1):
        sheet.cell(row=1, column=col, value=header)
    
    # Переменная для отслеживания строки
    row_num = 2
    
    # Процесс обработки участников чата в файл Excel
    for user in all_participants:
        # Если параметр id равен True, записываем ID пользователя без проверки
        if id:
            sheet.cell(row=row_num, column=1, value=user.id)
        
        # Если параметр name равен True и у пользователя есть имя, записываем его
        if name:
            # Проверка наличия атрибута username у объекта user
            if hasattr(user, 'username'):
                sheet.cell(row=row_num, column=2, value=user.username)
            # Проверка наличия атрибута first_name у объекта user
            if hasattr(user, 'first_name'):
                sheet.cell(row=row_num, column=3, value=user.first_name)
            # Проверка наличия атрибута last_name у объекта user
            if hasattr(user, 'last_name'):
                sheet.cell(row=row_num, column=4, value=user.last_name)
            # Проверка наличия атрибута username у объекта user
            if hasattr(user, 'username'):
                sheet.cell(row=row_num, column=5, value=user.username)
            # Проверка наличия атрибута participant.type у объекта user
            if hasattr(user, 'participant') and hasattr(user.participant, 'type'):
                sheet.cell(row=row_num, column=6, value=user.participant.type)
        
        # Увеличиваем номер строки для следующего пользователя
        row_num += 1
    
    # Сохранение документа Excel с указанным названием файла
    wb.save(file_name)
# Получаем ИД и Names в текстовый файл оригинал
def parsing(client, index: int, id: bool, name: bool):
    all_participants = []
    all_participants = client.get_participants(index)
    if name:
        with open('usernames.txt', 'r+') as f:
            usernames = f.readlines()
            for user in all_participants:
                if user.username:
                    if ('Bot' not in user.username) and ('bot' not in user.username):
                        if (('@' + user.username + '\n') not in usernames):
                            f.write('@' + user.username + '\n')
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
    if id:
        with open('userids.txt', 'r+') as f:
            userids = f.readlines()
            for user in all_participants:
                if (str(user.id) + '\n') not in userids:
                    f.write(str(user.id) + '\n')


def config():
    while True:
        os.system('cls||clear')

        with open('options.txt', 'r+') as f:
            if not f.readlines():
                f.write("NONEID\n"
                        "NONEHASH\n"
                        "True\n"
                        "True\n")
                continue
                
        options = getoptions()
        sessions = []
        for file in os.listdir('.'):
            if file.endswith('.session'):
                sessions.append(file)

        prompt_message = (
            f"1 - Обновить api_id [{options[0].rstrip()}]\n"
            f"2 - Обновить api_hash [{options[1].rstrip()}]\n"
            f"3 - Парсить user-id [{options[2].rstrip()}]\n"
            f"4 - Парсить user-name [{options[3].rstrip()}]\n"
            f"5 - Добавить аккаунт юзербота[{len(sessions)}]\n"
            "6 - Сбросить настройки\n"
            "e - Выход\n"
            "Ввод: "
        )

        key = str(input(prompt_message))

        if key == '1':
            os.system('cls||clear')
            options[0] = str(input("Введите API_ID: ")) + "\n"

        elif key == '2':
            os.system('cls||clear')
            options[1] = str(input("Введите API_HASH: ")) + "\n"

        elif key == '3':
            if options[2] == 'True\n':
                options[2] = 'False\n'
            else:
                options[2] = 'True\n'

        elif key == '4':
            if options[3] == 'True\n':
                options[3] = 'False\n'
            else:
                options[3] = 'True\n'
        
        elif key == '5':
            os.system('cls||clear')
            if options[0] == "NONEID\n" or options[1] == "NONEHASH":
                print("Проверьте api_id и api_hash")
                time.sleep(2)
                continue

            print("Аккаунты:\n")
            for i in sessions:
                print(i)

            phone = str(input("Введите номер телефона аккаунта: "))
            client = TelegramClient(phone, int(options[0].replace('\n', '')), 
                                    options[1].replace('\n', '')).start(phone)
            
        elif key == '6':
            os.system('cls||clear')
            answer = input("Вы уверены?\nAPI_ID и API_HASH будут удалены\n"
                           "1 - Удалить\n2 - Назад\n"
                           "Ввод: ")
            if answer == '1':    
                options.clear()
                print("Настройки очищены.")
                time.sleep(2)
            else:
                continue

        elif key == 'e':
            os.system('cls||clear')
            break

        with open('options.txt', 'w') as f:
            f.writelines(options)


def getoptions():
    with open('options.txt', 'r') as f:
        options = f.readlines()
    return options
