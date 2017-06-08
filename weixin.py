from wxpy import *


bot = Bot(cache_path = True, console_qr=-2)
bot.enable_puid()
#bot.friends().search('SHHH')[0].send('new_session')

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
    new_friend.send('吧你想报的课注册在这里,就能在状态改变时收到通知\n注册示例：add+88888\n如果想看自己注册了哪些课，回复：课表')
    
@bot.register(Friend, TEXT)
def reply_text(msg): #add 20099
    n_msg = msg.text.split('+')
    if msg.text == "课表":
        reply = file2reply(msg.sender.puid)
        for mail in reply:
            msg.sender.send(mail)
    elif msg.text == "格式":
        msg.sender.send('吧你想报的课注册在这里,就能在状态改变时收到通知\n注册示例：add+88888\n如果想看自己注册了哪些课，回复：课表')
    elif msg.text == 'mmma':
        classes_content = reply_statue()
        for i in classes_content:
            msg.sender.send(i)
    elif n_msg[0].upper() == 'ADD':
        code = n_msg[1]
        puid = msg.sender.puid
        add_Lec(code, puid)
        return 'Success!注册可能需要几秒钟\n课程状态改变后会给你发微信\n如果想看自己注册了哪些课，回复：课表'
    elif n_msg[0].upper() == 'DEL':
        code = n_msg[1]
        puid = msg.sender.puid
        outfile = open('del.txt', 'a')
        outfile.write(code + ' ' + puid + '\n')
        outfile.close()
        return 'Success!删除可能需要几秒钟\n如果想看自己注册了哪些课，回复：课表'
    elif msg.text =='cleanall':
        clean('classes.txt')
        return 'Success'
    else:
        msg.sender.send('吧你想报的课注册在这里,就能在状态改变时收到通知\n注册示例：add+88888\n如果想看自己注册了哪些课，回复：课表')

    
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
    infile = open('classes.txt', 'r')
    for line in infile.readlines():
        result.append(' '.join(line.split()))
    infile.close()
    return result
    
def send_notify(code, name, puid1, statue):
    print('push notification to: ' + puid)
    try:
        bot.friends().search(puid = puid1)[0].send('{}: {}  状态变更为{}'.format(name, code, statue))
    except:
        pass
    
def send_msg(puid1, msg):
    try:
        bot.friends().search(puid = puid1)[0].send(msg)
    except:
        pass
    
def add_Lec(code, puid):
#     Loads.append(Lec(code, puid))
    outfile = open('class2.txt', 'a')
    outfile.write(code +' NULL '+ puid +' NULL\n')
    outfile.close()

def clean(f):
    file = open(f, 'w')
    file.write('')
    file.close()
    
#    chat = bot.friends().search('shhh')
#    for i in chat:
#        send_msg(i.puid, 'add {} for {}'.format(code, puid))
    
# embed()
