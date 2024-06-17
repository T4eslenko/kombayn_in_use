def get_messages_from_group(client, target_group, selection):
    minsk_timezone = timezone('Europe/Minsk')

    # Информация об объекте
    me = client.get_me()
    userid_client = me.id
    firstname_client = me.first_name
    username_client = f"@{me.username}" if me.username is not None else ""
    lastname_client = me.last_name if me.last_name is not None else ""

   
    messages = []
    messages_count = 0
    first_message_date = None
    last_message_date = None
    forward_sender = None
    try:
        for message in client.iter_messages(target_group):
            sender_id = message.sender_id if hasattr(message, 'sender_id') else None
            username = message.sender.username if hasattr(message.sender, 'username') else None
            first_name = message.sender.first_name if hasattr(message.sender, 'first_name') else None
            last_name = message.sender.last_name if hasattr(message.sender, 'last_name') else None
            message_time = message.date.astimezone(minsk_timezone).strftime('%d.%m.%Y %H:%M:%S')
            if first_message_date is None or message.date < first_message_date:
                first_message_date = message.date

            if last_message_date is None or message.date > last_message_date:
                last_message_date = message.date
                
            if message.sender_id == userid_client:
                sender_info = f"{firstname_client}:"
            else:
                sender_info = f"{first_name}:"

            forward_text = None
            is_forward = False
            if message.forward:
                is_forward = True
                forward_text = escape(message.text) if message.text else None
                forward_sender = get_forwarded_info(client, message) #Новая фишка
        
            reply_text = None
            if message.reply_to_msg_id:
                if message.reply_to_msg_id:
                    original_message = client.get_messages(target_group, ids=message.reply_to_msg_id)
                    if original_message:
                        reply_text = escape(original_message.text) if original_message.text else None
                    else:
                        reply_text = None
   
            reaction_info = ""
            reactions = message.reactions
            if reactions and reactions.recent_reactions:
                reaction_info = " ".join(reaction.reaction.emoticon for reaction in reactions.recent_reactions)

            media_type = None
            if message.media is not None:
                if isinstance(message.media, types.MessageMediaPhoto):
                    if selection in ['45', '450']:
                        # Загрузка фото в формате base64
                        photo_bytes = client.download_media(message.media.photo, file=BytesIO())
                        if photo_bytes:
                            image = Image.open(photo_bytes)
                            original_size = image.size
                            new_size = (original_size[0] // 2, original_size[1] // 2)
                            image = image.resize(new_size)
                            output = BytesIO()
                            image.save(output, format='JPEG', quality=70)
                            encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
                            image_data_url = f"data:image/jpeg;base64,{encoded_image}"
                            media_type = f'<img src="{image_data_url}" alt="Photo">'
                        else:
                            media_type = 'Photo'
                    else:
                            media_type = 'Photo'
                    
                elif isinstance(message.media, types.MessageMediaDocument):
                    for attribute in message.media.document.attributes:
                        if isinstance(attribute, types.DocumentAttributeFilename):
                            if selection == '450':
                                video_bytes = client.download_media(message.media.MessageMediaDocument, file=BytesIO())
                                #if video_bytes
                            
                            else:
                                document_name = attribute.file_name
                                media_type = f"Document: {document_name}"
                                break
                    if media_type is None:
                        media_type = 'Document (Photo, video, etc)'
                elif isinstance(message.media, types.MessageMediaWebPage):
                    media_type = 'WebPage'
                elif isinstance(message.media, types.MessageMediaContact):
                    media_type = 'Contact'
                elif isinstance(message.media, types.MessageMediaGeo):
                    media_type = 'Geo'
                elif isinstance(message.media, types.MessageMediaVenue):
                    media_type = 'Venue'
                elif isinstance(message.media, types.MessageMediaGame):
                    media_type = 'Game'
                elif isinstance(message.media, types.MessageMediaInvoice):
                    media_type = 'Invoice'
                elif isinstance(message.media, types.MessageMediaPoll):
                    media_type = 'Poll'
                elif isinstance(message.media, types.MessageMediaDice):
                    media_type = 'Dice'
                elif isinstance(message.media, types.MessageMediaPhotoExternal):
                    media_type = 'PhotoExternal'
                else:
                    media_type = 'Unknown'
            
            messages_count +=1
            messages.append({
                'time': message_time,
                'sender_info': sender_info,
                'reply_text': reply_text,
                'forward_text': forward_text, 
                'text': escape(message.text) if message.text else '',
                'reactions': reaction_info,
                'media_type': media_type,
                'sender_id': message.sender_id, 
                'is_forward': is_forward,
                'forward_sender': forward_sender
            })
    except Exception as e:
        messages.append({
            'time': '',
            'sender_info': 'Ошибка',
            'reply_text': None,
            'forward_text': None, 
            'text': f"Ошибка при получении переписки: {e}",
            'reactions': '',
            'media_type': '',
            'sender_id': None
        })
            

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template_user_messages.html')
    html_output = template.render(
        firstname_client=firstname_client,
        first_name=first_name,
        messages=messages,
        userid_client=userid_client,
        user_id=user_id,
        first_message_date=first_message_date.astimezone(minsk_timezone).strftime('%d.%m.%Y'),
        last_message_date=last_message_date.astimezone(minsk_timezone).strftime('%d.%m.%Y'),
        messages_count=messages_count
    )
    
    filename = f"{target_group}_private_messages.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_output)
    
    
    print(f"HTML-файл сохранен как '{filename}' и отправлен в бот")
