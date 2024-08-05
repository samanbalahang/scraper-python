import telebot
import time
import requests
import pymysql.cursors


# تست
#bot_token = '1290577640:AAGBDmPGSCNqSLOldot0PP3fMraKSLnqdj0'
#bot_chatID = '@testgitapython'


# گیتا
# bot_token = '1207877459:AAHUo1MscOWiAlvlHBWF_kkTkGz4itLo7rE'
# bot_chatID = '@gitarealestatefile'
connection = pymysql.connect(host='localhost',user='mojtaba',password='1234',db='extractdata')


def telegram_bot_sendtext(bot_message):
    
    
    bot_token = '1290577640:AAGBDmPGSCNqSLOldot0PP3fMraKSLnqdj0'
    bot_chatID = '@testgitapython'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    
    
# with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM `divar`"
#         cursor.execute(sql)
#         result = cursor.fetchone()
        
# telegram_bot_sendtext("قیمت: "+result[13])
telegram_bot_sendtext("salam")

connection.close()
 
#+result[3]+result[5]+result[6]+result[7]+result[8]+result[9]+result[13]


#view rawtelegram_bot_sendtext.py hosted with ❤ by GitHub


