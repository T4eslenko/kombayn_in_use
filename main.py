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
   
                               phone = sessions[session_index].split('.')[0]
                               userid, userinfo, firstname, lastname, username = get_user_info(client, phone) # Получение информации о пользовател

                              
                               result = client(GetContactsRequest(0))
                               contacts = result.users
            
                               session_name = sessions[session_index].replace('.session', '')
                               contacts_file_name = f'{session_name}_contacts.xlsx'
                               save_contacts(client, contacts, contacts_file_name, userinfo, userid)
                               os.system('cls||clear')
                               
                               print('=ИНФОРМАЦИЯ О КОНТАКТАХ=')
                               print('-----------------------------')
                               print()
                               
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
                               os.system('cls||clear')
                       except ValueError:
                           print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                           time.sleep(2)
                           os.system('cls||clear')
           

       
       # 5 Выгрузить инфу об аккаунте
        elif selection == '5':
             
                   
             os.system('cls||clear')
             chats = []
             last_date = None
             size_chats = 500
             groups = []
             exit_flag = False
             
         
         
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
                             phone = sessions[session_index].split('.')[0]
                             #qqqs = client.get_dialogs()
         
                             ##for qqq in qqqs:
                              ##  print(qqq)
                            ## input("нажми")
                            # break
                             
                             # Получение информации о пользователе
                             userid, userinfo, firstname, lastname, username = get_user_info(client, phone)

                             # Получение информации о чатах и каналах
                             delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats = get_type_of_chats(client, selection)
                            
                 
                             while True:
                                 os.system('cls||clear')
                                 print('-----------------------------')
                                 print("=ИНФОРМАЦИЯ О КАНАЛАХ И ЧАТАХ=")
                                 print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                                 print('-----------------------------')
                                 print()
                                 
                                 all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = type_of_channel(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats)        
                                 
                                 openchannel_count = openchannel_count-1
                                 closechannel_count = closechannel_count-1
                                 opengroup_count = opengroup_count-1
                                 closegroupdel_count = closegroupdel_count-1
                                 closegroup_count = closegroup_count-1
                                 print_pages(all_info, 25)
                                 print()
                                 
                                 print("---------------------------------------")
                                 print(f"Открытые каналы: {openchannel_count}")
                                 print(f"Открытые группы: {opengroup_count}")
                                 print()
                                 print(f"\033[91mЗакрытые каналы: {closechannel_count}\033[0m")
                                 print(f"\033[91mЗакрытые группы: {closegroup_count}\033[0m")
                                 print(f"\033[91mУдаленные группы: {closegroupdel_count}\033[0m")
                                 print("---------------------------------------")
                                 print()
                                 print(f"\033[96mИмеет права владельца или админа в {owner_channel} каналах, из них {owner_closechannel} - в закрытых\033[0m")
                                 print(f"\033[96mИмеет права владельца или админа в {owner_group} группах, из них {owner_closegroup} - в закрытых\033[0m")
                                 print()
                                 
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
                                             ws.append([f"Открытые каналы: {openchannel_count}"])
                                             ws.append([f"Открытые группы: {opengroup_count}"])
                                             ws.append([f"Закрытые каналы: {closechannel_count}"])
                                             ws.append([f"Закрытые группы: {closegroup_count}"])
                                             ws.append([f"Имеет права владельца или админа в {owner_channel} каналах, из них {owner_closechannel} - в закрытых"])
                                             ws.append([f"Имеет права владельца или админа в {owner_group} группах, из них {owner_closegroup} - в закрытых"])
         
                                             ws_open_channels = wb.create_sheet("Открытые Каналы")
                                             ws_closed_channels = wb.create_sheet("Закрытые Каналы")
                                             ws_open_groups = wb.create_sheet("Открытые Группы")
                                             ws_closed_groups = wb.create_sheet("Закрытые Группы")
                                             ws_closed_groups_del = wb.create_sheet("Удаленные Группы")
                                             write_data(ws_open_channels, openchannels)
                                             write_data(ws_closed_channels, closechannels)
                                             write_data(ws_open_groups, openchats)
                                             write_data(ws_closed_groups, closechats)
                                             write_data_del(ws_closed_groups_del, delgroups)
                                             wb.save(f"{phone}_about.xlsx")
                                             os.system('cls||clear')
                                             print('Ссылки на чаты добавлены в файл, мой командир')
                                             time.sleep(3)
                                             exit_flag = True
                                             client.disconnect()
                                             break
                                         else:
                                             print("Пожалуйста, сделайте свой выбор")
                                             time.sleep(2)
                                             all_info = []
                                             os.system('cls||clear')
                                     except ValueError:
                                         print("Пожалуйста, сделайте свой выбор")
                                         time.sleep(2)
                                         all_info = []
                                         os.system('cls||clear')
                         else:
                             print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions) - 1)
                             time.sleep(2)
                             os.system('cls||clear')
                     except ValueError:
                         print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions) - 1)
                         time.sleep(2)   
                         os.system('cls||clear')
              
           
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
                          phone = sessions[session_index].split('.')[0]
      
                          # Получение информации о пользователе
                          userid, userinfo, firstname, lastname, username = get_user_info(client, phone)
                         
                         # Получение информации о чатах и каналах
                          delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats = get_type_of_chats(client, selection)
                         
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
                                          all_info = []
                                          os.system('cls||clear')
                                  except ValueError:
                                      print("Пожалуйста, выберите группу из списка")
                                      time.sleep(2)
                                      all_info = []
                                      os.system('cls||clear')
                      else:
                          print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                          time.sleep(2)
                          os.system('cls||clear')
                  except ValueError:
                      print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                      time.sleep(2)
                      os.system('cls||clear')

           
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
                            phone = sessions[session_index].split('.')[0]
                           
                            # Получение информации о пользователе
                            userid, userinfo, firstname, lastname, username = get_user_info(client, phone)

                            # Получение информации о чатах и каналах
                            delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats = get_type_of_chats(client, selection)

                                 
                            
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
                                            all_info = []
                                            os.system('cls||clear')
                                    except ValueError:
                                        print("Пожалуйста, выберите группу из списка")
                                        time.sleep(2)
                                        all_info = []
                                        os.system('cls||clear')
                        else:
                            print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                            time.sleep(2)
                            os.system('cls||clear')
                    except ValueError:
                        print("Пожалуйста, выберите существующий аккаунт в диапазоне от 0 до", len(sessions)-1)
                        time.sleep(2)
                        os.system('cls||clear')
    
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
            config(api_id, api_hash, selection) 


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


