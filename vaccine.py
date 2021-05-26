# Developer : Sagar B

import requests
import json
import datetime

# url="https://cdn-api.co-vin.in/api/v2/admin/location/states"
# url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"



today=datetime.date.today()
# pincode="421201"
state_id=392

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(state_id,today.strftime("%d-%m-%Y"))


print(url)
browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

resp=requests.get(url,headers=browser_header)

# print(resp.text)

data_json = json.loads(resp.text)

# # print(data_json)
# # print(type(state_resp.text))
# # print(type(data_json))

for center in data_json["centers"]:
    session=center["sessions"][0]
    if str(center["block_name"])=="Ambernath" or str(center["block_name"])=="Kalyan Dombivali Municipal Corporation" or str(center["block_name"])=="Ulhasnagar Municipal Corporation":
        if session["available_capacity_dose1"] > 0:
            print("-----------------------------------------------------------------------" + '\n'
            + "Center Name:\t\t\t"+ str(center["name"]) + '\n'
            + "Address:\t\t\t"+ str(center["address"]) + '\n'
            + "Block name:\t\t\t"+ str(center["block_name"]) + '\n'
            + "Fees:\t\t\t\t"+ str(center["fee_type"]) + '\n'
            + "Total capacity(Dose 1 + 2):\t" + str(session["available_capacity"]) + '\n'
            + "Minimum Age limit:\t\t" + str(session["min_age_limit"]) +'\n'
            + "Vaccine:\t\t\t" + str(session["vaccine"]) +'\n'
            + "Available capacity dose 1 :\t" + str(session["available_capacity_dose1"]) + '\n'
            + "Available capacity dose 2 :\t" + str(session["available_capacity_dose2"]) + '\n')
