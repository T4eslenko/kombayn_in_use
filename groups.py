import os
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Chat, Channel

def channelandgroups(api_id, api_hash):
    os.system('cls||clear')
    chats = []
    last_date = None
    size_chats = 500
    groups = []
    exit_flag = False
    openchannels = []
    closechannels = []
    openchats = []
    closechats = []

    while not exit_flag:
        os.system('cls||clear')
        print("Выберите существующий аккаунт для получения ссылок на подключенные чаты (e - назад)\n")
        sessions = [file for file in os.listdir('.') if file.endswith('.session')]

        for i in range(len(sessions)):
            print(f"[{i}] - {sessions[i]}")
        print()

        user_input = input("Ввод: ")
        if user_input.lower() == 'e':
            break
        else:
            try:
                i = int(user_input)
                if 0 <= i < len(sessions):
                    client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash)
                    client.connect()
                    result = client(GetDialogsRequest(
                        offset_date=last_date,
                        offset_id=0,
                        offset_peer=InputPeerEmpty(),
                        limit=size_chats,
                        hash=0
                    ))
                    chats.extend(result.chats)

                    # Парсим информацию обо всех группах
                    for chat in chats:
                        if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                            if chat.broadcast == False and chat.username == None:
                                closechats.append(chat)
                                groups.append(chat)
                        if isinstance(chat, Chat) and chat.migrated_to is None:
                            closechats.append(chat)
                            groups.append(chat)

                        if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                            if chat.broadcast and chat.username:
                                openchannels.append(chat)
                                groups.append(chat)

                        if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                            if chat.broadcast and chat.username == None and chat.title != 'Unsupported Chat':
                                closechannels.append(chat)
                                groups.append(chat)

                        if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                            if chat.broadcast == False and chat.username:
                                openchats.append(chat)
                                groups.append(chat)

                    while True:
                        os.system('cls||clear')
                        oc = 0
                        cc = 0
                        og = 0
                        cg = 0
                        owner_channel = 0
                        owner_group = 0
                        owner_closegroup = 0
                        owner_closechannel = 0
                        print('-----------------------------')
                        print('=ИНФОРМАЦИЯ О КАНАЛАХ И ЧАТАХ=')
                        print('-----------------------------')
                        print()
                        print("\033[95mОткрытые КАНАЛЫ:\033[0m")
                        for openchannel in openchannels:
                            owner = " (Владелец)" if openchannel.creator else ""
                            admin = " (Администратор)" if openchannel.admin_rights is not None else ""
                            print(f"{oc} - {openchannel.title} [{openchannel.participants_count}]\033[91m{owner} {admin}\033[0m ID:{openchannel.id} @{openchannel.username}")
                            oc += 1
                            if owner !="" or admin != "":
                                owner_channel += 1
                        
                        print()
                        print("\033[95mЗакрытые КАНАЛЫ:\033[0m")
                        for closechannel in closechannels:
                            owner = " (Владелец)" if closechannel.creator else ""
                            admin = " (Администратор)" if closechannel.admin_rights is not None else ""
                            print(f"{cc} - {closechannel.title} [{closechannel.participants_count}] \033[91m{owner} {admin}\033[0m ID:{closechannel.id}")
                            cc += 1
                            if owner !="" or admin != "":
                                owner_channel += 1
                                owner_closechannel += 1
                        
                        print()
                        print("\033[95mОткрытые ГРУППЫ:\033[0m")
                        for openchat in openchats:
                            owner = " (Владелец)" if openchat.creator else ""
                            admin = " (Администратор)" if openchat.admin_rights is not None else ""
                            print(f"{og} - {openchat.title} [{openchat.participants_count}]\033[91m{owner} {admin}\033[0m ID:{openchat.id} @{openchat.username}")
                            og += 1
                            if owner !="" or admin != "":
                                owner_group += 1
                        
                        print()
                        print("\033[95mЗакрытые ГРУППЫ:\033[0m")
                        for closechat in closechats:
                            owner = " (Владелец)" if closechat.creator else ""
                            admin = " (Администратор)" if closechat.admin_rights is not None else ""
                            print(f"{cg} - {closechat.title} [{closechat.participants_count}]\033[91m{owner} {admin}\033[0m ID:{closechat.id}")
                            cg += 1
                            if owner !="" or admin != "":
                                owner_group += 1
                                owner_closegroup += 1
                     
                        print()
                        print("---------------------------------------")
                        print(f"Открытые каналы: {oc}")
                        print(f"Открытые группы: {og}")
                        print()
                        print(f"\033[91mЗакрытые каналы: {cc}\033[0m")
                        print(f"\033[91mЗакрытые группы: {cg}\033[0m")
                        print("---------------------------------------")
                        print(f"\033[96mИмеет права админа в {owner_channel} каналах, из них {owner_closechannel} - в закрытых\033[0m")
                        print(f"\033[96mИмеет права админа в {owner_group} группах, из них {owner_closegroup} - в закрытых\033[0m")

                        g_index_str = str(input("Ввод: "))

                        if g_index_str.lower() == 'e':
                            client.disconnect()
                            groups = []
                            chats = []
                            openchannels = []
                            closechannels = []
                            openchats = []
                            closechats = []
                            owner_channel = 0
                            owner_group = 0
                            owner_closegroup = 0
                            owner_closechannel = 0
                            break
                        else:
                            try:
                                if g_index_str == "get":
                                    parsing_chats(chatids)
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
