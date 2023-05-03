#BCSF19A005

from Classes import User,EnrollmentObject
import pymysql

class DataBaseHandler:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = None

        try:
            self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database)
        except Exception as e:
            print("There is error in connection", str(e))

    def __del__(self):
        if self.con != None:
            self.con.close()

    #return all teachers data
    def getTeachers(self):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select teacher_name,teacher_id,teacher_email,teacher_password,tch_acc_status from teacher"
                cur.execute(query1)
                rows = cur.fetchall()
                print("row are = ",rows)
                return rows
        except Exception as e:
            print(str(e))
        finally:
           if cur != None:
                cur.close()

    #return all students data
    def getStudents(self):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select student_name,student_id,student_email,student_password,std_acc_status from student"
                cur.execute(query1)
                rows = cur.fetchall()
                return rows
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    #for signup check if already user exist or not
    def checkTeacherStdExist(self,accType,email):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if accType=="Teacher":
                    query1 = "select * from teacher where teacher_email=%s;"
                if accType == "Student":
                    query1 = "select * from student where student_email=%s;"
                args = (email)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) > 0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    #check user(student,teacher,adim) exist in db or not
    def checkUserExist(self,user2):
        try:

            if self.con != None:
                cur = self.con.cursor()
                if user2.acc_type == "Teacher":
                    query1 = "select * from teacher where teacher_email=%s and teacher_password=%s and tch_acc_status=1;"
                elif user2.acc_type == "Admin":
                    query1 = "select * from admin where admin_email=%s and admin_password=%s;"
                else:
                    query1 = "select * from student where student_email=%s and student_password=%s and std_acc_status=1;"
                args = (user2.email,user2.password)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) > 0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    #check account of user is disable or not
    def checkUserAccountDisable(self,user2):
        try:

            if self.con!=None:
                cur = self.con.cursor()
                if user2.acc_type!="Admin":
                    if user2.acc_type=="Teacher":
                        query1="select * from teacher where teacher_email=%s and teacher_password=%s and tch_acc_status=0;"
                    elif user2.acc_type=="Student":
                        query1="select * from student where student_email=%s and student_password=%s and std_acc_status=0;"
                    args = (user2.email,user2.password)
                    cur.execute(query1, args)
                    rows=cur.fetchall()
                    if(len(rows)>0):
                        return True
                    else:
                        return False
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    #Add user in database table
    def addUser(self,user2):
        try:
            if self.con!=None:
                cur = self.con.cursor()
                if user2.acc_type=="Teacher":
                    query1="Insert into teacher(teacher_name,teacher_email,teacher_password) values(%s,%s,%s);"
                else:
                    query1 = "INSERT INTO student(student_name,student_email,student_password) values(%s,%s,%s);"

                args = (user2.name,user2.email,user2.password)
                cur.execute(query1, args)
                self.con.commit()

                #set ID of teacher/student
                if user2.acc_type=="Teacher":
                    query2="update teacher set teacher_id=concat(teacher_str,teacher_no);"
                else:
                    query2 = "update student set student_id=concat(student_str,student_no);"

                cur.execute(query2)
                self.con.commit()

                if user2.acc_type=="Teacher":
                    query3="select teacher_id from teacher where teacher_email=%s;"
                else:
                    query3 = "select student_id from student where student_email = %s;"

                args = (user2.email)
                cur.execute(query3,args)
                self.con.commit()
                return cur.fetchall()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addClassroom(self,classObj1):
        try:
            if self.con != None:
                cur=self.con.cursor()
                query1 = "insert into classroom (classroom_name,classroom_id,teacher_no,teacher_id) values(%s,%s,%s,%s);"
                args=(classObj1.className,classObj1.classId,int(classObj1.TeacherNo),classObj1.TeacherId)
                cur.execute(query1,args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def fetchIDs(self,acc_type,Id):
        try:
            if self.con != None:
                cur=self.con.cursor()
            if acc_type == "Teacher":
                query1 = "select classroom_id from classroom where teacher_id =%s and cls_remove_status=1"
                args=(Id)
                cur.execute(query1,args)
                IdList = cur.fetchall()
                return IdList

            elif acc_type=="Student":
                query1 = "select student_id from student where student_id =%s and std_acc_status=1"
                args=(Id)
                cur.execute(query1, args)
                IdList = cur.fetchall()
                return IdList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def checkClassID(self, acc_type, ClassId):
        try:
            if self.con != None:
                cur = self.con.cursor()
            if acc_type == "Teacher":
                query1 = "select *  from  classroom where classroom_id=%s"
                args = (ClassId)
                cur.execute(query1, args)
                IdList = cur.fetchall()
                if len(IdList) == 0:
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getId(self,user):
        try:
            if self.con != None:
                cur=self.con.cursor()
            if user.acc_type == "Teacher":
                query1 = "select teacher_id from Teacher where teacher_email=%s"
            elif user.acc_type=="Student":
                query1 = "select student_id from student where student_email=%s"
            else:
                query1 = "select admin_id from admin where admin_email=%s"
            args=(user.email)
            cur.execute(query1,args)
            id = cur.fetchall()
            return id[0][0]

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addToClassroom(self,enroll=EnrollmentObject()):
            try:
                if self.con != None:
                    cur = self.con.cursor()
                    query1 = "insert into enrollment (classroom_id,student_id, student_no, teacher_id) values(%s,%s,%s,%s);"
                    args = (enroll.classId, enroll.stuId, int(enroll.stuNo), enroll.TeacherId)
                    cur.execute(query1, args)
                    self.con.commit()
            except Exception as e:
                print(str(e))
            finally:
                if cur != None:
                    cur.close()

    def fetchClsIDs(self,acc_type,Id):
        try:
            if self.con != None:
                cur=self.con.cursor()
            if acc_type == "Teacher":
                query1 = "select classroom_id,classroom_name from classroom where teacher_id =%s and cls_remove_status=1"
                args=(Id)
                cur.execute(query1,args)
                IdList = cur.fetchall()
                return IdList

            elif acc_type=="Student":
                query1 = "select classroom_id from enrollment where student_id =%s and enroll_status=1"
                args=(Id)
                cur.execute(query1, args)
                IdList = cur.fetchall()
                return IdList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


