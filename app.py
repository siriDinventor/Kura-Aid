from fastapi import FastAPI, Request, responses
import time
app = FastAPI()
fake_db = {
    "09032097223":
        {
            "location": "Ikpoba Okha, Edo Satte",
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


def location(text, phone_number):
    print(text)
    loc = locationDictionary.get(text, None)
    print(loc)
    response = "CON Which LGA are you in?\n"
    s = text
    s_list = s.split("*")
    if s_list[0] == fake_db.get(phone_number)["name"]:
        loc = locationDictionary.get(s_list[1])
        j = 1
        for i in loc:
            response += f"{j}. {i}" + "\n"
            j += 1
            print(response)
        return response
    if loc == None and text == "":
        return "CON please provide your state"
    else:
        for i in loc:
            response += i + "\n"
            print(response)
        return response
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
        elif user["location"] == "":
            return location(text, phone_number)
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
                response = "reminder"
                return response
            elif text == "3":
                response = "Pharmacy"
            elif text == "4":
                response = "Hospital"
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
                    "name": "",
                    "phone": phone_number,
                    "joined": time.time(),
                    "history": [
                        {}
                    ]
                }}
        )
        return "CON please type your name"
