from hangups.ui.utils import get_conv_name

from hangupsbot.utils import text_to_segments
from hangupsbot.commands import command

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

@command.register
def 동측(bot, event, *args):
    """동측 식당 메뉴를 출력합니다.
사용법:
/bot 동측 아침
/bot 동측 점심
/bot 동측 저녁
    """
    #URL------------------------------------------------------------------------------------#
    kaist_url = 'http://www.kaist.ac.kr'
    food_url = kaist_url + '/_prog/fodlst/index.php'\
            + '?site_dvs_cd=kr&menu_dvs_cd=050303&dvs_cd=fclt&dvs_cd=east1&stt_dt=%s&site_dvs='
    #---------------------------------------------------------------------------------------#

    #getCurrentTime-------------------------------------------------------------------------#
    select = args[0] 
    date = datetime.now()
    if(select == "아침"):
        current_time_index = 0
        current_time_str = "Moring"
    elif(select == "점심"):
        current_time_index = 1
        current_time_str = "Afternoon"
    elif(select == "저녁"):
        current_time_index = 2
        current_time_str = "Evening"
    else:
        current_time_index = -1
    #---------------------------------------------------------------------------------------#

    if(current_time_index is not -1):
        #getFoodMenu------------------------------------------------------------------------#
        menu = ""
        html = urlopen( food_url % str(date.date()))
        webpage = html.read()
        soup = BeautifulSoup(webpage)
        tdList = soup.findAll("td")
        anchor = '&gt;'

        for line in tdList[current_time_index]:
            if(len(line) > 1):
                if(line.find(anchor) != -1):
                    menu += "< %s >\n" % current_time_str
                else:
                    menu += line.strip() + "\n"
        #-----------------------------------------------------------------------------------#

        menu = menu.replace('&quot;', '\"')
        menu = menu.replace('&lt;', '<')
        menu = menu.replace('&gt;', '>')
        menu = menu.replace('&amp;', '&')

        yield from event.conv.send_message(text_to_segments(menu))
    else:
        yield from event.conv.send_message(text_to_segments('사용법: /bot 동측 아침'))

@command.register
def 서측(bot, event, *args):
    """서측 식당 메뉴를 출력합니다.
사용법:
/bot 서측 아침
/bot 서측 점심
/bot 서측 저녁
    """
    #URL------------------------------------------------------------------------------------#
    kaist_url = 'http://www.kaist.ac.kr'
    food_url = kaist_url + '/_prog/fodlst/index.php'\
            + '?site_dvs_cd=kr&menu_dvs_cd=050303&dvs_cd=fclt&dvs_cd=west&stt_dt=%s&site_dvs='
    #---------------------------------------------------------------------------------------#

    #getCurrentTime-------------------------------------------------------------------------#
    select = args[0] 
    date = datetime.now()
    if(select == "아침"):
        current_time_index = 0
        current_time_str = "Moring"
    elif(select == "점심"):
        current_time_index = 1
        current_time_str = "Afternoon"
    elif(select == "저녁"):
        current_time_index = 2
        current_time_str = "Evening"
    else:
        current_time_index = -1
    #---------------------------------------------------------------------------------------#

    if(current_time_index is not -1):
        #getFoodMenu------------------------------------------------------------------------#
        menu = ""
        html = urlopen( food_url % str(date.date()))
        webpage = html.read()
        soup = BeautifulSoup(webpage)
        tdList = soup.findAll("td")
        anchor = '&gt;'

        for line in tdList[current_time_index]:
            if(len(line) > 1):
                if(line.find(anchor) != -1):
                    menu += "< %s >\n" % current_time_str
                else:
                    menu += line.strip() + "\n"
        #-----------------------------------------------------------------------------------#

        menu = menu.replace('&quot;', '\"')
        menu = menu.replace('&lt;', '<')
        menu = menu.replace('&gt;', '>')
        menu = menu.replace('&amp;', '&')
        menu = menu.replace('\"', '')

        yield from event.conv.send_message(text_to_segments(menu))
    else:
        yield from event.conv.send_message(text_to_segments('사용법: /bot 서측 아침'))
