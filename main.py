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

#Version 4: Simple Message with full name 
@app.route("/api/v4/simple_messege_fullname", methods=['POST'])
def simple_messege_fullname():
    sql = "SELECT * FROM MEMBER WHERE Date_of_Birth LIKE '%" + now_date + "%\'"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    data = {}
    for row in myresult:
        email = str(row[5])
        message = {}
        message["title"] = 'Subject: Happy birthday!'
        message["content"] = 'Happy birthday, dear ' + str(row[1]) + ", " + str(row[2]) + '!'
        msg = Message(
            subject="Happy birthday!",
            recipients=[email],
            html=json.dumps(message)
        )
        data[row[0]] = message
        mail.send(msg)

    res = json.dumps(data)
    return res

#Version 4: Simple Message but database changes 
@app.route("/api/v4/simple_messege_mongodb", methods=['POST'])
def simple_messege_mongodb(): 
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["MEMBER"]
    myquery = { "Date_of_Birth": { "$regex":now_date} }
    mydoc = mycol.find(myquery)

    data = {}
    index = 0
    for row in mydoc:
        email = str(row['Email'])
        message = {}
        message["title"] = 'Subject: Happy birthday!'
        message["content"] = 'Happy birthday, dear ' + str(row['First_Name']) + '!'

        msg = Message(
            subject='Subject: Happy birthday!',
            recipients=[email],
            html= json.dumps(message)
        )
        data[index] = message
        index = index + 1
        mail.send(msg)
        
    res = json.dumps(data)
    return res


if __name__ == '__main__':
    app.run()