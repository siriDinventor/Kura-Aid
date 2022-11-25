from fastapi import FastAPI, Request, responses
import time
app = FastAPI()
fake_db = {
    "09032097223":
        {
            "LGA": "Oredo",
            "state": "Edo",
            "name": "",
            "phone": "902346829",
            "joined": 897643289,
            "history": [
                {
                    "date": 6781982376,
                    "complain": "",
                }
            ]
        },
}
locationDictionary = {
    "Edo": ["Oredo", "Ikpoba-Okha"]
}
HospitalDictionary = {
    "LGA": ["hb"]
}
def make_lga(p_response, lga_list, part = 0):
    i = 0
    if len(lga_list) < 8:
        j = 1
        for i in lga_list:
            p_response += f"{j}. {i}\n"
            j += 1
        return p_response 
def Hospital(LGA):
    LGA = fake_db.get(phone_Number["LGA"])
    hospitalList = HospitalDictionary.get(LGA)
    response = "CON These are the list of hospitals:"
    for i in hospitalList:
        response += f"{1}\n"
    return response
def getState(text, phone_number):
    is_exist = ""
    if text == "":
        return "CON will you type your state\nmy friend!"
    text = text.split("*")[-1]
    for i in locationDictionary:
        if str(text).casefold() == str(i).casefold():
            is_exist = i
    
    if is_exist:
        user = fake_db.get(phone_number)
        user.update({"state": is_exist})
        fake_db.update({str(phone_number): user})

        res = "CON Which LGA are you in?\n"
        loc = locationDictionary[is_exist]
        return make_lga(res, loc, 0)
    else:
        return "CON spell your State correctly"

def getLga(number, phone_number):
    if number == "":
        return "CON Please will you type your number\n"
    number = number.split("*")[-1]
    user = fake_db.get(phone_number)
    main_list = locationDictionary[user.get("state")]
    p = user["part"]
    if len(main_list) < int(number) and int(number) < 1:
        return "CON Please type your number\n"
    else:
        l = main_list[int(number) - 1]
        user = fake_db.get(phone_number)
        user.update({"LGA": l})
        fake_db.update({str(phone_number): user})
        response = "CON Welcome to Kura where you have access to quality health services\n"
        response += "1. Specialist\n"
        response += "2. Reminder \n"
        response += "3. Pharmacy \n"
        response += "4. Hospital \n"
        response += "5. Caretaker\n"
        return response
def unregisteredUser(text, phone):
    user = fake_db.get(phone)
    user.update({"name": text})
    fake_db.update({str(phone): user})
    return "CON Which State do you reside:"


@app.get("/test")
def check():
    return ('please work')


@app.post("/app", response_class=responses.PlainTextResponse)
async def index(request: Request):
    form = await request.form()
    session_id = form["sessionId"]
    serviceCode = form["serviceCode"]
    phone_number = form["phoneNumber"]
    text = form["text"]
    user = fake_db.get(phone_number)
    if user:
        if user["name"] == "":
            return unregisteredUser(text, phone_number)
        elif user["state"] == "":
            return getState(text, phone_number)
        elif user["LGA"] == "":
            return getLga(text, phone_number)
        else:
            s = text
            s_list = s.split("*")
            # e.g s_list = ['salman', '1']
            j = 0
            real_string = ""
            for i in s_list:
                if i.isdigit():
                    for k in s_list[j:]:
                        real_string += k + "*"
                        print(real_string)
                    # real_string = "".join(s_list[j:])
                    # print(real_string)

                    break
                j += 1
            text = real_string[:-1]

            # return f"END the text is {text}"

            if text == "":
                response = "CON Welcome to Kura where yo have access to quality health services\n"
                response += "1. Specialist \n"
                response += "2. Reminder \n"
                response += "3. Pharmacy \n"
                response += "4. Hospital \n"
                response += "5. Caretaker\n"
                return response
            elif text == "1":
                response = "END welldone you can read english"
                return response
            elif text == "2":
                response = "CON what type of reminder do you want?\n1. One time\n2. Repeat"
                return response
            elif text == "2*1":
                response = "CON what do you want to reminded off?.. type away"
            elif text == "2*2":
                response = "CON what do you want to reminded off?.. type away"
                return response
            elif text == "3":
                response = "Pharmacy"
            elif text == "4":
                return Hospital(LGA)
            elif text == "5":
                response = "Caretaker"
                return response
            else:
                return "Invalid Input"

    else:
        fake_db.update(
            {
                phone_number: {
                    "location": "",
                    "state": "",
                    "LGA": "",
                    "part": 0,
                    "name": "",
                    "phone": phone_number,
                    "joined": time.time(),
                    "history": [
                        {}
                    ]
                }}
        )
        return "CON please type your name"
