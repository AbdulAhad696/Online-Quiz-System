
from types import MethodDescriptorType
from typing import NamedTuple, Optional
from flask import Flask,request,render_template
app=Flask(__name__,template_folder="templates")

myfile=open("questions.txt","a")
myfile.close()
myfile=open("data.txt","a")
myfile.close()



class questions():
    ques=""
    optA=""
    optB=""
    optC=""
    optD=""
    ans=""
    radioname=""
    def __init__(self,question,optionA,optionB,optionC,optionD,answer):
        self.ques=question
        self.optA=optionA
        self.optB=optionB
        self.optC=optionC
        self.optD=optionD
        self.ans=answer


class students():
    def __init__(self,stdname,user,pass_word):
        self.name=stdname
        self.username=user
        self.password=pass_word
    name=""
    username=""
    password=""
    marks=0

student_list=[]
currentlyloggedin=""
##########################################################################

def login_verify(user,pass_word):
    if user=="admin":
        if pass_word=="anti_Proton13":
            return "adminmain.html"
        else:
            return "Invalid-login.html"
    else:
        myfile=open("data.txt","r")
        records=myfile.read().splitlines()
        userval=False
        passval=False
        for record in records:
            stringcount=0
            record_username=""
            record_pass=""
            while(record[stringcount]!=','):
                stringcount+=1
            stringcount+=1
            while(record[stringcount]!=','):
                record_username+=record[stringcount]
                stringcount+=1
            if(record_username==user):
                userval=True
                stringcount+=1
                while(record[stringcount]!=','):
                    record_pass+=record[stringcount]
                    stringcount+=1
                if(record_pass==pass_word):
                    passval=True
        
        if passval and userval:
            global currentlyloggedin
            currentlyloggedin=record_username
            myfile.close()
            return "studentmain.html"
        else:
            myfile.close()
            return "Invalid-login.html"

@app.route("/login-check",methods=['POST','GET'])
def checklogin():
    username=request.form['username']
    password=request.form['password']
    file=login_verify(username,password)
    return render_template(file)

@app.route("/")
def login():
    return render_template("login.html")
##########################################################################
@app.route("/signup")
def signup():
    return render_template("sign-up.html")

def V_user(user):
    verified=True
    myfile=open("data.txt","r")
    records=myfile.read().splitlines()
    
    for record in records:
        stringcount=0
        username=""
        while record[stringcount]!=',':
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            username+=record[stringcount]
            stringcount+=1
        if username==user:
            verified=False
    myfile.close()
    return verified

def V_pass(password):
    captrue=False
    num=False
    special=False
    if(len(password)>=8):
        for i in password:
            if(i.isupper()):
                captrue=True
            if(i.isdigit()):
                num=True
            if((ord(i)>=32 and ord(i)<=47) or (ord(i)>=58 and ord(i)<=64) or (ord(i)>=91 and ord(i)<=96) or (ord(i)>=123 and ord(i)<=126)):
                special=True
        if(captrue and num and special):
                return True
        else:
            return False
    else:
        return False

def savestd(stdname,user_name,password):
    student=students(stdname,user_name,password)
    student_list.append(student)
    myfile=open("data.txt","a")
    record=student.name+","+student.username+","+student.password+","+str(student.marks)
    print(record,file=myfile,sep="\n")
    myfile.close()

@app.route("/signupsave",methods=['POST','GET'])
def signup_save():
    stdname=request.form['stdname']
    user_name=request.form['username']
    password=request.form['password']
    confirm_pass=request.form['confirm-password']
    if confirm_pass==password:
        if V_user(user_name) and V_pass(password):
            savestd(stdname,user_name,password)
            return render_template("login.html")
        elif V_user==False:
            return render_template("invalid-user.html")
        elif V_pass==False:
            return render_template("invalid-pass.html")
    else:
        return render_template("Pass-not-match.html")

#####################################################################################
@app.route("/admin-success")
def admin_main():
    return render_template("adminmain.html")

######################################################################################

@app.route("/savequestion",methods=['POST','GET'])
def savequestion():
    myfile=open("questions.txt","a")
    question=request.form['question']
    optionA=request.form['optionA']
    optionB=request.form['optionB']
    optionC=request.form['optionC']
    optionD=request.form['optionD']
    answer=request.form['answer']
    record=question+","+optionA+","+optionB+","+optionC+","+optionD+","+answer
    print(record,file=myfile,sep="\n")  
    return render_template("adminmain.html")


@app.route("/quiz-edit")
def edit():
    return render_template("edit.html")

######################################################################################

