import requests
import json
from bs4 import BeautifulSoup
from pushover import init, Client

url = 'https://www.reg.uci.edu/perl/WebSoc'
head = {'Content-Type':'application/x-www-form-urlencoded'}
post = 'Submit=Display+Web+Results&YearTerm=2017-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=AC+ENG&CourseNum=&Division=ANY&CourseCodes=&InstrName=MINNIS&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='


while True:
    r = requests.post(url, data=post, headers = head)

    soup = BeautifulSoup(r.text, 'html.parser')

    list_class = soup.find_all(attrs = {'nowrap':"nowrap"})

    for i in list_class:
        if 'OPEN' in i:
            init('afiq2ntpokxubmzt61j9ii5kf2w4o9')
            Client('uuij88hm2xkrk17brz1enbiuyko6ph').send_message('Hello!', title = 'HEllo')

