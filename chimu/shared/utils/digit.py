import re

dig = re.compile('\d+(\.\d+)?')


def isDigit(s: str):
    if (s == None):
        return False

    return dig.match(s) != None
