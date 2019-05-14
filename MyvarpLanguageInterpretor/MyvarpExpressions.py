import re
from collections import deque

assignment = re.compile("(\w+ *?\=)")
statement = re.compile("\w+.+\w+.")
operation = re.compile("\w+.+\w+")
params = re.compile("\(.*\)")
expression = statement or operation
variable = re.compile("\w+")
method = re.compile("\.\w+\(.*?\)")
method_call = re.compile("\w+\.\w+\(.*?\)")
call = re.compile("\w+\(.*\)")
collection = re.compile("\[.*\]|\(.*\)|\{.*\}")
rawdata = re.compile("(\w+?,)+[\w]+")
number = re.compile("[0-9]+")
string = re.compile("(\".*?\"|\'.*?\')")
lists = re.compile("\[((\w+,)+\w+)?\]")
sets = re.compile("\{((\w+,)+\w+)?\}")
dicts = re.compile("\{((\w+:\w+,)+\w+:\w+)?\}")
tuples = re.compile("\(((\w+,)+\w+)?\)")
func = re.compile("func +\w+\(.*\)\{?.*")
classes = re.compile("class +\w+\(.*\)\{?.*")
indexing = re.compile("((\w+|\w+\(.*\))(\[([0-9]|[0-9]:[0-9]|[0-9]:[0-9]:[0-9])\])+)")
boolbegin = re.compile("((if|else|while|else +if|when) +\(?|\(+( +| ?))")
comparer = re.compile(
    "(true|false|((\w+|\w+( +| ?)\(.*\)))( +| ?)(==|>|<|>=|<=|is|not|in|is +not|not +in) +(\w+|\w+( +| ?)\(.*\)))")
expressionender = re.compile("(( +| ?)(\)?|\)+)( +| ?){)")
elses = re.compile("(else( +| ?)({?))")
boolean = re.compile(
    '(((if|while|else +if|when) +\(?|\(+( +| ?))(not +)?(true|false|\w+|\w+( +| ?)\(.*\)|((\w+|\w+( +| ?)\(.*\)))( +| ?)(==|!=|>|<|>=|<=|is|not|in|is +not|not +in) +(\w+|\w+( +| ?)\(.*\)))(( +| ?)(\)?|\)+)( +| ?){))|(else( +| ?)({?))')


# p = re.compile('ab*', re.IGNORECASE)


class Stack:
    DATA = deque()

    def __init__(self):
        self.DATA = deque()

    @classmethod
    def push(cls, data):
        cls.DATA.appendleft(data)

    @classmethod
    def pop(cls):
        ret = cls.DATA.popleft()
        return ret

    @classmethod
    def top(cls):
        if cls.isEmpty():
            return None
        return cls.DATA[0]

    @classmethod
    def isEmpty(cls):
        return cls.size() == 0 or cls.DATA is None

    @classmethod
    def size(cls):
        return len(cls.DATA)

    @classmethod
    def __str__(cls):
        return str(cls.DATA)


def has_paranthesis(line):
    line = str(line)
    paranthesis = re.compile("(\(+( +| ?)((\w+|)|\w+( +| ?)(.|..)( +| ?)\w+)( +| ?)\)+)")
    found = paranthesis.findall(line)
    if found != []:
        found = found[0][0]
        if len(found) == len(line):
            return True


def has_curlybraces(line):
    if line[0] == '{' and line[-1] == '}':
        return True


def has_braces(line):
    if line[0] == '[' and line[-1] == ']':
        return True


def is_string(line):
    if isinstance(line, str) and not line.isspace() and line != '':
        if line[0] == '"' and line[-1] == '"':
            return True
        if line[0] == "'" and line[-1] == "'":
            return True


def raw_string(line):
    return line[1:-1]


def split_args(line):
    line = str(line).split(',')
    arg_list = []
    halfStr = None
    retStr = ''
    stop = ''
    for word in line:
        if halfStr == True:
            if word[-1] != stop:
                retStr += word + ','
            else:
                retStr += word
                arg_list.append(retStr)
                retStr = ''
                halfStr = None
        else:
            if word[0] == '"' or word[0] == "'":
                stop = word[0]
                if word[-1] == stop:
                    arg_list.append(word)
                else:
                    halfStr = True
                    retStr += word + ','
            else:
                arg_list.append(word.strip())
    return tuple(arg_list)


def check(p, line):
    if len(p.findall(line)) > 0:
        return True
    return False


