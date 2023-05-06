#BCSF19A005
from random import random

from flask import Flask, render_template ,request, make_response,session
from User_Validation import UserValidation
from Classes import User, ClassObject, EnrollmentObject
from DBHandler import DataBaseHandler
import random


handler = DataBaseHandler("cmsrdsdatabase.cbkhtbowrv8m.eu-north-1.rds.amazonaws.com", "admin", 'user12345', "classroommanagementsystem")
#handler = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")

def generateClassId(unique):
    chars = "bdfhjlnprtvxz"
    str = ""
    value = ""

    for str in range(5):
        value = value + random.choice(chars)
    return value




myapp1 = Flask(__name__)

myapp1.secret_key="XYZ12345" #password

def validationLogin(name1,email1,pwd1):
    v=UserValidation()
    if v.validateName(name1)==True and v.validateEmail(email1)==True and v.validatePassword(pwd1)==True:
        return True
    return False

def checkUserAlreadyExist(acctype,email):
    try:
       # handler = DataBaseHandler("cmsrdsdatabase.cbkhtbowrv8m.eu-north-1.rds.amazonaws.com", "admin", 'user12345', "classroommanagementsystem")
        #handler = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")
        return handler.checkTeacherStdExist(acctype,email)
    except Exception as e:
        print(str(e))


@myapp1.route('/')
def test():
    return render_template("Welcome.html")


#It will show all teachers and student data in sepearte table
@myapp1.route('/showAllUsers')
def showAllUsers():
    try:
        data1 = handler.getStudents()
        data2=handler.getTeachers()
        return render_template("loginadmin.html",data1=data1,data2=data2)
    except Exception as e:
        print(str(e))

#signUp router
@myapp1.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email=request.form["email"]
        nm=request.form["nm"]
        pwd=request.form["pwd"]
        acctype=request.form["acctype"]
    else:
        email = request.args.get("email")
        nm = request.args.get("nm")
        pwd = request.args.get("pwd")
        acctype = request.args.get("acctype")


    if email==None and pwd==None and acctype==None and nm==None:
        return render_template("signup.html")

    login = False
    flag1=checkUserAlreadyExist(acctype,email)
    if validationLogin(nm,email,pwd)==True and flag1==False:
        login=True
    print("flag= ",flag1)

    if login== True:
        user1=User(nm,email,pwd,acctype)
        try:
            handler.addUser(user1)

        except Exception as e:
            print(str(e))

        if acctype=="Teacher":
            return render_template("loginteacher.html", name=nm)
        elif acctype=="Student":
            return render_template("loginstd.html", name=nm)
        else:
            return render_template("admin.html", name=nm)
    else:
        if flag1==True:
            return render_template("signup.html", error="User Already Exist!!")
        else:
            return render_template("signup.html",error="Invalid Credentials!!" )


#Login router

@myapp1.route("/loginUser", methods=["GET", "POST"])
def loginUser():
    try:
        if request.method == "POST":
            email = request.form["email"]
            pwd = request.form["pwd"]
            acctype = request.form["acctype"]
        else:
            email = request.args.get("email")
            pwd = request.args.get("pwd")
            acctype = request.args.get("acctype")

        if email == None and pwd == None and acctype == None:
            return render_template("loginUser.html")

        login = False

        user1 = User()
        user1.email = email
        user1.password = pwd
        user1.acc_type = acctype

        flag = False
        try:
            flag1 = handler.checkUserExist(user1)
            flag2 = handler.checkUserAccountDisable(user1)
        except Exception as e:
            print(str(e))
        else:

            if flag1 == True and flag2 == False:
                login = True
            if login == True:
                if acctype != "Student":
                    if acctype == "Teacher":
                        resp = make_response(render_template("loginteacher.html", name="Teacher"))
                    else:
                        resp = make_response(render_template("admin.html"))

                    print("setting response")
                    resp.set_cookie("uemail", email)
                    resp.set_cookie("uacctype", acctype)
                    return resp

                else:
                    session["uemail"] = email
                    session["upwd"] = pwd
                    session["uacctype"] = acctype
                    return render_template("loginstd.html", name="Student")
            else:
                if flag2 == True:
                    return render_template("loginUser.html", error="Your Account is Locked/Bocked!!")
                else:
                    return render_template("loginUser.html", error="Invalid Credentials!!")

            return render_template("loginUser.html", error="Login Failed!!")
    except Exception as e:
        print("Exception Occur",str(e))
        return render_template("loginUser.html", error="Login1 Failed!!")

