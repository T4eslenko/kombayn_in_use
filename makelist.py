def print_channel_lists(openchannels, closechannels, openchats, closechats):
    print()
    print("\033[95mОткрытые КАНАЛЫ:\033[0m")
    openchannel_list = []
    oc = 1
    for openchannel in openchannels:
        owner = " (Владелец)" if openchannel.creator else ""
        admin = " (Администратор)" if openchannel.admin_rights is not None else ""
        openchannel_list.append(f"{oc} - {openchannel.title} \033[93m[{openchannel.participants_count}]\033[0m\033[91m {owner} {admin}\033[0m ID:{openchannel.id} \033[94m@{openchannel.username}\033[0m")
        oc += 1
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
    print_pages(closechat_list, 25)

