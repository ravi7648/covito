# <TwilioResponse>
#     <SMSMessage>
#         <Sid>SM1f0e8ae6ade43cb3c0ce4525424e404f</Sid>
#         <DateCreated>Fri, 13 Aug 2010 01:16:24 +0000</DateCreated>
#         <DateUpdated>Fri, 13 Aug 2010 01:16:24 +0000</DateUpdated>
#         <DateSent/>
#         <AccountSid>ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</AccountSid>
#         <To>+13455431221</To>
#         <From>+15104564545</From>
#         <Body>A Test Message</Body>
#         <Status>queued</Status>
#         <Flags>
#             <Flag>outbound</Flag>
#         </Flags>
#         <ApiVersion>2010-04-01</ApiVersion>
#         <Price/>
#         <Uri>
#             /2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SM1f0e8ae6ade43cb3c0ce4525424e404f
#         </Uri>
#     </SMSMessage>
# </TwilioResponse>
# {
#     "sid": "SM1f0e8ae6ade43cb3c0ce4525424e404f",
#     "date_created": "Fri, 13 Aug 2010 01:16:24 +0000",
#     "date_updated": "Fri, 13 Aug 2010 01:16:24 +0000",
#     "date_sent": null,
#     "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "to": "+15305431221",
#     "from": "+15104564545",
#     "body": "A Test Message",
#     "status": "queued",
#     "flags":["outbound"],
#     "api_version": "2010-04-01",
#     "price": null,
#     "uri": "\/2010-04-01\/Accounts\/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\/Messages\/SM1f0e8ae6ade43cb3c0ce4525424e404f.json"
# }
from covid import covid
import string
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    raw_sender = request.form.get('From')
    sender = raw_sender.split(':')


    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time) 
    greet = ""

    if current_time < "12:00:00":
        greet = "good morning"
    elif current_time < "16:00:00":
        greet = "good afternoon"
    elif current_time > "16:00:00":
        greet = "good evening"
    else:
        greet = "Warm wishes"

    sender_name = {"+917759039884":"Ravi", "+918578947225":"Sweta", "+916299664603":"Abhishek", "+919182784044":"Bharathi"}
    # Create reply
    resp = MessagingResponse()
    
    if msg.lower().startswith('hi'):
        resp.message("Hi {}, {}. \nThis is *Covito : The Covid-19 Bot* specially built for sending report of the COVID-19 situation".format(sender_name[sender[1]], greet))
        resp.message('''How can I help you? These are few keywords through which you can control me properly. Don't worry {}, I am not case sensitive. If I found these keywords in your message I will try my best to understand you 😇\n1. Hi\n2. Ok\n3. Report\n4. Country: Country name\n5. Bye'''.format(sender_name[sender[1]]))
    elif msg.lower().startswith('bye'):
        resp.message("Bye {}, Nice to talk with you".format(sender_name[sender[1]]))
        if current_time > "20:00:00":
            resp.message("Good night !")
    elif msg.lower().find("report") != -1:
        rep = covid.covidSummary()
        a, b, c, d, e, f = rep
        resp.message("------------------------------\nCOVID19 report:\n------------------------------\n*New Confirmed:* {}\n*Total Confirmed:* {}\n*New Deaths:* {}\n*Total Deaths:* {}\n*New Recovered:* {}\n*Total Recovered:* {}\n------------------------------\nIf you want report for your country, please type your country name starts with keyword *Country* followed with ':' and your country name.".format(a, b, c, d, e, f))
    elif msg.lower().startswith("country:"):
        try:
            country = msg.split(':')
            rep = covid.covidCountry(country[1].lower().strip())
            a, b, c, d, e, f, g = rep
            g = g.lower().split("t")
            g = g[1].lower().split("z")
            g = g[0].split(':')
            g = g[0]+":"+g[1]
            capital = country[1].title().strip()
            resp.message("------------------------------\nCOVID19 report in {}:\n------------------------------\n*New Confirmed:* {}\n*Total Confirmed:* {}\n*New Deaths:* {}\n*Total Deaths:* {}\n*New Recovered:* {}\n*Total Recovered:* {}\n------------------------------\nRecent update at {}".format(capital, a, b, c, d, e, f, g))
            resp.message("------------------------------\n🏠 *STAY HOME. SAVE LIVES 👨‍👩‍👧‍👦* \n------------------------------\n1. *STAY* home\n2. *KEEP* a safe distance\n3. *WASH* hands often\n4. *COVER* your cough\n5. *SICK?* call the helpline\n------------------------------\nHelpline Number: +91-11-23978046\nToll Free : 1075\nHelpline Email ID : ncov2019@gov.in")
        except:
            resp.message("Oops! I caught with some errors. 😕")
    elif msg.lower().startswith("ok"):
        resp.message("😊")
    else:
        resp.message("Sorry {}! I am still incomplete".format(sender_name[sender[1]]))
    # print(msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)