@myapp1.route("/logintech")
def loginteach():
    email1 = request.cookies.get("uemail")
    acctype1 = request.cookies.get("uacctype")
    if email1 == None and acctype1 == None:
        return render_template("loginUser.html", errormsg="Please First Login to use this feature")
    return render_template("loginteacher.html", name="Teacher")

@myapp1.route("/createclassroom",methods=["POST","GET"])
def createClassroom():
    email1 = request.cookies.get("uemail")
    acctype1 = request.cookies.get("uacctype")
    if email1!=None and acctype1!=None:
        return render_template("classRoomForm.html")
    else:
        return render_template("loginUser.html", errormsg="Please First Login to use this feature")


@myapp1.route("/createclassroom_",methods=["POST","GET"])
def createclassroom_():
    try:
        email1 = request.cookies.get("uemail")
        acctype1 = request.cookies.get("uacctype")
        if email1 == None and acctype1 == None:
            return render_template("loginUser.html", errormsg="Please First Login to use this feature")

        if request.method=="POST":
            cname = request.form["cname"]
        else:
            cname = request.args.get("cname")

        email1 = request.cookies.get("uemail")
        acctype1 = request.cookies.get("uacctype")

        user1 =User("",email1,"",acctype1)

        idtech=handler.getId(user1)


        unique = set()
        classID = generateClassId(unique)
        IdList = handler.fetchIDs("Teacher", classID)
        if len(IdList) == 0:
            status = False
            while status == False:
                unique = set()
                Class_Id = generateClassId(unique)
                status = handler.checkClassID("Teacher", Class_Id)
                if status == True:
                    classroom1 = ClassObject()
                    classroom1.classId = Class_Id
                    classroom1.className = cname
                    classroom1.TeacherId = idtech
                    idList = str(idtech).split("_")
                    classroom1.TeacherNo = idList[1]
                    handler.addClassroom(classroom1)
                else:
                    status = False
            return render_template("loginteacher.html",msg="Class Room Created Successfully!!")
        else:
            return render_template("loginteacher.html",msg="Class Room Already Exist!")

        return render_template("classRoomForm.html")

    except Exception as e:
        print("Class Creation Failed ", str(e))
        return render_template("loginteacher.html", msg="Class Creation Failed ")

@myapp1.route("/addstudent") #methods=["POST","GET"]
def addstudent():
    email1 = request.cookies.get("uemail")
    acctype1 = request.cookies.get("uacctype")
    if email1 != None and acctype1 != None:
        return render_template("addStd.html")
    else:
        return render_template("loginUser.html", errormsg="Please First Login to use this feature")

@myapp1.route("/addstudent_",methods=["POST","GET"]) #methods=["POST","GET"]
def addstudent_():
    try:
        email1 = request.cookies.get("uemail")
        acctype1 = request.cookies.get("uacctype")
        if email1 == None and acctype1 == None:
            return render_template("loginUser.html", errormsg="Please First Login to use this feature")


        if request.method=="POST":
            cid = request.form["cid"]
            stdid=  request.form["stdid"]
        else:
            cid = request.args.get("cid")
            stdid=request.args.get("stdid")

        user1 =User("",email1,"",acctype1)

        idList = str(stdid).split("_")
        stdid1 = idList[0]
        stdno1 = idList[1]

        idtech=handler.getId(user1)
        enr=EnrollmentObject(cid,stdid1,stdno1,idtech)
        handler.addToClassroom(enr)
        return render_template("loginteacher.html", msg="Student Successfully!!")
    except Exception as e:
        print("Class Creation Failed ", str(e))
        return render_template("loginteacher.html", msg="Failed ")


