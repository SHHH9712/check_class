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
    new_friend.send('把你想监控的课code注册在这里，在OPEN之后会自动通知你\n格式： add+课号（add 888888）.\n回复：课表 查看当前课程状态。')
    
@bot.register(Friend, TEXT)
def reply_text(msg): #add 20099
    n_msg = msg.text.split('+')
    if msg.text == "课表":
        reply = file2reply(msg.sender.puid)
        for mail in reply:
            msg.sender.send(mail)
    elif msg.text == "格式":
        msg.sender.send('格式: add+课号\n(add加号888888).\n回复：课表，查看监控列表')
    elif msg.text == 'mmma':
        classes_content = reply_statue()
        for i in classes_content:
            msg.sender.send(i)
    elif n_msg[0].upper() == 'ADD':
        code = n_msg[1]
        puid = msg.sender.puid
        add_Lec(code, puid)
        return 'Success!\n课程状态改变后会给你发微信\n回复：课表，查看监控列表'
    elif msg.text =='cleanall':
        clean()
        return 'Success'
    else:
        msg.sender.send('把你想监控的课code注册在这里，在OPEN之后会自动通知你\n回复：格式，查看格式.\n回复：课表，查看监控列表')

    
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
    print('push notification to: ' + puid)
    ensure_one(bot.friends().search(puid = puid)).send('{}: {}  状态变更为{}'.format(name, code, statue))
    
def send_msg(puid, msg):
    ensure_one(bot.friends().search(puid = puid)).send(msg)
    
def add_Lec(code, puid):
#     Loads.append(Lec(code, puid))
    outfile = open('classes.txt', 'a')
    outfile.write(code +' NULL '+ puid +' NULL\n')
    outfile.close()

def clean():
    file = open('classes.txt', 'w')
    file.write('')
    file.close()
    
#    chat = bot.friends().search('shhh')
#    for i in chat:
#        send_msg(i.puid, 'add {} for {}'.format(code, puid))
    
# embed()
