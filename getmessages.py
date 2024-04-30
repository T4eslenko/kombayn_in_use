from openpyxl import Workbook
from telethon.tl.types import User

def remove_timezone(dt: datetime) -> Optional[datetime]:
    # Удаление информации о часовом поясе из объекта datetime
    if dt is None:
        return None
    if dt.tzinfo:
        dt = dt.astimezone().replace(tzinfo=None)
    return dt

def get_message_info(client, group_title, msg_id):
    # Получение информации о сообщении
    message = client.get_messages(group_title, ids=[msg_id])[0]
    if message is None:
        return None, None, None, None, None, None
    user_id = message.sender_id if isinstance(message.sender, User) else None
    username = message.sender.username if isinstance(message.sender, User) else None
    first_name = message.sender.first_name if isinstance(message.sender, User) else None
    last_name = message.sender.last_name if isinstance(message.sender, User) else None
    return user_id, username, first_name, last_name, message.date, message.text

def parsing_messages(client, index: int, id_: bool, name: bool, group_title, userid, userinfo):
    wb = Workbook()
    ws = wb.active
    ws.cell(row=1, column=1, value=userinfo)
    ws.append(['ID объекта', 'Group ID', 'Message ID', 'Date and Time', 'User ID', '@Username', 'First Name', 'Last Name', 'Message', 'Reply to Message', 'Reply to User ID', '@Reply Username', 'Reply First Name', 'Reply Last Name', 'Reply Message ID', 'Reply Date and Time'])

    for message in client.get_messages(group_title, limit=None, reverse=True):
        # Проверяем, что message является экземпляром Message
        if not isinstance(message, Message):
            continue
        # Основная информация о сообщении
        user_id, username, first_name, last_name, date, text = get_message_info(client, group_title, message.id)
        if date is None:
            continue
        row_data = [
            userid,
            message.chat_id,
            message.id,
            remove_timezone(date),
            user_id,
            f"@{username}" if username else None,
            first_name,
            last_name,
            text
        ]

        # Если сообщение является ответом на другое сообщение
        if isinstance(message.reply_to_msg_id, int):
            reply_msg_id = message.reply_to_msg_id
            reply_user_id, reply_username, reply_first_name, reply_last_name, reply_date, reply_text = get_message_info(client, group_title, reply_msg_id)
            if reply_date is None:
                continue
            row_data.extend([
                reply_text,
                reply_user_id,
                f"@{reply_username}" if reply_username else None,
                reply_first_name,
                reply_last_name,
                reply_msg_id,
                remove_timezone(reply_date)
            ])

        else:
            row_data.extend([None] * 7)

        ws.append(row_data)

    # Сохраняем книгу Excel с названием, содержащим group_title
    filename = f"{group_title}_messages.xlsx"
    wb.save(filename)
