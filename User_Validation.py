#BCSF19A005

import re

class UserValidation:
    def __init__(self):
        pass

    def checkIsDigit(self, str1):
        if str!=None:
            for ch in str1:
                if ch.isdigit() == True:
                    return True
        return False

    def validateName(self, name1):
        if (self.checkIsDigit(name1) == True):
            return False
        if (len(name1) <= 0):
            return False
        return True

    def validateEmail(self, email1):
        if (len(email1) <= 0):
            return False
        else:
            st = re.fullmatch(r'[a-zA-Z0-9._+]+@(yahoo.com|gmail.com|outlook.com)', email1)
            if st == None:
               return False
        return True

    def validatePassword(self, pwd1, flagstatus=False):
        if flagstatus == True and len(pwd1) < 8:
            return False
        elif len(pwd1) < 8:
            return False
        return True
