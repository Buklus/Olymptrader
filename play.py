from pyvirtualdisplay import Display
from selenium import webdriver
import time, sys, pickle
from selenium.webdriver.common.keys import Keys

import telegram, requests, json, sys, random

telegram_token = "754942247:AAG8gXODpV5nG6LOUApghhgWlxABJK9fUIc"

kingsley_telegram_id = "553991636"

def send_telegram_message(user_id, message):
    api_url = "https://api.telegram.org/bot{}/".format("754942247:AAG8gXODpV5nG6LOUApghhgWlxABJK9fUIc")
    
    params = {'chat_id': user_id, 'text': message}
    method = 'sendMessage'
    
    resp = requests.post(api_url + method, params)
    
    return resp

def time_reached( to_check="06:00" ):
    #strftime format: '05:04:53 12/14/18 UTC'
    struct_time = time.strftime('%X %x %Z')
    hour = struct_time.split()[0].split(":")[0]
    minute = struct_time.split()[0].split(":")[1]
    
    #If passed time(hour):
    if hour > to_check.split(":")[0]:
        return True
    
    #Check if passed/reached time(minute):
    elif hour == to_check.split(":")[0]:
        if minute >= to_check.split(":")[1]:
            return True
        else:
            return False
    
    else:
        return False
		
while not time_reached( to_check="4:16" ):
	time.sleep(10)
	send_telegram_message(kingsley_telegram_id, "Random " + str( random.random() ))