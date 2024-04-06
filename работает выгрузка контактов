from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from defunc import *
import time
import random
import os
import openpyxl
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import GetContactsRequest
import asyncio  # Add this import statement at the beginning of your script

async def get_contacts(client):
    result = await client(GetContactsRequest(0))
    contacts = result.users

    # Создаем новый документ Excel
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Записываем заголовки столбцов
    headers = ['ID', 'Имя', 'Фамилия', 'Телефон']
    for col, header in enumerate(headers, start=1):
        sheet.cell(row=1, column=col, value=header)

    # Переменная для отслеживания строки
    row_num = 2

    # Процесс записи контактов в файл Excel
    for contact in contacts:
        # Если контакт имеет телефон, записываем его
        if hasattr(contact, 'phone'):
            sheet.cell(row=row_num, column=4, value=contact.phone)

        # Проверяем наличие атрибутов ID, имени и фамилии у контакта
        if hasattr(contact, 'id'):
            sheet.cell(row=row_num, column=1, value=contact.id)
        if hasattr(contact, 'first_name'):
            sheet.cell(row=row_num, column=2, value=contact.first_name)
        if hasattr(contact, 'last_name'):
            sheet.cell(row=row_num, column=3, value=contact.last_name)
        
        # Увеличиваем номер строки для следующего контакта
        row_num += 1

    # Сохраняем документ Excel
    wb.save('contacts.xlsx')

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
                            "3 - Парсинг в excel\n"
                            "4 - Инвайтинг\n"
                            "5 - Получить список контактов\n"  
                            "e - Выход\n"
                            "Ввод: "))
        

        if selection == '1':
            config()

        elif selection == '2':
            chats = []
            last_date = None    
            size_chats = 200
            groups = []         

            print("Выберите юзер-бота для парсинга.\n"
                "(Аккаунт который состоит в группах, которые нужно спарсить)\n")

            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            for i in range(len(sessions)):
                print(f"[{i}] -", sessions[i], '\n')
            i = int(input("Ввод: "))
            
            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash).start(sessions[i].replace('\n', ''))

            result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=size_chats,
                hash=0
            ))
            chats.extend(result.chats)

            for chat in chats:
                try:
                    if chat.megagroup is True:
                        groups.append(chat)         
                except:
                    continue

            i = 0
            print('Очистка базы юзеров: clear') 
            print('-----------------------------')
            for g in groups:
                print(str(i) + ' - ' + g.title)
                i+=1
            print(str(i + 1) + ' - ' + 'Спарсить всё')
            g_index = str(input())

            if g_index == 'clear':
                f = open('usernames.txt', 'w')
                f.close()
                f = open('userids.txt', 'w')
                f.close

            elif int(g_index) < i + 1:
                target_group = groups[int(g_index)]
                parsing(client, target_group, user_id, user_name)
                print('Спаршено.')
                time.sleep(2)

            elif int(g_index) == i + 1:
                for g_index in groups:
                    parsing(client, g_index, user_id, user_name)
                print('Спаршено.')
                time.sleep(2)

        elif selection == '3':
            chats = []
            last_date = None    
            size_chats = 200
            groups = []         

            print("Выберите юзер-бота для парсинга.\n"
                "(Аккаунт который состоит в группах, которые нужно спарсить)\n")

            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            for i in range(len(sessions)):
                print(f"[{i}] -", sessions[i], '\n')
            i = int(input("Ввод: "))
            
            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash).start(sessions[i].replace('\n', ''))

            result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=size_chats,
                hash=0
            ))
            chats.extend(result.chats)

            for chat in chats:
                try:
                    if chat.megagroup is True:
                        groups.append(chat)         
                except:
                    continue

            i = 0
            #print('Очистка базы юзеров: clear') 
            #print('-----------------------------')
            for g in groups:
                print(str(i) + ' - ' + g.title)
                i+=1
            #print(str(i + 1) + ' - ' + 'Спарсить всё')
            g_index = str(input())

            if g_index == 'clear':
                f = open('usernames.txt', 'w')
                f.close()
                f = open('userids.txt', 'w')
                f.close

            elif int(g_index) < i + 1:
                target_group = groups[int(g_index)]
                parsing_xlsx(client, target_group, user_id, user_name)
                print('Спаршено.')
                time.sleep(2)

            elif int(g_index) == i + 1:
                for g_index in groups:
                    parsing_xlsx(client, g_index, user_id, user_name)
                print('Спаршено.')
                time.sleep(2)

        elif selection == '4':
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

        elif selection == '5':
            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            print("Выберите юзер-бота для получения списка контактов:\n")
            for i, session in enumerate(sessions):
                print(f"[{i}] - {session}")
            session_index = int(input("Ввод: "))

            client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash).start(sessions[session_index].replace('\n', ''))
            
            asyncio.get_event_loop().run_until_complete(get_contacts(client))

        elif selection == 'e':
            break
