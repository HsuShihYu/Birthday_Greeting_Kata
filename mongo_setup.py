import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["MEMBER"]

mycol.drop() 

#Read data.csv
with open('data.csv','r') as csv_file:
    lines = csv_file.readlines()

#Insert data into mongodb
for line in lines:
    data = line.split(',')
    mydict = { "First_Name": str(data[1]), "Last_Name": str(data[2]), "Gender": str(data[3]),\
    "Date_of_Birth": str(data[4]),"Email": str(data[5])}
    x = mycol.insert_one(mydict)


for x in mycol.find():
    print(x)

print("Data.csv successfully trans to mongoDB")