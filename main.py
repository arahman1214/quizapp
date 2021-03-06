from flask import Flask, render_template, request,redirect
import math,copy,random,csv
import json
import time
import speedtest
import logging
from requests.models import Response


app = Flask(__name__)
# ...

logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

jsonData = {}

def csvToJson():
    csvFilePath = 'StudentDetails.csv'
    data = {}
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            logger.info(rows)
            data.update(rows)
    return csvReader

csvToJson()

Question_bank1 = {
 #Format is 'question':[options]
 'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
 'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
 'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
 'Colosseum':['Rome','Milan','Bari','Bologna'],
 'Christ the Redeemer':['Rio de Janeiro','Natal','Olinda','Betim']
}

Question_bank2 = {
 #Format is 'question':[options]
 'Taj M':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
 'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
 'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
 'Colosseum':['Rome','Milan','Bari','Bologna'],
}

original_questions1={}
original_questions2={}
datalist=[]
c=0
l=[]
while True:
    if (c >=5):
        break
    x=random.choice(list(Question_bank1.keys()))
    if x not in l:
        l.append(x)
        original_questions1[x]=Question_bank1[x]
        #print(x)
        #print(original_questions[x])
        c = c + 1
questions1 = copy.deepcopy(original_questions1)

c1=0
l1=[]

while True:
    if (c1 >=5):
        break
    x=random.choice(list(Question_bank2.keys()))
    if x not in l1:
        l1.append(x)
        original_questions2[x]=Question_bank2[x]
        #print(x)
        #print(original_questions[x])
        c1 = c1 + 1
questions2 = copy.deepcopy(original_questions2)

def shuffle(q):
 """
 This function is for shuffling
 the dictionary elements.
 """
 selected_keys = []
 i = 0
 while i < len(q):
  current_selection = random.choice(list(q.keys()))
  if current_selection not in selected_keys:
   selected_keys.append(current_selection)
   i = i+1
 return selected_keys


@app.route('/', methods=['post', 'get'])
def login():
    message1 = ''
    message2=''
    message=''
    c=0
    companyName = ''

    if request.method == 'POST':
        name = request.form.get('name')  # access the data inside
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        if request.form.get('companyName'):
            companyName = request.form.get('companyName')

        if name == '' or  age == '' or  phone == '' or  email == '' or  address == '':
            message = "Please Fill all the details"

        else:
            message = "Thank You"
            if int(age)>10:
                message1=message1+" "+name+" Please select the Quiz2"
                message=message+" "+name+" "+"Please select the Quiz2"
            else:
                message2 = message2 +" "+name+" Please select the Quiz1"
                message = message + " " + name + " " + "Please select the Quiz1"

        datalist.append(name)
        datalist.append(age)
        datalist.append(phone)
        datalist.append(email)
        datalist.append(address)
        datalist.append(companyName)
        logger.info(datalist)
    return render_template('SaveDetails.html',message=message,message1=message1,message2=message2)


#no button for this----admin shld access with ur "/adminpanel/"
@app.route('/adminpanel/', methods=['post', 'get'])
def adminpanel():
    return render_template('adminpanel.html')


@app.route('/admin_details/', methods=['post', 'get'])
def admin_details():
    msg = 'hi'
    print("sssss")
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username=="gaurav" and password=="gaurav":
            return render_template('add_questions.html')




@app.route('/quiz1/')
def quiz1():
 questions_shuffled = shuffle(questions1)
 for i in questions1.keys():
     random.shuffle(questions1[i])
 return render_template('quiz1.html', q=questions_shuffled, o=questions1)

@app.route('/quiz1_answers/', methods=['POST'])
def quiz1_answers():
 correct = 0
 for i in questions1.keys():
  answered = request.form[i]
  if original_questions1[i][0] == answered:
   correct = correct+1
 datalist.append(correct)
 save_internet_speed()
 datasave(datalist)
 return render_template('thankyou.html')


def datasave(datalist):
    fieldnames = ['name', 'age','phone','email','address','score', 'Company Name', 'speed']

    with open(datalist[5]+'.csv', 'a') as inFile:
        writer = csv.DictWriter(inFile, fieldnames=fieldnames)
        writer.writerow({'name': datalist[0], 'age': datalist[1],'phone':datalist[2],'email':datalist[3],'address':datalist[4],'score':datalist[6]
                         , 'Company Name': datalist[5], 'speed': datalist[7]})
        jsonData.update({'name': datalist[0], 'age': datalist[1],'phone':datalist[2],'email':datalist[3],'address':datalist[4],'score':datalist[6]
                         , 'Company Name': datalist[5], 'speed': datalist[7]})
    logger.info(jsonData)

@app.route('/quiz2/')
def quiz2():
 questions_shuffled = shuffle(questions2)
 for i in questions2.keys():
  random.shuffle(questions2[i])

 logger.info("quesions shuffled: ", questions_shuffled)
 logger.info("quesions2: ", questions2)
 return render_template('quiz2.html', q=questions_shuffled, o=questions2)

@app.route('/quiz2_answers/', methods=['POST'])
def quiz2_answers():
 correct = 0
 for i in questions2.keys():
  answered = request.form[i]
  if original_questions2[i][0] == answered:
   correct = correct+1
 datalist.append(correct)
 save_internet_speed()
 datasave(datalist)
 return render_template('thankyou.html')


def save_internet_speed():
    speed = speedtest.Speedtest()
    speed_new = str(speed.download())
    speed_new1 = speed_new.split('.')[0]
    final_speed = ''
    if len(speed_new1) == 8:
        final_speed = final_speed + speed_new1[0] + speed_new1[1]
    else:
        final_speed = final_speed + speed_new1[0]

    datalist.append(final_speed)


@app.route('/addQuestions/', methods=['POST'])
def addQuestions():
    message = ''
    if request.method == "POST":
        optionsList = []
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        age = request.form.get('optradio')
        #ageGroup = request.form.get('ageGroup')
        optionsList.extend({option1, option2, option3, option4})
        logger.info(optionsList)

        if age == "0":
            Question_bank1.update({question: optionsList})
            message = "question added successfully for less than 10"
            logger.info(Question_bank1)
            logger.info(message)
            return render_template('add_questions.html', message=message)
        else:
            Question_bank2.update({question: optionsList})
            message = "question added successfully for greater than 10"
            return render_template('add_questions.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)