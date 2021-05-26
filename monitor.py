import os
from time import sleep
import requests
import telebot
from decouple import config
from telebot.types import Message
import json
import datetime

API_KEY = config('API_KEY')
today=datetime.date.today()
STATE_ID = config ('STATE_ID')
DISTRICT_URL = config('DISTRICT_URL')

BROWSER_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"

bot = telebot.TeleBot(API_KEY)
response = ""

while (True):
    try:
        resp=requests.get(DISTRICT_URL.format(STATE_ID,today.strftime("%d-%m-%Y")),headers=BROWSER_HEADER)
    except Exception as e:
        bot.send_message(659261445, str(e))
    data_json = json.loads(resp.text)
    if resp.status_code == 200:
        for center in data_json["centers"]:
            session=center["sessions"][0]
            if str(center["block_name"])=="Ambernath" or str(center["block_name"])=="Kalyan Dombivali Municipal Corporation" or str(center["block_name"])=="Ulhasnagar Municipal Corporation":
                if session["available_capacity"] > 0:
                    response = ( f"Center Name:\t\t\t"+ str(center["name"]) + '\n'
                    + "Address:\t\t\t"+ str(center["address"]) + '\n'
                    + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
                    + "Pincode:\t\t\t"+ str(center["pincode"]) + '\n'
                    + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
                    + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
                    + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
                    + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
                    + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
                    + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n\n' 
                    + "CoWin: https://selfregistration.cowin.gov.in" + '\n')
                    bot.send_message(659261445, response)
                    response = ""
    sleep(37)

bot.polling()