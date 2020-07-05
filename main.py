from flask import Flask, render_template, request
import math,copy,random,csv
from requests.models import Response





app = Flask(__name__)
# ...


original_questions = {
 #Format is 'question':[options]
 'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
 'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
 'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
 'Colosseum':['Rome','Milan','Bari','Bologna'],
 'Christ the Redeemer':['Rio de Janeiro','Natal','Olinda','Betim']
}


original_questions1={}
datalist=[]
c=0
l=[]
while True:
    if (c >=5):
        break
    x=random.choice(list(original_questions.keys()))
    if x not in l:
        l.append(x)
        original_questions1[x]=original_questions[x]
        #print(x)
        #print(original_questions[x])
        c = c + 1
questions = copy.deepcopy(original_questions1)

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
    message = ''
    c=0
    if request.method == 'POST':
        name = request.form.get('name')  # access the data inside
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        if name == '' or  age == '' or  phone == '' or  email == '' or  address == '':
            message = "Please Fill all the details"

        else:
            message = "Thank You"
            if int(age)>10:
                message=message+" "+name+" Please select the Quiz2"
            else:
                message = message +" "+name+" Please select the Quiz1"

        datalist.append(name)
        datalist.append(age)
        datalist.append(phone)
        datalist.append(email)
        datalist.append(address)
    return render_template('SaveDetails.html',message=message)




@app.route('/admin/', methods=['post', 'get'])
def admin():
    msg = 'hi'
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username=="gaurav" and password=="gaurav":
            return render_template('add_questions.html')
        else:
            msg="please check the details2"
            return render_template('SaveDetails.html',message=password)



@app.route('/quiz1/')
def quiz1():
 questions_shuffled = shuffle(questions)
 for i in questions.keys():
     random.shuffle(questions[i])
 return render_template('quiz1.html', q=questions_shuffled, o=questions)

@app.route('/quiz1_answers/', methods=['POST'])
def quiz1_answers():
 correct = 0
 for i in questions.keys():
  answered = request.form[i]
  if original_questions1[i][0] == answered:
   correct = correct+1
 datalist.append(correct)
 datasave(datalist)
 return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'


def datasave(datalist):
    fieldnames = ['name', 'age','phone','email','address','score']

    with open('StudentDetails.csv', 'a') as inFile:
        writer = csv.DictWriter(inFile, fieldnames=fieldnames)


        writer.writerow({'name': datalist[0], 'age': datalist[1],'phone':datalist[2],'email':datalist[3],'address':datalist[4],'score':datalist[5]})


@app.route('/quiz2/')
def quiz2():
 questions_shuffled = shuffle(questions)
 for i in questions.keys():
  random.shuffle(questions[i])
  return render_template('quiz2.html', q=questions_shuffled, o=questions)

@app.route('/quiz2_answers/', methods=['POST'])
def quiz2_answers():
 correct = 0
 for i in questions.keys():
  answered = request.form[i]
  if original_questions1[i][0] == answered:
   correct = correct+1
 datalist.append(correct)
 datasave(datalist)
 return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'




if __name__ == '__main__':
 app.run(debug=True)