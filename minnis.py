import requests
import json
import time
from bs4 import BeautifulSoup
from pushover import init, Client
from collections import namedtuple

Class = namedtuple('Class', ['pre_name', 'name', 'code', 'teacher', 'time', 'statue'])

url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post_1 = 'Submit=Display+Web+Results&YearTerm=2017-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=ALL&CourseNum=&Division=ANY&CourseCodes='
post_2 = '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

def get_info(code):
    post = post_1 + code[0] + post_2
    r = requests.post(url, data=post, headers = head)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_class = soup.find_all(attrs = {'nowrap':"nowrap"})
    return Class(code[1], list_class[0].string, list_class[1].string, list_class[5].string, list_class[6].string, list_class[-1].string)

def open_notify(pre_name, code, statue):
    init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
    Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('NOW {}'.format(statue), title = '{} {}'.format(pre_name, code))

def find_content(st):
    pass

def check_by_time():
    pass

def read_files():
    codes = []
    r = open('classes.txt')
    for i in r.readlines():
        codes.append([i.split()[0], i.split()[1]])
    return codes
    r.close()

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
        time.sleep(60)
        
        
if __name__ == '__main__':
    main_loop()
    
