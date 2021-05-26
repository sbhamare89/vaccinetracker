# Developer : Sagar B

import os
import requests
import telebot
from decouple import config
from telebot.types import Message
import json
import datetime
import re

API_KEY = config('API_KEY')
today=datetime.date.today()
pincode="421201"
STATE_ID = config ('STATE_ID')
DISTRICT_URL = config('DISTRICT_URL')
PINCODE_URL = config('PINCODE_URL')

BROWSER_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['help'])
def send_greetings(message):
    response = '''
    Welcome to Covid Vaccine tracker bot.

    This bot used to send you regular updates for available vaccine slots.
    Below commands used to get data :

        check <pincode> => This will give you list of vaccine centers with avalable doses.
    '''
    bot.send_message(message.chat.id, response)

def user_message(message):
    request = message.text.split()
    if len(request) < 1: # or request[0].lower() not in "check":
        return False
    else:
        return True

@bot.message_handler(func=user_message)
def check_vaccine_slots(message):
    
    if len(message.text.split()) == 2:    
        STRING_1 = message.text.split()[0]
        STRING_2 = message.text.split()[1]
    else:
        STRING_1 = message.text.split()[0]
        STRING_2 = ""
    obj = re.compile(regex)
    n = ""
    def isValidPincode(n):
        if n == '':
            return False
        value = re.match(obj, n)
        if value is None:
            return False
        else:
            return True
    if str(STRING_1.lower()) == "check" and isValidPincode(STRING_2) == True:
        response = ""
        try:
            resp=requests.get(PINCODE_URL.format(STRING_2,today.strftime("%d-%m-%Y")),headers=BROWSER_HEADER)
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
        data_json = json.loads(resp.text)
        if resp.status_code == 200:
            FLAG = False
            for center in data_json["centers"]:
                index = 0
                if len(center["sessions"]) > 1:
                    for session in center["sessions"]:
#                        session=center["sessions"][index]
                        if int(session["available_capacity"]) > 0:
                            if str(center["fee_type"]) == "Free":
                                response = ( f"Center Name:\t\t\t"+ str(center["name"]) + '\n'
                                + "Address:\t\t\t"+ str(center["address"]) + '\n'
                                + "Date :\t\t\t" + str(session['date']) + '\n'
                                + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
                                + "Pincode:\t\t\t"+ str(center["pincode"]) + '\n'
                                + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
                                + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
                                + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
                                + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
                                + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
                                + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n\n'
                                + "CoWin: https://selfregistration.cowin.gov.in" + '\n')
                                bot.send_message(message.chat.id, response)
                                response = ""
                                FLAG = True
                            else:
                                vaccine_fee = center["vaccine_fees"][0]
                                response = ( f"Center Name:\t\t\t"+ str(center["name"]) + '\n'
                                + "Address:\t\t\t"+ str(center["address"]) + '\n'
                                + "Date :\t\t\t" + str(session['date']) + '\n'
                                + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
                                + "Pincode:\t\t\t"+ str(center["pincode"]) + '\n'
                                + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
                                + "Amount :\t\t\t\t"+ str(vaccine_fee["fee"]) + '\n'
                                + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
                                + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
                                + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
                                + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
                                + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n\n'
                                + "CoWin: https://selfregistration.cowin.gov.in" + '\n')
                                bot.send_message(message.chat.id, response)
                                response = ""
                                FLAG = True

                        index += 1
                else:
                    session=center["sessions"][0]
                    if int(session["available_capacity"]) > 0:
                        if str(center["fee_type"]) == "Free":
                            response = ( f"Center Name:\t\t\t"+ str(center["name"]) + '\n'
                            + "Address:\t\t\t"+ str(center["address"]) + '\n'
                            + "Date :\t\t\t" + str(session['date']) + '\n'
                            + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
                            + "Pincode:\t\t\t"+ str(center["pincode"]) + '\n'
                            + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
                            + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
                            + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
                            + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
                            + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
                            + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n\n'
                            + "CoWin: https://selfregistration.cowin.gov.in" + '\n')
                            bot.send_message(message.chat.id, response)
                            response = ""
                            FLAG = True
                        else:
                            vaccine_fee = center["vaccine_fees"][0]
                            response = ( f"Center Name:\t\t\t"+ str(center["name"]) + '\n'
                            + "Address:\t\t\t"+ str(center["address"]) + '\n'
                            + "Date :\t\t\t" + str(session['date']) + '\n'
                            + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
                            + "Pincode:\t\t\t"+ str(center["pincode"]) + '\n'
                            + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
                            + "Amount :\t\t\t\t"+ str(vaccine_fee["fee"]) + '\n'
                            + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
                            + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
                            + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
                            + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
                            + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n\n'
                            + "CoWin: https://selfregistration.cowin.gov.in" + '\n')
                            bot.send_message(message.chat.id, response)
                            response = ""
                            FLAG = True




            if FLAG == True:
                return
            else:
                bot.send_message(message.chat.id, "Currently no slots avaiable for pincode entered : {}".format(STRING_2))

            FLAG = False                      
        else:
            bot.send_message(message.chat.id, "Error while fetching data, try again after 10 seconds.")


    elif str(STRING_1.lower()) == "myarea":
        response = ""
        try:
            resp=requests.get(DISTRICT_URL.format(STATE_ID,today.strftime("%d-%m-%Y")),headers=BROWSER_HEADER)
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
        data_json = json.loads(resp.text)
        if resp.status_code == 200:
            FLAG = False
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
                        bot.send_message(message.chat.id, response)
                        bot.send_message(504351192, response)
                        response = ""
                        FLAG = True

            if FLAG == True:
                return
            else:
                bot.send_message(message.chat.id, "Currently no slots avaiable for pincode entered : 421306")

            FLAG = False                      
                        
        else:
            bot.send_message(message.chat.id, "Error while fetching data, try again after 10 seconds.")

    elif str(STRING_1) == "help":
        response ='''
        Welcome to Covid Vaccine tracker bot.

        This bot gets data from Govt Setu API and presents to you, feel free to share.

        help = to get help
        check <pincode> = to get available vaccine centers
        '''
        bot.send_message(message.chat.id, response)
    
    else:
        bot.send_message(message.chat.id, "Wrong input format,use :\n\tcheck <pincode>")







@bot.message_handler(func=user_message)
def check_vaccine_slots(message):
    pass

bot.polling()