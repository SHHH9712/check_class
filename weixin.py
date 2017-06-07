from wxpy import *


bot = Bot(cache_path = True, console_qr=2)
bot.enable_puid()
f1 = ensure_one(bot.friends().search('BotSHHH'))
f1.send('new_session')

# 
# puids = dict()
# for i in bot.friends():
#     print(i.name, i.puid)
#     puids[i.puid] = i.name
    
print(bot.self.puid)



@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('格式： add+课号（add 888888）.\n回复-课表 查看当前课程状态。')
    
@bot.register(Friend, TEXT)
def reply_text(msg): #add 20099
    n_msg = msg.text.split()
    if msg.text == "课表":
        reply = file2reply(msg.sender.puid)
        for mail in reply:
            msg.sender.send(mail)
    if msg.text == "格式":
        return '格式： add+课号（add 888888）.'
    if msg.text == 'mmma':
#         puids = save_puid()
        classes_content = reply_statue()
#         for i in puids:
#             bot.self.send(str(i))
        for i in classes_content:
            bot.self.send(i)
    if n_msg[0].upper() == 'ADD':
        code = n_msg[1]
        puid = msg.sender.puid
        add_Lec(code, puid)
        return f'吧{code}加入到{puid}的列表中.'
    
def file2reply(puid):
    result = []
    infile = open('classes.txt')
    for line in infile.readlines():
        if puid in line.split():
            result.append(line.split()[1]+' ('+line.split()[0]+'): '+line.split()[3])
    infile.close()
    return result

# def save_puid():
#     result = []
#     outfile = open('puid_cab.txt', 'w')
#     for friend in bot.friends():
#         puid = str(friend.puid)
#         name = str(friend.name)
#         result.append(tuple([puid, name]))
#         outfile.write(f'{puid}:{name}')
#     outfile.close()
#     return result
    
def reply_statue():
    result = []
    infile = open('classes.txt')
    for line in infile.readlines():
        result.append(' '.join(line.split()))
    infile.close()
    return result
    
def send_notify(code, name, puid, statue):
    print('push notification' + puid)
    ensure_one(bot.friends().search(puid = puid)).send(f'{name}: {code}  状态变更为{statue}')
    
def send_msg(puid, msg):
    ensure_one(bot.friends().search(puid = puid)).send(msg)
    
def add_Lec(code, puid):
#     Loads.append(Lec(code, puid))
    outfile = open('classes.txt', 'a')
    outfile.write(code +' NULL '+ puid +' NULL\n')
    outfile.close()
    send_msg(bot.self.puid, f'add {code} for {puid}')
    
# embed()