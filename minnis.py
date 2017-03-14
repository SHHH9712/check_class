import requests
import json
import smtplib
import time
from datetime import datetime
from bs4 import BeautifulSoup
from pushover import init, Client
from collections import namedtuple

#Class = namedtuple('Class', ['pre_name', 'name', 'code', 'teacher', 'time', 'last_statue', 'now_statue', 'i'])

sender = 'mailbotalex7@gmail.com'
url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post_1 = 'Submit=Display+Web+Results&YearTerm=2017-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=ALL&CourseNum=&Division=ANY&CourseCodes='
post_2 = '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='


Check_gap = 40  # Unit = s
Report_gap = 80  # Unit = check_gaps


class Lec:
    def __init__(self, code, user_name, mail):      
        self._user_name = user_name
        self._mail = mail
        self._code = code
        
        nns = self.get_info()
        
        self._name = nns[0]
        self._time = datetime.now().strftime('%H:%M:%S')
        self._last_statue = nns[1]
        self._now_statue = nns[1]

    def get_info(self):
        post = post_1 + self._code + post_2
        r = requests.post(url, data=post, headers = head)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        list_class = soup.find_all(attrs = {'nowrap':"nowrap"})
        '''
        time = 0
        for i in list_class:
            for m in i.strings:
                print('{}: {}'.format(time, m))
                time+=1
        print(list_class[11].string)
        '''
        names = []
        for i in list_class[0].strings:
            names.append(i)
        real_name = ' '.join(names[0].string.split())
        return [real_name, list_class[-1].string]

    def open_notify(self):
        init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
        Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('NOW {}'.format(self._now_statue), title = '{} {}'.format(self._name, self._code))

    def update(self):
        update_data = self.get_info()
        self._last_statue = self._now_statue
        self._now_statue = update_data[1]
        self._date = datetime.now().strftime('%H:%M:%S')
        if str(self._last_statue) != str(self._now_statue):
            self.open_notify()
            postman(self)
            # print('push: {}'.format(self._code))
        print('{:13} [{}] | {:10} | {:5} => {:5} | {}'.format(self._name, self._code, self._user_name, self._last_statue, self._now_statue, self._time))
        #postman(self)

    def push_statue(self):
        self.open_notify()
        
        # print('regular push: {}'.format(self._code))
        

def read_files():
    codes = []
    r = open('classes.txt')
    for i in r.readlines():
        if i != '':
            codes.append([i.split()[0], i.split()[1], i.split()[2]])
    r.close()
    return codes
    

def postman(lec):
    To = [lec._mail, 'shhh9712@gmail.com']
    
    subject = 'Your class {} [{}] statue has changed!'.format(lec._name, lec._code)
    main = 'Hi {}!\n Your class: {} [{}] statue has changed statue \n     |--FROM: {} \n     |--TO: {} \n     |--AT:   {}\n\nFrom MailbotAlex :)'.format(lec._user_name, lec._name, lec._code, lec._last_statue, lec._now_statue, lec._time)

    # print(subject)
    # print(main)

    body = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\n{}".format(sender, To, subject, main)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('mailbotalex7@gmail.com', 'neverknowmypwd')
        server.sendmail(sender, To, body)
        server.close()
        print('sent success!')
    except:
        print('SENT FAIL!')

def send_statue_mail(loads):
    print('sending statue_mail.....')
    
    To = ['mailbotalex7@gmail.com']
    
    subject = 'ALL STATUE UPDATE'
    main = ''
    for lec in loads:
        main += '{} [{}]\n    |--Statue: {} => {} \n    |--Last_update: {}\n'.format(lec._name, lec._code, lec._last_statue, lec._now_statue, lec._time)
    
    body = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\n{}".format(sender, To, subject, main)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('mailbotalex7@gmail.com', 'neverknowmypwd')
        server.sendmail(sender, To, body)
        server.close()
        print('sent success!')
    except:
        print('SENT FAIL!')
 
def send_statue_noti(loads):
    OPEN = 0
    FULL = 0
    WAIT = 0
    for load in loads:
        if load._now_statue == 'OPEN':
            OPEN += 1
        if load._now_statue == 'FULL':
            FULL += 1
        if load._now_statue == 'Waitl':
            WAIT += 1
    print(OPEN, FULL, WAIT)
    init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
    Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('Open:{} Full:{} Wait:{}'.format(OPEN, FULL, WAIT) ,title = 'RUNNING!')

def timestamp():
    pass

def main_loop():
    REPORT_TIME = 0
    while True:
        contents = read_files()
        loads = []
        for content in contents:
            loads.append(Lec(content[0], content[1], content[2]))

        print('Update {} ------------------------'.format(REPORT_TIME))
        for load in loads:
            try:
                load.update()
            except:
                pass
        print('')
        
        if REPORT_TIME ==0:
            send_statue_mail(loads)
            send_statue_noti(loads)
        
        if REPORT_TIME == Report_gap:
            REPORT_TIME = 0
                
        REPORT_TIME += 1
        time.sleep(Check_gap)


if __name__ == '__main__':
    main_loop()
    

'''

     
def notify_running(OPEN, FULL, WAIT):
    init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
    Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message(''.format(OPEN, FULL, WAIT) ,title = 'Server still running!')

def open_notify(pre_name, code, statue):
    init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
    Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('NOW {}'.format(statue), title = '{} {}'.format(pre_name, code))

def find_content(st):
    pass

def check_by_time():
    pass




def main_loop():
    i = 0
    REPORT_TIME = 0
    now_statue = ''
    while True:
        PUSH_LIST = []  
        for code in read_files():
            content = get_info(code)
            last_statue = now_statue
            now_statue = get_info(code).statue
            print(last_statue, now_statue, i)
            i += 1
            if last_statue != now_statue and i > 1:
                open_notify(content.pre_name, content.code, content.statue)
            PUSH_LIST.append([content.pre_name, content.code, content.statue])  
        for push in PUSH_LIST:
            print('{}: {}, is now {}'.format(push[0], push[1], push[2]))
        if REPORT_TIME == 60:
            for push in PUSH_LIST:
                open_notify(push[0], push[1], push[2])
            REPORT_TIME = 0
        REPORT_TIME += 1
        time.sleep(5)

def main_loop():
    loads = []
    REPORT_TIME = 0
    while True:
        codes = read_files()
        for code in codes:
            loads.append(get_info(code))
            
        for load in loads:
            load = load._replace(last_statue = load.now_statue)
            load = load._replace(now_statue = get_info(load.code).now_statue)
            load = load._replace(i = load.i+1)
            if load.last_statue != load.now_statue and i > 1:
                open_notify(load.pre_name, load.code, load.now_statue)

        if REPORT_TIME == 60:
            for push in PUSH_LIST:
                open_notify(push[0], push[1], push[2])
            REPORT_TIME = 0
        REPORT_TIME += 1

        time.sleep(5)
'''       
        