def get(p, line):
    if check(p, line):
        return p.findall(line)
    return []


def cleanList(lists):
    l = []
    for item in lists:
        if dress(item):
            l.append(dress(item))
    return l


def dress(line):
    if not str(line).isspace() and line != "":
        return str(line).strip()
    return None


def containsAssignment(line):
    return check(assignment, line)


def isMethodCall(line):
    return check(method_call, line) and validateParanthesis(line)


def isCallable(line):
    return check(call, line) and validateParanthesis(line)


def isFunc(line):
    return check(func, line)


def isClass(line):
    return check(classes, line)


def isCollection(line):
    return check(collection, line) and validateParanthesis(line)


def isNumber(line):
    return check(number, line)


def isString(line):
    return check(string, line)


def isList(line):
    return check(lists, line)


def isDict(line):
    return check(dicts, line)


def isSet(line):
    return check(sets, line)


def isTuple(line):
    return check(tuples, line)


def isIndexing(line):
    return check(indexing, line)


def isRawdata(line):
    return check(rawdata, line)


def hasOperation(line):
    op = ['++', '--', '**', '//', '+=', '-=',
          '*=', '/=', '==', '>=', '<=', '!=', '=',
          '/', '*', '+', '-', '%', '>', '<', '!']
    for i in op:
        if i in line:
            return True


def is_operator(line):
    op = ['++', '--', '**', '//', '+=', '-=',
          '*=', '/=', '==', '>=', '<=', '!=', '=',
          '/', '*', '+', '-', '%', '>', '<', '!']
    for i in op:
        if i == line:
            return True


def isBoolean(line):
    return check(boolean, line) or check(elses, line)


def isStatement(line):
    return check(statement, line)


def isExpression(line):
    return check(expression, line) and validateParanthesis(line)


def isDataObject(line):
    line = line.strip()
    if isCollection(line):
        if isIndexing(line):
            pass
        if isSet(line):
            pass
        elif isDict(line):
            pass
        elif isList(line):
            pass
        elif isTuple(line):
            pass
    elif isString(line):
        return isString(line)
    elif isNumber(line):
        return isNumber(line)
    elif isRawdata(line):
        line = getArgs(line)
        return isRawdata(line)
    else:
        pass


def getArgs(args):
    if validateParanthesis(args):
        while has_paranthesis(args) or has_curlybraces(args) or has_braces(args) and len(args) > 2:
            if has_paranthesis(args) and len(args) > 2:
                args = raw_string(args)
            if has_curlybraces(args) and len(args) > 2:
                args = raw_string(args)
            if has_braces(args) and len(args) > 2:
                args = raw_string(args)
            if args.__contains__(','):
                args = split_args(args)
            return args


def cleansetList(list):
    nlist = []
    list = cleanList(list)
    for l in list:
        if l not in nlist:
            nlist.append(l)
    return nlist


def getBooleanParam(line):
    signs = ['==', '!=', '>=', '<=', '<', '>', 'is', 'in']
    # if sign in signs split condition by sign to get args
    nlist = {}
    list = cleansetList(boolean.findall(line)[0])
    list = cleansetList(list)
    if len(list) == 9:
        nlist['full'] = list[0]
        nlist['method'] = list[2]
        nlist['sign'] = list[5]
        if nlist['sign'] in signs:
            nlist['args'] = cleanList(list[3].split(list[5]))
        else:
            nlist['args'] = (list[4] if not '{' in list[4] else '')
        nlist['condition'] = list[3]
        return nlist
    elif len(list) == 8:
        nlist['full'] = list[0]
        nlist['method'] = list[2]
        nlist['sign'] = list[5]
        if nlist['sign'] in signs:
            nlist['args'] = cleanList(list[3].split(list[5]))
        else:
            nlist['args'] = (list[4] if not '{' in list[4] else '')
        nlist['condition'] = list[3]
        return nlist
    elif len(list) == 7:
        nlist['full'] = list[0]
        nlist['method'] = list[2]
        nlist['sign'] = ''
        if nlist['sign'] in signs:
            nlist['args'] = cleanList(list[3].split(list[5]))
        else:
            nlist['args'] = (list[4] if not '{' in list[4] else '')
        nlist['condition'] = list[3]
        return nlist
    elif len(list) == 6 or len(list) == 5:
        nlist['full'] = list[0]
        nlist['method'] = list[2]
        nlist['sign'] = ''
        if nlist['sign'] in signs:
            nlist['args'] = cleanList(list[3].split(list[5]))
        else:
            nlist['args'] = (list[4] if not '{' in list[4] else '')
        nlist['condition'] = list[3]
        return nlist
    else:
        nlist['full'] = list[0]
        nlist['method'] = 'else'
        nlist['sign'] = ''
        nlist['args'] = ''
        nlist['condition'] = ''
        return nlist