@myapp1.route("/showallclassroom")
def showallclassroom():
    try:
        email1 = request.cookies.get("uemail")
        acctype1 = request.cookies.get("uacctype")

        if email1 == None and acctype1 == None:
            return render_template("loginUser.html", errormsg="Please First Login to use this feature")

        user1 = User("", email1, "", acctype1)
        idtech = handler.getId(user1)

        list1=handler.fetchClsIDs(acctype1,idtech)
        if list1!=None:
            return render_template("ShowClassrooms.html", data=list1)
        else:
            return render_template("ShowClassrooms.html", error="No Classroom")
    except Exception as e:
        print(str(e))
        return render_template("loginteacher.html", msg="Failed2 ")

@myapp1.route("/logoutTech")
def logoutTech():
    try:
        email1 = request.cookies.get("uemail")
        acctype1 = request.cookies.get("uacctype")
        if email1 == None and acctype1 == None:
            return render_template("loginUser.html", errormsg="Please First Login to use this feature")

        res=make_response(render_template("loginUser.html"))
        res.delete_cookie("uemail")
        res.delete_cookie("uacctype")

        res.set_cookie("uemail", max_age=0)
        res.set_cookie("uacctype", max_age=0)
        return res

        return res
    except Exception as e:
        print(str(e))

@myapp1.route("/loginStd")
def loginStd():
    email1 = session.get("uemail")
    pwd1 = session.get("upwd")
    acctype1 = session.get("uacctype")
    print(email1, pwd1, acctype1)

    if email1 == None and pwd1 == None and acctype1 == None:
        return render_template("loginUser.html", errormsg="Please First Login to use this feature")

    return render_template("loginstd.html")

@myapp1.route("/joinclassroom")
def joinClass():
    email1=session.get("uemail")
    pwd1=session.get("upwd")
    acctype1=session.get("uacctype")

    if email1 != None and acctype1 != None and pwd1!=None:
        return render_template("joinClass.html")

    else:
        return render_template("loginUser.html", errormsg="Please First Login to use this feature")

@myapp1.route("/joinclassroom_",methods=["POST","GET"])
def joinClass_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")
        acctype1 = session.get("uacctype")

        if email1 == None and pwd1 == None and acctype1 == None:
            return render_template("loginUser.html", errormsg="Please First Login to use this feature")

        if request.method=="POST":
            cid = request.form["cid"]
            tid=  request.form["tid"]
        else:
            cid = request.args.get("cid")
            tid=request.args.get("tid")

        userstd = User("", email1, "", acctype1)


        idstd = handler.getId(userstd)
        idList = str(idstd).split("_")
        stdid1=idList[0]
        stdno1 = idList[1]

        enr = EnrollmentObject(cid, idstd, stdno1, tid)
        handler.addToClassroom(enr)
        return render_template("joinClass.html", msg="Student join Successfully!!")

    except Exception as e:
        print(str(e))
        return render_template("loginStd.html",error ="Failed joining")


@myapp1.route("/showallclassroomStd")
def showllAllStd():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")
        acctype1 = session.get("uacctype")

        if email1 == None and pwd1 == None and acctype1 == None:
            return render_template("loginUser.html", error=True, errormsg="Please First Login to use this feature")

        user1 = User("", email1, "", acctype1)
        idtech = handler.getId(user1)

        list1=handler.fetchClsIDs(acctype1,idtech)

        return render_template("ShowClassroomsStd.html", data=list1)

    except Exception as e:
        print(str(e))
        return render_template("loginStd.html", msg="show classroom std Failed2 ")


@myapp1.route("/logoutStd")
def logoutStd():
    email1 = session.get("uemail")
    pwd1 = session.get("upwd")
    acctype1 = session.get("uacctype")

    if email1 == None and pwd1 == None and acctype1 == None:
        return render_template("loginUser.html", error=True, errormsg="Please First Login to use this feature")

    session.clear()
    return render_template("loginUser.html")


if __name__ == '__main__':
    myapp1.run(debug =True)
