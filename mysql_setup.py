from config import mydb


mycursor = mydb.cursor()

# sql = "DROP TABLE MEMBER"
# mycursor.execute(sql)

#Create Member table
mycursor.execute("CREATE TABLE MEMBER (id INT AUTO_INCREMENT PRIMARY KEY,First_Name VARCHAR(255),Last_Name VARCHAR(255),\
Gender VARCHAR(255),Date_of_Birth VARCHAR(255),Email VARCHAR(255))")

#Read data.csv
with open('data.csv','r') as csv_file:
    lines = csv_file.readlines()

#Insert into mysql
sql = "INSERT INTO MEMBER (First_Name, Last_Name, Gender, Date_of_Birth, Email) VALUES (%s, %s, %s, %s, %s)"
for line in lines:
    data = line.split(',')
    val = (str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]))
    mycursor.execute(sql, val)
    mydb.commit()

print("********** Successfully trans data to mysql database ***********")

