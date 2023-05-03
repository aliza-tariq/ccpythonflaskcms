#BCSF19A005

class User:
    def __init__(self,name1="",email1="",password1="",acc_type1=""):

        self.name=name1
        self.email=email1
        self.password=password1
        self.acc_type=acc_type1



class ClassObject:
    def __init__(self,classId1="",className1="",TeacherId1="",TeacherNo1="",date_Deleted1=""):
        self.classId=classId1
        self.className=className1
        self.TeacherId=TeacherId1
        self.TeacherNo=TeacherNo1
        self.dateDeleted=date_Deleted1


class EnrollmentObject:
    def __init__(self,classId1="",stuIId1="",stuNo1=0,TeacherId1=""):
        self.classId = classId1
        self.stuId = stuIId1
        self.stuNo=stuNo1
        self.TeacherId = TeacherId1