def is_holder(c):
    if c == '[' or c == '{' or c == '(' or c == ')' or c == '}' or c == ']':
        return True

def is_opener(c):
    if c == '[' or c == '{' or c == '(':
        return True

def is_closer(c):
    if c == ')' or c == '}' or c == ']':
        return True

def validateParanthesis(line):

    PARANTHESIS = {
        "{": "}",
        "(": ")",
        "[": "]",
        "'": "'",
        '"': '"'
    }

    stack = Stack()

    line = str(line)

    string_is_open = False
    string_closer = ""

    if '[' in line or '{' in line or '(' in line or ')' in line or '}' in line or ']' in line:
        for c in line:
            if string_is_open and c == string_closer:
                string_is_open = False
                string_closer = ""
            elif not string_is_open and c == "'" or c == '"':
                string_is_open = True
                string_closer = c
            elif is_opener(c) and not string_is_open:
                stack.push(c)
            elif is_closer(c) and not string_is_open:
                if stack.isEmpty() or PARANTHESIS[stack.top()] != c:
                    return False
                else:
                    stack.pop()
        if stack.isEmpty():
            return True
        return False
    return True


def IsPrime(num):
    num = abs(num)

    if num < 2:
        return True
    elif num % 2 == 0:
        return num == 2
    else:
        i = 3
        while i ** 2 <= num:
            if num % i == 0:
                return False
            else:
                i += 2
        return True

def line_is_tuple(line):

    PARANTHESIS = {
        "(": ")",
        "'": "'",
        '"': '"'
    }

    stack = Stack()

    line = str(line)

    first_close = False
    string_is_open = False
    string_closer = ""

    if '(' in line or ')' in line:
        for c in line:
            if string_is_open and c == string_closer:
                string_is_open = False
                string_closer = ""
            elif not string_is_open and c == "'" or c == '"':
                string_is_open = True
                string_closer = c
            elif not string_is_open and c == "(":
                if first_close:
                    return False
                stack.push(c)
            elif not string_is_open and c == ")":
                if stack.isEmpty() or PARANTHESIS[stack.top()] != c:
                    return False
                else:
                    if not first_close and stack.size() == 1:
                        first_close = True
                    stack.pop()
        if stack.isEmpty():
            return True
        return False
    return False

def line_is_dict(line):

    PARANTHESIS = {
        "{": "}",
        "'": "'",
        '"': '"'
    }

    stack = Stack()

    line = str(line)

    first_close = False
    string_is_open = False
    string_closer = ""

    if '{' in line or '}' in line:
        for c in line:
            if string_is_open and c == string_closer:
                string_is_open = False
                string_closer = ""
            elif not string_is_open and c == "'" or c == '"':
                string_is_open = True
                string_closer = c
            elif not string_is_open and c == "{":
                if first_close:
                    return False
                stack.push(c)
            elif not string_is_open and c == "}":
                if stack.isEmpty() or PARANTHESIS[stack.top()] != c:
                    return False
                else:
                    if not first_close and stack.size() == 1:
                        first_close = True
                    stack.pop()
        if stack.isEmpty():
            return True
        return False
    return False

def line_is_list(line):

    PARANTHESIS = {
        "[": "]",
        "'": "'",
        '"': '"'
    }

    stack = Stack()

    line = str(line)

    first_close = False
    string_is_open = False
    string_closer = ""

    if '[' in line or ']' in line:
        for c in line:
            if string_is_open and c == string_closer:
                string_is_open = False
                string_closer = ""
            elif not string_is_open and c == "'" or c == '"':
                string_is_open = True
                string_closer = c
            elif not string_is_open and c == "[":
                if first_close:
                    return False
                stack.push(c)
            elif not string_is_open and c == "]":
                if stack.isEmpty() or PARANTHESIS[stack.top()] != c:
                    return False
                else:
                    if not first_close and stack.size() == 1:
                        first_close = True
                    stack.pop()
        if stack.isEmpty():
            return True
        return False
    return False

