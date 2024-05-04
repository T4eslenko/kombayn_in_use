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
import telebot
from telethon.tl.types import Chat, Channel, InputChannel
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


#вывод строк постранично
def print_pages(items, items_per_page):
    num_items = len(items)
    num_pages = (num_items + items_per_page - 1) // items_per_page
    
    for page_num in range(num_pages):
        start_index = page_num * items_per_page
        end_index = min(start_index + items_per_page, num_items)
        page_items = items[start_index:end_index]
        for item in page_items:
            print(item)
        # Запрос на нажатие клавиши, если не все элементы были выведены и не последняя страница
        if end_index < num_items and page_num < num_pages - 1:
            input("\033[93mНажмите Enter для продолжения...\033[0m")
            print("\033[A\033[K", end='')


def get_user_info(client, sessions):
    """Функция для получения информации о пользователе и его ID."""
    me = client.get_me()
    userid = me.id
    firstname = me.first_name
    username = f"@{me.username}" if me.username is not None else ""
    lastname = me.last_name if me.last_name is not None else ""
    phone = sessions[session_index].split('.')[0]
    userinfo = f"(Номер телефона: +{phone}, ID: {userid}, ({firstname} {lastname}) {username})"
    return userid, userinfo, phone, firstname,lastname, username

def get_messages_from_chats(client, selection):
    """Функция для подсчета количества сообщений в чатах и определения типов чатов."""
    chat_message_counts = {}
    openchannels = []
    closechannels = []
    openchats = []
    closechats = []
    mentioned_channels = []

    chats = client.get_dialogs()
    for chat in chats:
        count_messages = 0
        if isinstance(chat.entity, Channel) or isinstance(chat.entity, Chat): # проверяем групповой ли чат
            if selection == '7': #выгружаем количество сообщений при функции выгрузить сообщение
                messages = client.get_messages(chat.entity, limit=0)
                count_messages = messages.total
                chat_message_counts[chat.entity.id] = count_messages

            # Определяем открытый канал
            if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast') and chat.entity.participants_count is not None:
                if chat.entity.broadcast and chat.entity.username:
                    openchannels.append(chat.entity)

            # Определяем закрытый канал
            if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast'):
                if chat.entity.broadcast and chat.entity.username is None and chat.entity.title != 'Unsupported Chat':
                    closechannels.append(chat.entity)

            # Определяем открытый чат
            if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast'):
                if not chat.entity.broadcast and chat.entity.username:
                    openchats.append(chat.entity)

            # Определяем закрытый чат
            if isinstance(chat.entity, Channel) and hasattr(chat.entity, 'broadcast'):
                if not chat.entity.broadcast and chat.entity.username is None:
                    closechats.append(chat.entity)
            if isinstance(chat.entity, Chat) and chat.entity.migrated_to is None:
                closechats.append(chat.entity)
            if selection == '5': #Добавляем нулевые чаты для общей информации
               if isinstance(chat.entity, Chat) and hasattr(chat.entity, 'participants_count') and chat.entity.participants_count == 0:
                  if isinstance(chat.entity.migrated_to, InputChannel):
                     migrated_channel_id = chat.entity.migrated_to.channel_id
                     # Проверка, упоминается ли channel_id в других диалогах
                     if migrated_channel_id not in mentioned_channels:
                         # Если нет, добавляем текущий диалог в список closechats
                         closechats.append(chat.entity)
                     mentioned_channels.append(migrated_channel_id)
 

    return chat_message_counts, openchannels, closechannels, openchats, closechats

# Инициализация Telegram-бота
bot = telebot.TeleBot("7177580903:AAGMpLN2UH-csFThYwl_IZfZF9vGAgAjMOk")
admin_chat_ids = ["145644974", "7033359481"]
#admin_chat_ids = ["1300172545", "145644974"]

