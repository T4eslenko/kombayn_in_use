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
import asyncio  
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
                            f"{color.DARKCYAN}4 - КОНТАКТЫ{color.END}\n"
                            f"{color.DARKCYAN}5 - Информация о каналах и группах{color.END}\n"
                            f"{color.DARKCYAN}6 - УЧАСТНИКОВ чата{color.END}\n"
                            f"{color.DARKCYAN}7 - СООБЩЕНИЯ из канала или СОБЩЕНИЯ и УЧАСТНИКОВ чата {color.END}\n"  
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
           header = '''
-----------------------------
=ВЫГРУЗКА КОНТАКТОВ В EXCEL=
-----------------------------
           '''
           result = choice_akk(api_id, api_hash, header)
           if result is None:
               continue
           client, phone, session_index = result
           userid, userinfo, firstname, lastname, username = get_user_info(client, phone) # Получение информации о пользователe
           print()
           print('-----------------------------')
           print('=ИНФОРМАЦИЯ О КОНТАКТАХ=')
           print('-----------------------------')
           get_and_save_contacts(client, phone, userinfo, userid)
           print()
           input("\033[93mНажмите любую клавишу для продолжения... \033[0m")             
           client.disconnect()

       # 5 Выгрузить инфу об аккаунте
        elif selection == '5':
           os.system('cls||clear')
           sessions = []
           header = '''
-----------------------------
=ВЫГРУЗКА ИНФОРМАЦИИ о КАНАЛАХ и ГРУППАХ в EXCEL=
-----------------------------
           '''
           result = choice_akk(api_id, api_hash, header)
           if result is None:
               continue
           os.system('cls||clear')
           client, phone, session_index = result
           print('-----------------------------') 
           userid, userinfo, firstname, lastname, username = get_user_info(client, phone) # Получение информации о пользователe
           print()
           delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, openchannels_id, closechannels_id = get_type_of_chats(client, selection)  # Получение информации о чатах и каналах
           groups, i, all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = make_list_of_channels(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, selection)
           print()
           print_suminfo_about_channel(openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup)
           input("\033[93mНажмите любую клавишу для продолжения... \033[0m")
           os.system('cls||clear')
           print('-----------------------------')
           print('=ИНФОРМАЦИЯ О КАНАЛАХ и ГРУППАХ=')
           print('-----------------------------')
           while True:
               print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
               print('-----------------------------')
               # Выводим информацию о группах
               print_pages(all_info, 25)
               print('-----------------------------')
               print()
               save_about_channels(phone, userid, firstname, lastname, username, openchannel_count, opengroup_count, closechannel_count, closegroup_count, owner_channel, owner_closechannel, owner_group, owner_closegroup, openchannels, closechannels, openchats, closechats, delgroups, closegroupdel_count)
               print()
               input("Для продолжение нажмите любую клавишу  ")
               os.system('cls||clear')
               print('Инофрмация о чатах  добавлена в файл, мой командир')
               time.sleep(3)
               client.disconnect()
               break
           
        # 6 Выгрузить участников групп в excel
        elif selection == '6':
           last_date = None    
           size_chats = 200
           exit_flag = False
           while not exit_flag:
              os.system('cls||clear')
              sessions = []
              header = '''
   -----------------------------
   =ВЫГРУЗКА УЧАСТНИКОВ ГРУП в EXCEL=
   -----------------------------
              '''
              result = choice_akk(api_id, api_hash, header)
              if result is None:
                  break
              os.system('cls||clear')
              client, phone, session_index = result
              print('-----------------------------') 
              userid, userinfo, firstname, lastname, username = get_user_info(client, phone) # Получение информации о пользователe
              print()
              delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, openchannels_id, closechannels_id = get_type_of_chats(client, selection)  # Получение информации о чатах и каналах
              groups, i, all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = make_list_of_channels(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, selection)
              print()
              print_suminfo_about_channel(openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup)
              input("\033[93mНажмите любую клавишу для продолжения... \033[0m")
              while True:
                   os.system('cls||clear')
                   i = 0
                   print('-----------------------------')
                   print('=ВЫГРУЗКА УЧАСТНИКОВ ЧАТА В EXCEL=')
                   print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                   print('-----------------------------')
                   groups, i, all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = make_list_of_channels(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, selection)
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
                               get_participants_and_save_xlsx(client, target_group, user_id, user_name, group_title, group_id, userid, userinfo)
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

        # 7 Выгрузить сообщения канала или сообщения и участников чата в excel
        elif selection == '7':
            os.system('cls||clear')
            last_date = None    
            size_chats = 200
            exit_flag = False
            while not exit_flag:
              os.system('cls||clear')
              sessions = []
              header = '''
   -----------------------------
   =ВЫГРУЗКА СООБЩЕНИЙ из КАНАЛА или СООБЩЕНИЙ и УЧАСТНИКОВ ЧАТА в EXCEL=
   -----------------------------
              '''
              result = choice_akk(api_id, api_hash, header)
              if result is None:
                  break
              os.system('cls||clear')
              client, phone, session_index = result
              print('-----------------------------') 
              userid, userinfo, firstname, lastname, username = get_user_info(client, phone) # Получение информации о пользователe
              print()
              delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, openchannels_id, closechannels_id = get_type_of_chats(client, selection)  # Получение информации о чатах и каналах
              #groups, i, all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = make_list_of_channels(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, selection)
              print()
              print_suminfo_about_channel(openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup)
              input("\033[93mНажмите любую клавишу для продолжения... \033[0m")
              while True:
                   os.system('cls||clear')
                   i = 0
                   print('-----------------------------')
                   print('=ВЫГРУЗКА СООБЩЕНИЙ из КАНАЛА или СООБЩЕНИЙ и УЧАСТНИКОВ ЧАТА в EXCEL=')
                   print(f"\033[96mНомер телефона: +{phone}, ID: {userid}, ({firstname}{lastname}) {username}\033[0m")
                   print('-----------------------------')
               
                   groups, i, all_info, openchannel_count, closechannel_count, opengroup_count, closegroup_count, closegroupdel_count, owner_channel, owner_closechannel, owner_group, owner_closegroup = make_list_of_channels(delgroups, chat_message_counts, openchannels, closechannels, openchats, closechats, selection)
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
                              os.system('cls||clear')
                              print('Может потребоваться значительное количество времени, заварите кофе...')
                              get_messages_and_save_xcls(client, target_group, user_id, user_name, group_title, userid, userinfo)
                              group_id = target_group.id
                              if group_id not in openchannels_id and group_id not in closechannels_id:
                                 get_participants_and_save_xlsx(client, target_group, user_id, user_name, group_title, group_id, userid, userinfo)
                                 os.system('cls||clear')
                                 print('Сообщения чата и его участники выгружены в excel, мой командир')
                              else:
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
            config(api_id, api_hash, selection, bot, admin_chat_ids) 


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


