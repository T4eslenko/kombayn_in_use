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
                        #try:
                            # Закрытые группы
                            if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                                if chat.broadcast == False and chat.username == None:
                                    closechats.append(chat)
                                    groups.append(chat)
                            if isinstance(chat, Chat) and chat.migrated_to is None:
                                closechats.append(chat)
                                groups.append(chat)

                            # Открытые каналы
                            if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                                if chat.broadcast and chat.username:
                                    openchannels.append(chat)
                                    groups.append(chat)

                            # Закрытые каналы
                            if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                                if chat.broadcast and chat.username == None:
                                    closechannels.append(chat)
                                    groups.append(chat)

                            # Открытые группы
                            if isinstance(chat, Channel) and hasattr(chat, 'broadcast'):
                                if chat.broadcast == False and chat.username:
                                    openchats.append(chat)
                                    groups.append(chat)

                        #except:
                            #continue

                    while True:
                        os.system('cls||clear')
                        oc = 0
                        cc = 0
                        og = 0
                        cg = 0
                        print('-----------------------------')
                        print('=ИНФОРМАЦИЯ О КАНАЛАХ И ЧАТАХ=')
                        print('-----------------------------')

                        # for groups in groups:
                        print("Открытые каналы:")
                        for openchannel in openchannels:
                            owner = " (Владелец)" if openchannel.creator else ""
                            admin = " (Администратор)" if openchannel.admin_rights is not None else ""
                            print(f"{oc} - {openchannel.title} \033[91m{owner} {admin}\033[0m ID:{openchannel.id} @{openchannel.username}")
                            oc += 1
                        
                        print("Закрытые каналы:")
                        for closechannel in closechannels:
                            owner = " (Владелец)" if closechannel.creator else ""
                            admin = " (Администратор)" if closechannel.admin_rights is not None else ""
                            print(f"{cc} - {closechannel.title} \033[91m{owner} {admin}\033[0m ID:{closechannel.id}")
                            cc += 1
                        
                        print("Открытые группы:")
                        for openchat in openchats:
                            owner = " (Владелец)" if openchat.creator else ""
                            admin = " (Администратор)" if openchat.admin_rights is not None else ""
                            print(f"{og} - {openchat.title} \033[91m{owner} {admin}\033[0m ID:{openchat.id} @{openchat.username}")
                            og += 1
                        
                        print("Закрытые группы:")
                        for closechat in closechats:
                            owner = " (Владелец)" if closechat.creator else ""
                            admin = " (Администратор)" if closechat.admin_rights is not None else ""
                            print(f"{cg} - {closechat.title} \033[91m{owner} {admin}\033[0m ID:{closechat.id}")
                            cg += 1




                        print(f"Открытые каналы: {oc}")
                        print(f"Закрытые каналы: {cc}")
                        print(f"Открытые группы: {og}")
                        print(f"Закрытые группы: {cg}")

                        g_index_str = str(input("Ввод: "))

                        if g_index_str.lower() == 'e':
                            client.disconnect()
                            groups = []
                            chats = []
                            openchannels = []
                            closechannels = []
                            openchats = []
                            closechats = []
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