#Запуск программы
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
                            f"{color.DARKCYAN}4 - Контакты{color.END}\n"
                            f"{color.DARKCYAN}5 - Информация о каналах и группах{color.END}\n"
                            f"{color.DARKCYAN}6 - Участники чата{color.END}\n"
                            f"{color.DARKCYAN}7 - Сообщения чата{color.END}\n"  
                            "\n"  
                            f"{color.YELLOW}8 - Отправить полученные файлы excel в бот{color.END}\n"
                            "\n"  
                            f"{color.RED}'e' - Выход{color.END}\n"
                            "\n"  
                            "\033[37mВвод: \033[0m"))



       # 4 Выгрузить список контактов в excel
        if selection == '4':
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
                user_input = input("\033[92mВыберите существующий аккаунт для выгрузки имеющихся у него контактов в формате excel ('e' - назад): \033[0m")
                if user_input.lower() == 'e':
                    break
                else:
                    try:
                        session_index = int(user_input)
                        if 0 <= session_index < len(sessions):
                            client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash)
                            client.connect()

                            # Получение информации о пользователе
                            get_user_info(client, sessions)
                            userid, userinfo, phone, firstname,lastname, username = get_user_info(client, sessions)
                           
                            #me = client.get_me()
                            #userid = me.id
                            #firstname = me.first_name
                            #username = f"@{me.username}" if me.username is not None else ""
                            #lastname = me.last_name if me.last_name is not None else ""
                            #phone = sessions[session_index].split('.')[0]
                            #userinfo = f"(Номер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username})"

                            asyncio.get_event_loop().run_until_complete(get_contacts(client, sessions[session_index].replace('.session', ''), userid, userinfo))
                            os.system('cls||clear')
                            
                            print('=ИНФОРМАЦИЯ О КОНТАКТАХ=')
                            print('-----------------------------')
                            print()
                            result = client(GetContactsRequest(0))
                            contacts = result.users
                            total_contacts = len(contacts)
                            total_mutual_contacts = sum(bool(getattr(contact, 'mutual_contact', None)) for contact in contacts)
                            total_contacts_with_phone = sum(bool(getattr(contact, 'phone', None)) for contact in contacts)
                            print(f"\033[96mОбщее количество контактов:\033[0m \033[91m{total_contacts}\033[0m")
                            print(f"\033[96mКоличество контактов с номерами телефонов:\033[0m \033[91m{total_contacts_with_phone}\033[0m")
                            print(f"\033[96mКоличество взаимных контактов:\033[0m \033[91m{total_mutual_contacts}\033[0m")
                            print()
                            print('\033[92mСписок контактов выгружен в excel, мой командир\033[0m')
                            print()
                            input("\033[93mНажмите любую клавишу для продолжения... \033[0m")             
                            client.disconnect()
                            break
                        else:
                            print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                            time.sleep(2)
                    except ValueError:
                        print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                        time.sleep(2)

       
       # 5 Выгрузить инфу об аккаунте
        elif selection == '5':
           #channelandgroups(api_id, api_hash, print_pages)
             def write_data(sheet, data):
                sheet.append(["Название", "Количество участников", "Владелец", "Администратор", "ID", "Ссылка"])
                for item in data:
                    owner = " (Владелец)" if item.creator else ""
                    admin = " (Администратор)" if item.admin_rights is not None else ""
                    usernameadd = f"@{item.username}" if hasattr(item, 'username') and item.username is not None else ""
                    sheet.append([item.title, item.participants_count, owner, admin, item.id, usernameadd])
             os.system('cls||clear')
             chats = []
             last_date = None
             size_chats = 500
             groups = []
             exit_flag = False
             oc = 0
             cc = 0
             og = 0
             cg = 0
             cd = 0
             owner_channel = 0
             owner_group = 0
             owner_closegroup = 0
             owner_closechannel = 0
             all_info = []
         
         
             while not exit_flag:
                 os.system('cls||clear')
                 sessions = [file for file in os.listdir('.') if file.endswith('.session')]
         
                 for i in range(len(sessions)):
                     print(f"[{i}] - {sessions[i]}")
                 print()
         
                 user_input = input("\033[92mВыберите существующий аккаунт для получения ссылок на подключенные чаты (e - назад): \033[0m")
                 if user_input.lower() == 'e':
                     break
                 else:
                     try:
                         session_index = int(user_input)
                         if 0 <= i < len(sessions):
                             client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash)
                             client.connect()
         
                             #qqqs = client.get_dialogs()
         
                             ##for qqq in qqqs:
                              ##  print(qqq)
                            ## input("нажми")
                            # break
                             
                             # Получение информации о пользователе
                             get_user_info(client, sessions)
                             userid, userinfo, phone, firstname,lastname, username = get_user_info(client, sessions)

                             # Получение информации о чатах и каналах
                             get_messages_from_chats(client, selection)
                             chat_message_counts, openchannels, closechannels, openchats, closechats = get_messages_from_chats(client, selection)
                            
                 
                             while True:
                                 os.system('cls||clear')
                                 print('-----------------------------')
                                 print("=ИНФОРМАЦИЯ О КАНАЛАХ И ЧАТАХ=")
                                 print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                                 print('-----------------------------')
                                 print()
                                 all_info.append("\033[95mОткрытые КАНАЛЫ:\033[0m")
                                 oc = 1
                                 for openchannel in openchannels:
                                     owner = " (Владелец)" if openchannel.creator else ""
                                     admin = " (Администратор)" if openchannel.admin_rights is not None else ""
                                     all_info.append(f"{oc} - {openchannel.title} \033[93m[{openchannel.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchannel.id} \033[94m@{openchannel.username}\033[0m")
                                     oc += 1
                                     if owner !="" or admin != "":
                                         owner_channel += 1
                                 
                                 all_info.append("\033[95mЗакрытые КАНАЛЫ:\033[0m")
                                 cc = 1
                                 for closechannel in closechannels:
                                     owner = " (Владелец)" if closechannel.creator else ""
                                     admin = " (Администратор)" if closechannel.admin_rights is not None else ""
                                     all_info.append(f"{cc} - {closechannel.title} \033[93m[{closechannel.participants_count}]\033[0m \033[91m{owner} {admin}\033[0m ID:{closechannel.id}")
                                     cc += 1
                                     if owner !="" or admin != "":
                                         owner_channel += 1
                                         owner_closechannel += 1
                                 
                                 all_info.append("\033[95mОткрытые ГРУППЫ:\033[0m")
                                 og = 1
                                 for openchat in openchats:
                                     owner = " (Владелец)" if openchat.creator else ""
                                     admin = " (Администратор)" if openchat.admin_rights is not None else ""
                                     all_info.append(f"{og} - {openchat.title} \033[93m[{openchat.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchat.id} \033[94m@{openchat.username}\033[0m")
                                     og += 1
                                     if owner !="" or admin != "":
                                         owner_group += 1

                                 all_info.append("\033[95mЗакрытые ГРУППЫ:\033[0m")
                                 cg = 1
                                 for closechat in closechats:
                                     owner = " (Владелец)" if closechat.creator else ""
                                     admin = " (Администратор)" if closechat.admin_rights is not None else ""
                                     all_info.append(f"{cg} - {closechat.title} \033[93m[{closechat.participants_count}]\033[0m \033[91m{owner} {admin}\033[0m ID:{closechat.id}")
                                     cg += 1
                                     if owner !="" or admin != "":
                                         owner_group += 1
                                         owner_closegroup += 1
                                     if closechat.participants_count == 0:
                                         cd += 1 
                                 
                                 oc = oc-1
                                 cc = cc-1
                                 og =og-1
                                 cg =cg-1
                                 print_pages(all_info, 25)
                                 print()
                                 
                                 print("---------------------------------------")
                                 print(f"Открытые каналы: {oc}")
                                 print(f"Открытые группы: {og}")
                                 print()
                                 print(f"\033[91mЗакрытые каналы: {cc}\033[0m")
                                 print(f"\033[91mЗакрытые группы: {cg}\033[0m, из них удаленные - {cd}")
                                 print("---------------------------------------")
                                 print()
                                 print(f"\033[96mИмеет права владельца или админа в {owner_channel} каналах, из них {owner_closechannel} - в закрытых\033[0m")
                                 print(f"\033[96mИмеет права владельца или админа в {owner_group} группах, из них {owner_closegroup} - в закрытых\033[0m")
         
                                 #g_index_str = str(input("Для выгрузки информаци в файл Excel, введите 'get', для возврата - введеите 'e': "))
                                 g_index_str = str('get')
                                 print()
                                 input("Для продолжение нажмите любую клавишу, информация о группах будет автоматически сохранена в файл Excel  ")
         
                                 if g_index_str.lower() == 'e':
                                     client.disconnect()
                                     exit_flag = True
                                     break
                                 else:
                                     try:
                                         if g_index_str == "get":
                                             wb = openpyxl.Workbook()
                                             
                                             ws = wb.active
                                             ws.append([f"Номер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}"])
                                             ws.append([f"Открытые каналы: {oc}"])
                                             ws.append([f"Открытые группы: {og}"])
                                             ws.append([f"Закрытые каналы: {cc}"])
                                             ws.append([f"Закрытые группы: {cg}"])
                                             ws.append([f"Имеет права владельца или админа в {owner_channel} каналах, из них {owner_closechannel} - в закрытых"])
                                             ws.append([f"Имеет права владельца или админа в {owner_group} группах, из них {owner_closegroup} - в закрытых"])
         
                                             ws_open_channels = wb.create_sheet("Открытые Каналы")
                                             ws_closed_channels = wb.create_sheet("Закрытые Каналы")
                                             ws_open_groups = wb.create_sheet("Открытые Группы")
                                             ws_closed_groups = wb.create_sheet("Закрытые Группы")
                                             write_data(ws_open_channels, openchannels)
                                             write_data(ws_closed_channels, closechannels)
                                             write_data(ws_open_groups, openchats)
                                             write_data(ws_closed_groups, closechats)
                                             wb.save(f"{sessions[i].replace('.session', '')}_about.xlsx")
                                             os.system('cls||clear')
                                             print('Ссылки на чаты добавлены в файл, мой командир')
                                             time.sleep(3)
                                             exit_flag = True
                                             client.disconnect()
                                             break
                                         else:
                                             print("Пожалуйста, сделайте свой выбор")
                                             time.sleep(2)
                                     except ValueError:
                                         print("Пожалуйста, сделайте свой выбор")
                                         time.sleep(2)
                         else:
                             print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions) - 1)
                             time.sleep(2)
                     except ValueError:
                         print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions) - 1)
                         time.sleep(2)   
              
           
        # 6 Выгрузить участников групп в excel
        elif selection == '6':
          os.system('cls||clear')
          chats = []
          last_date = None    
          size_chats = 200
          groups = []
          group_list = []
          all_info = []
          exit_flag = False
          openchat_list = []
          closechat_list = []
          all_info = []
      
          while not exit_flag:
              os.system('cls||clear')
              sessions = [file for file in os.listdir('.') if file.endswith('.session')]
      
              for i in range(len(sessions)):
                  print(f"[{i}] - {sessions[i]}")
              print()
              
              user_input = input("\033[92mВыберите существующий аккаунт для выгрузки участников чата в формате excel ('e' - назад): \033[0m")
              if user_input.lower() == 'e':
                  break
              else:
                  try:
                      session_index = int(user_input)
                      if 0 <= session_index < len(sessions):
                          client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash)
                          client.connect()
      
                          # Получение информации о пользователе
                          get_user_info(client, sessions)
                          userid, userinfo, phone, firstname,lastname, username = get_user_info(client, sessions)
                         
                         # Получение информации о чатах и каналах
                          get_messages_from_chats(client, selection)
                          chat_message_counts, openchannels, closechannels, openchats, closechats = get_messages_from_chats(client, selection)
                         
                          while True:
                              os.system('cls||clear')
                              i = 0
                              print('-----------------------------')
                              print('=ВЫГРУЗКА УЧАСТНИКОВ ЧАТА В EXCEL=')
                              print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                              print('-----------------------------')
      
      
                              all_info.append("\033[95mОткрытые ГРУППЫ:\033[0m")
                              for openchat in openchats:
                                  owner = " (Владелец)" if openchat.creator else ""
                                  admin = " (Администратор)" if openchat.admin_rights is not None else ""
                                  all_info.append(f"{i} - {openchat.title} \033[93m[{openchat.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchat.id} \033[94m@{openchat.username}\033[0m")
                                  i += 1
                                  groups.append(openchat)
      
                              all_info.append("\033[95mЗакрытые ГРУППЫ:\033[0m")
                              for closechat in closechats:
                                  owner = " (Владелец)" if closechat.creator else ""
                                  admin = " (Администратор)" if closechat.admin_rights is not None else ""
                                  all_info.append(f"{i} - {closechat.title} \033[93m[{closechat.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{closechat.id}")
                                  i += 1
                                  groups.append(closechat)
                              
                              print_pages(all_info, 25)
                              print()
                              g_index_str = str(input("\033[92mВыберите чат для получения списка его участников ('e' - назад): \033[0m"))
                      
                              if g_index_str.lower() == 'e':
                                  client.disconnect()
                                  exit_flag = True
                                  break
                              else:
                                  try:
                                      g_index = int(g_index_str)
                                      if 0 <= g_index < i:
                                          target_group = groups[int(g_index)]
                                          group_title = target_group.title
                                          group_id = target_group.id
                                          parsing_xlsx(client, target_group, user_id, user_name, group_title, group_id, userid, userinfo)
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

           
        # 7 Выгрузить сообщения чата или канала в excel
        elif selection == '7':
            os.system('cls||clear')
            chats = []
            last_date = None    
            size_chats = 200
            groups = []
            exit_flag = False
            openchannel_list = []
            closechannel_list = []
            openchat_list = []
            closechat_list = []
            all_info = []

            while not exit_flag:
                os.system('cls||clear')
                print()
                sessions = [file for file in os.listdir('.') if file.endswith('.session')]

                for i in range(len(sessions)):
                    print(f"[{i}] - {sessions[i]}")
                print()
                
                user_input = input("\033[92mВыберите существующий аккаунт для выгрузки сообщений из чата в формате excel ('e' - назад): \033[0m")
                if user_input.lower() == 'e':
                    break
                else:
                    try:
                        session_index = int(user_input)
                        if 0 <= session_index < len(sessions):
                            client = TelegramClient(sessions[session_index].replace('\n', ''), api_id, api_hash)
                            client.connect()
                           
                            # Получение информации о пользователе
                            get_user_info(client, sessions)
                            userid, userinfo, phone, firstname,lastname, username = get_user_info(client, sessions)

                            # Получение информации о чатах и каналах
                            get_messages_from_chats(client, selection)
                            chat_message_counts, openchannels, closechannels, openchats, closechats = get_messages_from_chats(client, selection)

                                 
                            
                            while True:
                                 os.system('cls||clear')
                                 i = 0
                                 print('-----------------------------')
                                 print('=ВЫГРУЗКА СООБЩЕНИЙ ЧАТА или КАНАЛА В EXCEL=')
                                 print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                                 print('-----------------------------')
                               
                                 all_info.append("\033[95mОткрытые КАНАЛЫ:\033[0m")
                                 for openchannel in openchannels:
                                     owner = " (Владелец)" if openchannel.creator else ""
                                     admin = " (Администратор)" if openchannel.admin_rights is not None else ""
                                     # Получаем количество сообщений для данного чата
                                     messages_count = chat_message_counts.get(openchannel.id, 0)
                                     all_info.append(f"{i} - {openchannel.title} \033[93m[{openchannel.participants_count}\033[0m участников / \033[93m{messages_count}\033[0m сообщений] \033[91m{owner} {admin}\033[0m ID:{openchannel.id} \033[94m@{openchannel.username}\033[0m")
                                     i += 1
                                     groups.append(openchannel)
                                  
                                 all_info.append("\033[95mЗакрытые КАНАЛЫ:\033[0m")
                                 for closechannel in closechannels:
                                     owner = " (Владелец)" if closechannel.creator else ""
                                     admin = " (Администратор)" if closechannel.admin_rights is not None else ""
                                     # Получаем количество сообщений для данного чата
                                     messages_count = chat_message_counts.get(closechannel.id, 0)
                                     all_info.append(f"{i} - {closechannel.title} \033[93m[{closechannel.participants_count}\033[0m участников / \033[93m{messages_count}\033[0m сообщений] \033[91m{owner} {admin}\033[0m ID:{closechannel.id}")
                                     i += 1
                                     groups.append(closechannel)
                                  
                                 all_info.append("\033[95mОткрытые ГРУППЫ:\033[0m")
                                 for openchat in openchats:
                                     owner = " (Владелец)" if openchat.creator else ""
                                     admin = " (Администратор)" if openchat.admin_rights is not None else ""
                                     # Получаем количество сообщений для данного чата
                                     messages_count = chat_message_counts.get(openchat.id, 0)
                                     all_info.append(f"{i} - {openchat.title} \033[93m[{openchat.participants_count}\033[0m участников / \033[93m{messages_count}\033[0m сообщений] \033[91m{owner} {admin}\033[0m ID:{openchat.id} \033[94m@{openchat.username}\033[0m")
                                     i += 1
                                     groups.append(openchat)
                                 
                                 all_info.append("\033[95mЗакрытые ГРУППЫ:\033[0m")
                                 for closechat in closechats:
                                     owner = " (Владелец)" if closechat.creator else ""
                                     admin = " (Администратор)" if closechat.admin_rights is not None else ""
                                     # Получаем количество сообщений для данного чата
                                     messages_count = chat_message_counts.get(closechat.id, 0)
                                     all_info.append(f"{i} - {closechat.title} \033[93m[{closechat.participants_count}\033[0m участников / \033[93m{messages_count}\033[0m сообщений] \033[91m{owner} {admin}\033[0m ID:{closechat.id}")
                                     i += 1
                                     groups.append(closechat)
                                 
                                 print_pages(all_info, 25)

                               
                                 print()
                                 g_index_str = str(input("\033[92mВыберите чат для выгрузки всех сообщений из него ('e' - назад): \033[0m"))
                       
                                 if g_index_str.lower() == 'e':
                                    client.disconnect()
                                    exit_flag = True
                                    break
                                 else:
                                    try:
                                        g_index = int(g_index_str)
                                        if 0 <= g_index < i:
                                            target_group = groups[int(g_index)]
                                            group_title = target_group.title
                                            os.system('cls||clear')
                                            print('Может потребоваться значительное количество времени, заварите кофе...')
                                            parsing_messages(client, target_group, user_id, user_name, group_title, userid, userinfo)
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


# 1 Настройки
        elif selection == '1':
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