def read_data():
    myfile=open("data.txt","r")
    records=myfile.read().splitlines()
    return records

def TurnToObjects(records,newstudent_list):
    for record in records:
        name=""
        Obtmarks=""
        username=""
        password=""
        stringcount=0
        while record[stringcount]!=',':
            name+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            username+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            password+=record[stringcount]
            stringcount+=1
        stringcount+=1
        student=students(name,username,password)
        while stringcount<len(record):
            Obtmarks+=record[stringcount]
            stringcount+=1
        
        student.marks=int(Obtmarks)
        newstudent_list.append(student)
    return newstudent_list
        
@app.route("/view")
def View_result():
    records=read_data()
    newstudent_list=[]
    newstudent_list=TurnToObjects(records,newstudent_list)
    
    return render_template("view.html",student_records=newstudent_list)
#######################################################################################
                        ##########ADMIN CODE FINISHED#############
#######################################################################################

def TurnQsToObjects(records,newquestion_list):
    loopcount=1
    for record in records:
        question=""
        optionA=""
        optionB=""
        optionC=""
        optionD=""
        answer=""
        stringcount=0
        radname=""
        
        while record[stringcount]!=',':
            question+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            optionA+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            optionB+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            optionC+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            optionD+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while stringcount<len(record):
            answer+=record[stringcount]
            stringcount+=1
        ques=questions(question,optionA,optionB,optionC,optionD,answer)
        radname="answer"+str(loopcount)
        ques.radioname=radname
        newquestion_list.append(ques)
        print(ques.radioname)
        loopcount+=1
    
    return newquestion_list

@app.route("/attempt-quiz")
def view_quiz():
    myfile=open("questions.txt","r")
    records=myfile.read().splitlines()
    newquestion_list=[]
    newquestion_list=TurnQsToObjects(records,newquestion_list)
    return render_template("viewquiz.html",question_records=newquestion_list)

def checkanswers(ans1,ans2,ans3):
    myfile=open("questions.txt","r")
    records=myfile.read().splitlines()
    mrks=0
    answer=[]
    for record in records: 
        ans=""
        stringcount=0
        commacount=0
        while commacount!=5:
            if record[stringcount]==',':
                commacount+=1
            stringcount+=1
        while stringcount<len(record):
            ans+=record[stringcount]
            stringcount+=1
        answer.append(ans)
        print(ans)
    ######calculating marks##########
    myfile.close()
    if answer[0]==ans1:
        if answer[1]==ans2:
            if answer[2]==ans3:
                mrks=30
            else:
                print("here 20")
                mrks=20
        elif answer[2]==ans3:
            mrks=20
        else:
            mrks=10
    elif answer[1]==ans2:
        if answer[2]==ans3:
            mrks=20
        else:
            mrks=10
    elif answer[2]==ans3:
        mrks=10
    else:
        mrks=0
    
    
    newfile=open("data.txt","r")
    stdrecords=newfile.read().splitlines()
    loopcount=0
    print(stdrecords)
    
    for record in stdrecords:
        name=""
        Obtmarks=""
        username=""
        password=""
        stringcount=0
        while record[stringcount]!=',':
            name+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            username+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            password+=record[stringcount]
            stringcount+=1
        stringcount+=1
        print(username)
        if currentlyloggedin==username:
            Obtmarks=str(mrks)
            rec=name+","+username+","+password+","+Obtmarks
            stdrecords[loopcount]=rec
        loopcount+=1
    newfile.close()
    newfile=open("data.txt","w")
    print(stdrecords)
    for record in stdrecords:
        print(record,file=newfile,sep="\n")
    newfile.close()
      
@app.route("/saveanswers",methods=['POST','GET'])
def save_answers():
    ans1=request.form.get('answer1')
    ans2=request.form.get('answer2')
    ans3=request.form.get('answer3')
    print(ans1,ans2,ans3)
    checkanswers(ans1,ans2,ans3)
    return render_template("studentmain.html")

@app.route("/viewresult")
def std_resultview():
    myfile=open("data.txt","r")
    records=myfile.read().splitlines()
    mrkstopass=0
    for record in records:
        username=""
        Obtmarks=""
        stringcount=0
        while record[stringcount]!=',':
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            username+=record[stringcount]
            stringcount+=1
        stringcount+=1
        while record[stringcount]!=',':
            stringcount+=1
        stringcount+=1
        while stringcount<len(record):
            Obtmarks+=record[stringcount]
            stringcount+=1
        if currentlyloggedin==username:
            mrkstopass=int(Obtmarks)
    
    return render_template("viewresult.html",marks=mrkstopass)




if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")