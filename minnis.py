import requests
import json
import time
from bs4 import BeautifulSoup
from pushover import init, Client
from collections import namedtuple

#Class = namedtuple('Class', ['pre_name', 'name', 'code', 'teacher', 'time', 'last_statue', 'now_statue', 'i'])

url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post_1 = 'Submit=Display+Web+Results&YearTerm=2017-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=ALL&CourseNum=&Division=ANY&CourseCodes='
post_2 = '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='


class Lec:
    def __init__(self, code, pre_name):      
        self._pre_name = pre_name
        self._code = code
        
        nns = self.get_info()
        
        self._name = nns[0]
        self._last_statue = nns[1]
        self._now_statue = nns[1]

    def get_info(self):
        post = post_1 + self._code + post_2
        r = requests.post(url, data=post, headers = head)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        list_class = soup.find_all(attrs = {'nowrap':"nowrap"})
        return [list_class[0].string, list_class[-1].string]

    def open_notify(self):
        init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
        Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('NOW {}'.format(self._now_statue), title = '{} {}'.format(self._pre_name, self._code))

    def update(self):
        update_data = self.get_info()
        self._last_statue = self._now_statue
        self._now_statue = update_data[1]
        if self._last_statue != self._now_statue:
            self.open_notify()
            # print('push: {}'.format(self._code))
        self.open_notify()
        print('class: {}, statue is :{}'.format(self._code, self._now_statue))

    def push_statue(self):
        self.open_notify()
        # print('regular push: {}'.format(self._code))
        

def read_files():
    codes = []
    r = open('classes.txt')
    for i in r.readlines():
        codes.append([i.split()[0], i.split()[1]])
    r.close()
    return codes
    

def main_loop():
    REPORT_TIME = 0
    while True:
        contents = read_files()
        loads = []
        for content in contents:
            loads.append(Lec(content[0], content[1]))

        for load in loads:
            load.update()

        if REPORT_TIME == 60:
            for load in loads:
                load.push_statue()
                
        REPORT_TIME += 1
        time.sleep(10)

        
if __name__ == '__main__':
    main_loop()
    

'''
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
        