def getOperationArguments(line):

    operation_args = []
    stack = Stack()
    _operation = ""

    for c in line:
        if c == "'" or c == '"':
            if stack.top() == c:
                stack.pop()
            _operation += c
        elif c == "'" or c == '"':
            stack.push(c)
            _operation += c
        elif c == "(":
            stack.push(c)
            if len(_operation) > 0:
                _operation += c
        elif c == ")":
            if stack.top() == ")":
                stack.pop()
            if len(_operation) > 0:
                _operation += c
        elif is_operator(c) and not "(" in _operation:
            operation_args.append(_operation.strip())
            operation_args.append(c)
            _operation = ""
        else:
            _operation += c

    if _operation.strip() != "":
        operation_args.append(_operation.strip())

    return operation_args

def getParameterArguments(line):

    raw_args_data = []

    if validateParanthesis(line):

        data = ""
        stack = Stack()

        for i in range(len(line)):
            c = line[i]

            if not stack.isEmpty() and c == stack.top():
                stack.pop()
                data += c
            elif c == "'" or c == '"' or c == "(":
                if c == "(":
                    stack.push(")")
                else:
                    stack.push(c)
                data += c
            elif stack.isEmpty() and c == ",":
                while line_is_tuple(data.strip()):
                    data = raw_string(data.strip()).strip()
                raw_args_data.append(data.strip())
                data = ""
            else:
                data += c

        if data != "":
            while line_is_tuple(data.strip()):
                data = raw_string(data.strip()).strip()
            raw_args_data.append(data.strip())

    return raw_args_data

# print(line_is_tuple("(dasdsddasd)"))
# print(line_is_tuple("(dasds,ddasd)"))
# print(line_is_tuple("(da+(sd)+sd+(da)+sd)"))
# print(line_is_tuple("(da)+(sd)+sd+(da)+(sd)"))
# print(line_is_tuple("(12+45)+(567-8)*7+(2*3)+square(2)"))
# print(line_is_tuple("((12+45)+(567-8)*7+(2*3)+square(2))"))
# print(line_is_tuple("dfsdfsdfsddfsfdf"))

print(getParameterArguments("((12+45)+(567-8)*7+(2*3)+square(2)), 'sasas'"))

print(getParameterArguments("((12+45)+(567-8)*7+(2*3)+square(2))"))

print(getOperationArguments("'name' + (12+45)+(567-8)*7+(2*3)+square(5+(2+3))"))

# print(validateParanthesis("({[ ])}"),
#       validateParanthesis(")(( )){([( )])}"),
#       validateParanthesis("((('')(( )){([( )])}))"),
#       validateParanthesis("( )(( )){([( )])}"),
#       validateParanthesis('()("name is bernard()()")'))

# print(has_paranthesis("()"))
# print(has_paranthesis("(true)"))
# print(has_paranthesis("(( sdfasd ))"))
# print(has_paranthesis("(sdf+asd)"))
# print(has_paranthesis("(sdf)+(asd)"))
# print(has_paranthesis("(sdf)(asd)"))

# print(getBooleanParam("else if (false){ return 0}"))
# print(getBooleanParam("else{ return 0}"))
# print(getBooleanParam("if (1 == 5){ return 0}"))
# print(getBooleanParam("else if (1 > 5){ return 0}"))
# print(getBooleanParam("else if (1 < 7){ return 0}"))
# print(getBooleanParam("else if (1 >= 3){ return 0}"))
# print(getBooleanParam("else if (1 <= 4){ return 0}"))
# print(getBooleanParam("else if (1 in 2){ return 0}"))
# print(getBooleanParam("else if (1 is 1){ return 0}"))
# print(getBooleanParam("else if (new){ return 0}"))
# print(getBooleanParam("else if (old()){ return 0}"))
# print(getBooleanParam("else if (name('bernard')){ return 0}"))
# print(getBooleanParam("else if (not new){ return 0}"))
# print(getBooleanParam("else if (not new(ones)){ return 0}"))
# print(getBooleanParam("else if (not 1 == 1){ return 0}"))
# print(getBooleanParam("else if (not 1 == 2){ return 0}"))

# unEvenClosers("([['sdfd','sdfsdf]'],['sdfsdfsd'])")
# unEvenClosers("['sdfd','sdfsdf]'],['sdfsdfsd]']")


# print(isCollection("[]"))
# print(isCollection("[1,2,3,4]"))
# print(isCollection("(1)"))
# print(isCollection("{'name':1,'age':2}"))
# print(isCollection("[name]"))


# use stacks for everything
