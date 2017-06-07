import requests
import json
import smtplib
import time
from datetime import datetime
from bs4 import BeautifulSoup
from pushover import init, Client
from collections import namedtuple
import weixin

url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post_1 = 'Submit=Display+Web+Results&YearTerm=2017-92&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes='
post_2 = '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='
self_puid = 'a4578010'

check_gap = 2 # Unit = s
Loads = []

class Lec:
    def __init__(self, code, puid):
        self._code = code
        self._puid = puid
        self._course_name = self.pull_statue()[0]
        self.statue = self.pull_statue()[1]
            
            
    def pull_statue(self):
        post = post_1 + self._code + post_2
        r = requests.post(url, data=post, headers = head)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        list_class = soup.find_all(attrs = {'nowrap':"nowrap"})

        names = []
        for i in list_class[0].strings:
            names.append(i)
        real_name = ' '.join(names[0].string.split())
#         print([real_name, list_class[-1].string])
        return [real_name, list_class[-1].string]
        
    def update_check(self):
#         new_statue = self.pull_statue()[1]
        file = open('test.txt')
        new_statue = file.read()
        file.close()
        print(self.statue, new_statue)
        if new_statue != self.statue:
            self.statue = new_statue
            self.notify()
        else:
            self.statue = new_statue
        
    def notify(self):
        weixin.send_notify(self._code, self._course_name, self._puid, self.statue)
    
def read_file():
    infile = open('classes.txt')
    for line in infile.readlines():
        if line != '':
            c = line.split()
            Loads.append(Lec(c[0], c[1]))
    infile.close()
    
def add_from_file():
    infile = open('classes.txt')
    for line in infile.readlines():
        if line != '':
            c = line.split()
            for i in Loads:
                if i._puid != c[1] and i._code != c[0]:
                    Loads.append(Lec(c[0], c[1]))
                    break
    infile.close()
            
def add_Lec(code, puid):
#     Loads.append(Lec(code, puid))
    outfile = open('classes.txt', 'a')
    outfile.write(code +' '+ puid +'\n')
    outfile.close()
    weixin.send_msg(self_puid, '\n'.join([f"{x._course_name} - {x._code}\n{x._puid} - {x.statue}" for x in Loads]))




def mainloop():
    read_file()
    while True:
        for item in Loads:
            item.update_check()
        print('-'*20)
        time.sleep(check_gap)
         
if __name__ == '__main__':
    mainloop()
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         