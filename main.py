from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from config import mydb
import datetime
import json
from dict2xml import dict2xml
import pymongo


app = Flask(__name__)

# EMAIL Config
app.config.update(
    DEBUG=False,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('admin','xxxxxxxxxx@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='xxxxxxxxx@gmail.com',
    MAIL_PASSWORD='xxxxxxxxxxx'
)
mail = Mail(app)

#Standardize the format of Today's date (x/xx)
now_month = str(datetime.datetime.now())[5:7]
now_day = str(datetime.datetime.now())[8:11]
now_date = str(int(now_month)) + "/" + str(int(now_day))
print("Today is " + now_date)
now_year = int(str(datetime.datetime.now())[:4])

#Version 2: Tailer-made Message for different gender 
@app.route("/api/v2/messege_for_diff_gender", methods=['POST'])
def messege_for_diff_gender():
    try:
        sql = "SELECT * FROM MEMBER WHERE Date_of_Birth LIKE '%" + now_date + "%\'"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        data = {}
        for row in myresult:
            email = str(row[5])

            message = {}
            message["title"] = 'Subject: Happy birthday! '
            if str(row[3]) == 'Male':
                message["content"] = 'Happy birthday, dear ' + str(row[1]) + '!\n ' +\
                'We offer special discount 20% off for the following items: \n ' +\
                'White Wine, iPhone X'

            else:
                message["content"] = 'Happy birthday, dear ' + str(row[1]) + '!\n' +\
                'We offer special discount 50% off for the following items: \n '+\
                'Cosmetic, LV Handbags'
            msg = Message(
                subject = 'Subject: Happy birthday!',
                recipients = [email],
                html = json.dumps(message)
            )
            data[row[0]] = message
            mail.send(msg)
        
        res = json.dumps(data)
        return res

    except Exception as e:
        print(e)
        res2 = jsonify("Fail")
        res2.status_code = 400
        return res2

if __name__ == '__main__':
    app.run()