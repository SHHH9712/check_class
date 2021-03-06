import requests
import json
import smtplib
import time
from datetime import datetime
from bs4 import BeautifulSoup
from pushover import init, Client
from collections import namedtuple
import weixin

class LecError: pass

url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post_1 = 'Submit=Display+Web+Results&YearTerm=2017-92&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes='
post_2 = '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

check_gap = 2 # Unit = s
Loads = []

def file2list(f):
    result = []
    infile = open(f, 'r')
    for line in infile.readlines():
        if line != '':
            try:
                result.append(Lec(line.split()[0], line.split()[1], line.split()[2], line.split()[3]))
            except:
                print('improt error')
                #weixin.send_msg(line.split()[2], '{}这是节假课'.format(line.split()[0]))
    infile.close()
    return result

def load2file(loads):
    outfile = open('classes.txt', 'w')
    for i in loads:
        outfile.write("{} {} {} {}\n".format(i.code, i.course_name, i.puid, i.statue))
    outfile.close()

class Lec:
    def __init__(self, code, c_name, puid, statue):
        self.code = code
        self.puid = puid
        comb = self.pull_statue()
        
        if c_name == 'NULL':
            self.course_name = comb[0]
        else:
            try:
                self.course_name = c_name
            except:
                pass        
        if statue == 'NULL':
            self.statue = comb[1]
        else:
            try:
                self.statue = statue
            except:
                pass
        #print(self.code, self.course_name, self.puid, self.statue)

        #self.notify()
            
            
    def pull_statue(self):
        post = post_1 + self.code + post_2
        r = requests.post(url, data=post, headers = head)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        list_class = soup.find_all(attrs = {'nowrap':"nowrap"})

        names = []
        for i in list_class[0].strings:
            names.append(i)
        real_name = ' '.join(names[0].string.split())
#         print([real_name, list_class[-1].string])
        return [''.join(real_name.split()), list_class[-1].string]
        
    def update_check(self):
        new_statue = self.pull_statue()[1]
#         file = open('test.txt')
#         new_statue = file.read()
#         file.close()
        
        #print(self.code, self.course_name, self.statue, new_statue, self.puid) #test statue check
        
        if new_statue != self.statue:
            self.statue = new_statue
            self.notify()
        else:
            self.statue = new_statue
        
    def notify(self):
        try:
            weixin.send_notify(self.code, self.course_name, self.puid, self.statue)
        except:
            pass

def clean(f):
    file = open(f, 'w')
    file.write('')
    file.close()

def del_dulicate(load):
    result = []
    for i in load:
        switch = True
        for i2 in result:
            if i.puid == i2.puid and i.code == i2.code:
                switch = False
        if switch == True:
            result.append(i)
    return result
    
def del_lec(load, f):
    minus = []
    file = open(f, 'r')
    for i in file.readlines():
        minus.append(i.split())
    file.close()
    clean(f)
    result = []
    for i in load:
        switch = True
        for i2 in minus:
            if i.puid == i2[1] and i.code == i2[0]:
                switch = False
        if switch == True:
            result.append(i)
    return result
        
def mainloop():
    while True:
        Loads = []
        Loads = file2list('classes.txt')
        loa = file2list('class2.txt')
        clean('class2.txt')
        Load = Loads + loa
        Load2 = del_dulicate(Load)
        Loads = del_lec(Load2, 'del.txt')
        for item in Loads:
            item.update_check()
        load2file(Loads)
        print('-'*20)
        time.sleep(check_gap)
    
if __name__ == '__main__':
    mainloop()
