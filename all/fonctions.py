import re


def password_verify(password):
    if not re.search("[a-z]",password):
        return False
    elif not re.search("[A-Z]",password):
        return False
    elif not re.search("[0-9]",password):
        return False
    elif not re.search("[_@$]",password):
        return False
    elif re.search("\s",password):
        return False
    else:
        return True