# import date
# import datetime
import logging
# import subprocess
from collections import namedtuple
from typing import Optional, List

import time

from MyvarpExpressions import *

# Main Logger Configurations
# logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
#                     level=logging.DEBUG,
#                     filename="logs.txt"
#                     )

# basicConfg   datefmt="%d-%m-%Y %H:%M:%S"
# logging.getLogger(__name__)
# logging.getLogger(appname)
# logging.getLogger(appname.somemudole)
# logging.info("This is it")
# logging.debug("something stupid happened")
# logging.warning("you should'nt be doing that")
# logging.critical("the programs gonna fail")
# logging.disable(logging.DEBUG)


logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logging = logging.getLogger(__name__)

Process = namedtuple("Process", ["type", "object", "method", "args", "result"])


def assignP(p, **kwargs):
    s = {
        'type': p.type,
        'object': p.object,
        'method': p.method,
        'args': p.args,
        'result': p.result}
    for i, j in kwargs.items():
        s[i] = j
    return Process(s['type'], s['object'], s['method'], s['args'], s['result'])


# noinspection SpellCheckingInspection
class MyvarpRun:
    _temp = None
    _return = None
    _lines = ""
    _output = None
    _status = None
    _builtins = None
    _environ = None
    _multiline = None
    _multicomment = None
    _mline = ""

    def __init__(self):

        self._status = {
            'condition': None,
            'decision': None,
            'operating': None
        }

        self._environ = {
            'variables': {},
            'functions': {},
            'classes': {}
        }

        self._builtins = {
            'operators': {
                '++': {'name': '_inc_', 'function': self._inc_},
                '--': {'name': '_dec_', 'function': self._dec_},
                '**': {'name': '_pow_', 'function': self._pow_},
                '//': {'name': '_div.abs_', 'function': self._abs_div_},
                '+=': {'name': '_self.add_', 'function': self._self_add_},
                '-=': {'name': '_self.sub_', 'function': self._self_sub_},
                '*=': {'name': '_self.mul_', 'function': self._self_mul_},
                '/=': {'name': '_self.div_', 'function': self._self_div_},
                '==': {'name': '_is_eq_to_', 'function': self._add_},
                '>=': {'name': '_ge_', 'function': self._ge_},
                '<=': {'name': '_le_', 'function': self._le_},
                '!=': {'name': '_ne_', 'function': self._ne_},
                '=': {'name': '_eq_', 'function': self._eq_},
                '/': {'name': '_div_', 'function': self._div_},
                '*': {'name': '_mul_', 'function': self._mul_},
                '+': {'name': '_add_', 'function': self._add_},
                '-': {'name': '_sub_', 'function': self._sub_},
                '%': {'name': '_mod_', 'function': self._mod_},
                '>': {'name': '_gt_', 'function': self._gt_},
                '<': {'name': '_lt_', 'function': self._lt_},
                '!': {'name': '_not_', 'function': self._ne_}
            },

            'keywords': {
                'if': {'name': '_if_', 'function': self._pass_},
                'else': {'name': '_else_', 'function': self._pass_},
                'else if': {'name': '_elif_', 'function': self._pass_},
                'func': {'name': '_func_', 'function': self._pass_},
                'class': {'name': '_class_', 'function': self._pass_},
                'return': {'name': '_return_', 'function': self._pass_},
                'when': {'name': '_when_', 'function': self._pass_},
                'with': {'name': '_with_', 'function': self._pass_},
                'as': {'name': '_as_', 'function': self._pass_},
                'loop': {'name': '_loop_', 'function': self._pass_},
                'from': {'name': '_from_', 'function': self._pass_},
                'for': {'name': '_for_', 'function': self._pass_},
                'do': {'name': '_do_', 'function': self._pass_},
                'then': {'name': '_then_', 'function': self._pass_},
                'foreach': {'name': '_foreach_', 'function': self._pass_},
                'try': {'name': '_try_', 'function': self._pass_},
                'except': {'name': '_except_', 'function': self._pass_},
                'break': {'name': '_break', 'function': self._pass_},
                'continue': {'name': '_continue_', 'function': self._pass_},
            },

            'types': {
                'number': {'name': '_Number_', 'function': self._int_},
                'int': {'name': '_Number_', 'function': self._int_},
                'float': {'name': '_Float_', 'function': self._float_},
                'string': {'name': '_String_', 'function': self._string_},
                'list': {'name': '_List_', 'function': self._list_},
                'dict': {'name': '_Dict_', 'function': self._dict_},
                'set': {'name': '_Set_', 'function': self._set_},
                'tuple': {'name': '_Tuple_', 'function': self._tuple_},
                'bool': {'name': '_Bool_', 'function': self._bool_},
                'byte': {'name': '_Byte_', 'function': self._byte_},
                'object': {'name': '_Object_', 'function': self._object_},
                'true': {'name': '_True_', 'function': True},
                'false': {'name': '_False_', 'function': False},
                'none': {'name': '_None_', 'function': None}
            },

            'functions': {
                'display': {
                    'params': {
                        'arguments': ['args', 'start', 'sep', 'endl'],
                        'defaults': {'start': '', 'sep': ' ', 'endl': '\n'}
                    },
                    'function': self._display_,
                    'return': None
                },
                'input': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self._input_,
                    'return': None
                },
                'type': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self._type_,
                    'return': None
                },
                'exit': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self._exit_,
                    'return': None
                },
                'sleep': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self._sleep_,
                    'return': None
                },
                'check_type': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self.check_type,
                    'return': None
                },
                'getvar': {
                    'params': {
                        'arguments': ['args'],
                        'defaults': {}
                    },
                    'function': self._getvar_,
                    'return': None
                },
            }
        }

    def read(self, line, _return=None):
        self.run(line)
        self._return = _return

    def run(self, line):
        logging.debug("original = {} ".format(line))
        if self._multicomment:
            line = self.continueCollectingComments(line)
            if line is not None:
                line = self._lines.strip() + line.strip()
            else:
                line = self._lines
            self._line = ""  # reseting temp line storage
            logging.debug("continue collecting comments = {} ".format(line))
        else:
            line = self.stripComments(line)
            logging.debug("after striping comments = {} ".format(line))
        # if self.isMultiline(line): 
        #     logging.debug('is multiline  :: start collecting')
        # self._nline += line
        # line = self.continueCollectingLines(line)

        self._status['operating'] = None
        self._temp = None
        lines = self.splitline(line.strip())
        logging.debug("after spliting collected = {} ".format(lines))
        logging.debug("muticomment status = {} ".format(self._multicomment))
        if self._multicomment != True:
            for line in lines:
                logging.debug("processing line  : {} ".format(line))
                self.process(line) if line != "" else self._pass_()
                logging.debug("Environ Variables : {}".format(self._environ['variables']))
                logging.debug("Output :: {}".format(self._output))
                logging.debug("Temp :: {}".format(self._temp))
                if self._return:
                    print(self._output) if self._output is not None else self._pass_()
                self._output = (None if self._return else self._output)
            return self
        self._output = "..."

    def assign(self, obj, _return=None):
        if isinstance(obj, MyvarpRun):
            self = obj
            self._return = _return
            return self

    def splitline(self, old_line):
        lines = []
        if old_line is not None and ";" in old_line:
            line = ""
            stop = ""
            state = "closed"
            for i in range(len(old_line)):
                c = old_line[i]
                if state == "open":
                    line += c
                    if c == stop:
                        state = "closed"
                elif state == "closed":
                    if c == '"' or c == "'":
                        stop = c
                        state = "open"
                    if c != ";":
                        line += c
                    else:
                        lines.append(line)
                        line = ""
            lines.append(line) if line != "" else self._pass_()
            return lines
        return [old_line]

    def stripComments(self, old_line):
        line = ""
        mlc = False
        logging.debug("in striping comment start = {} ".format(old_line))
        logging.debug("mulcomm stats = {} ".format(self._multicomment))

        if self._multicomment == True:
            logging.debug("checking for end of multilinecomment")
            return self.continueCollectingComments(old_line)

        if "#" in old_line:
            stop = ""
            state = "closed"
            for i in range(len(old_line)):
                c = old_line[i]
                if mlc == True and (i + 4) < len(old_line):
                    r = old_line.find("###") + 3
                    rol = old_line[r:]
                    if rol.count("###") > 0:
                        logging.debug("cleaning single line multi commenting")
                        index = rol.find("###") + 3
                        rol = rol[index:]
                        self.multiline = False
                        self.run(line.strip() + ";" + rol.strip())
                        return ''
                    else:
                        self.multiline = True
                        break
                if state == "open":
                    line += c
                    if c == stop:
                        state = "closed"
                elif state == "closed":
                    if c == '"' or c == "'":
                        stop = c
                        line += c
                        state = "open"
                    elif c == "#":
                        if i + 2 < len(old_line) and old_line[i + 1] == "#" and old_line[i + 2] == "#":
                            mlc = True
                        else:
                            break
                    else:
                        line += c

            if mlc == True:
                self._multicomment = True
                self._lines = line
            logging.debug("in # striping comment end = {} ".format(line))
            return line
        logging.debug("in striping comment end = {} ".format(old_line))
        return old_line

    def continueCollectingComments(self, line):
        line = str(line)
        if self._multicomment == True:
            nline = ""
            if line.__contains__("###"):
                self._multicomment = False
                z = line.rfind("###") + 3
                for i in range(z, len(line)):
                    nline += line[i]
                    nline = nline.strip().rstrip()
                logging.debug("result from continue collecting = {}".format(nline))
                logging.debug("multicommenting status in continue collecting = {}".format(self._multicomment))
                self._output = None
                return self.stripComments(nline)
            else:
                self._output = "..."
        else:
            line = self.stripComments(line)
            self._lines += line
            return self._lines

    # def isMultiline(self, line):
    #     if str(line).endswith("\\") or self.unEvenClosers(line) :
    #         return True

    def continueCollectingLines(self, line):
        pass

    def process(self, line):
        p = self.getProcess(line)
        logging.debug(p)
        if p is not None and p.object != "":
            if p.type == "f.callable":
                hf = self.is_function(p.method)
                if hf != False:
                    self.run_function(p)
                else:
                    self._output = "CallError :: Callable object {} does not exist ".format(p.object)
            elif p.type == "m.callable":
                hf = self.is_function(p.method)
                if hf:
                    pass
                else:
                    self._output = "CallError :: Callable object {} or Method {} does not exist ".format(p.object,
                                                                                                         p.method)
            elif p.type == "operation":
                if p.object == "expression":
                    p = assignP(p, result=self.get_arg_values(p.args))
                else:
                    operator = self._builtins['operators'][p.method]
                    operate = operator['function']
                    p = assignP(p, result=operate(p))
                self._output = p.result
                self._temp = p
            elif p.type == "expression":
                try:
                    if self.exist_var(line):
                        self._output = self.get_var(line)
                    elif self.get_arg_values(line) is not None:
                        self._temp = self.get_arg_values(line)
                        self._output = self._temp
                    elif '[' in line and ']' in line:
                        self._index_(line)
                    else:
                        self._output = 'NameException :: Undefined Name'
                except Exception as e:
                    self._output = "Error :: {}".format(e)
            elif str(p.type).__contains__("datatype"):
                p = assignP(p, result=self.get_arg_values(p.object))
                self._output = p.result
                self._temp = p
            elif p.type == 'exception':
                # throwException(p)
                self._output = p.object

    def getProcess(self, line):

        if isBoolean(line):
            print("bool caught.... setting up and running statements")
        if isFunc(line):
            print("caught function.... setting up and defining func")
        if isClass(line):
            print("caught class.... setting up and defining new class")
        if containsAssignment(line) and isCallable(line):
            # checking which one comes first
            i = str(line).find('=')
            j = str(line).find('(')
            if i < j:
                return self.getAssignmentArgs(line)
            return self.getcallArgs(line)
        elif containsAssignment(line):
            return self.getAssignmentArgs(line)
        elif isCallable(line):
            return self.getcallArgs(line)
        elif hasOperation(line):
            logging.debug("as operation")
            return self.getOperation(line)
        elif isDataObject(line):
            return self.getDataObject(line)
        # elif isIndexing(line):
        #     return self._index_(line)
        elif self.is_type(line):
            return Process("datatype.system", line, None, None, None)
        elif isExpression(line):
            return self.getExpression(line)
        elif self.has_builtin(line):
            ho = self.is_operator(line)
            hk = self.is_keyword(line)
            if ho:
                line = line.split(ho)
                operator = self._builtins['operators']['{}'.format(ho)]
                f = operator['function']
                f(line)
            elif hk:
                pass
            else:
                self._output = 'SyntaxError :: Cannot run command : Invalid syntax at {} '.format(line)
        return Process("expression", line, None, None, None)

    def getAssignmentArgs(self, line):
        try:
            c = get(assignment, line)[0]
            name = get(variable, c)[0]
            args = line[line.find(c) + len(c):].strip()
            if self.has_builtin(args):
                args = self.getParamArgs(args)
                if args is None:
                    return Process("exception", "NameException :: Undefined Name", None, line, None)
            return Process("operation", name, "=", args, None)
        except Exception as e:
            return Process("exception", "AssignmentError :: " + str(e), None, line, None)

    def getcallArgs(self, line):
        # try:
        if isMethodCall(line):
            c = get(method_call, line)[0]
            t = get(call, line)[0]
            obj = cleanList(c.split("." + t))[0]
            args = get(params, c)[0]
            name = cleanList(t.split(args))[0]
            args = self.getParamArgs(args)
            if args is None:
                return Process("exception", "NameException :: Undefined Name", None, line, None)
            return Process("m.callable", obj, name, args, None)
        elif isCallable(line):
            args = get(params, get(call, line)[0])[0]
            name = cleanList(get(call, line)[0].split(args[0]))[0]
            args = self.getParamArgs(args)
            if args is None:
                return Process("exception", "NameException :: Undefined Name", None, line, None)
            return Process("f.callable", None, name, args, None)

    # except Exception as e:
    #     return Process("exception", "CallError :: "+str(e), None, line, None)

    def getOperation(self, line):
        return Process('operation', 'expression', None, self.getParamArgs(line), None)

    def resolveOperation(self, operation_args):
        pass

    def resolveParameterArguments(self, line):

        args_list = getParameterArguments(line)

        resolved_args = []

        for arg in args_list:
            if hasOperation(line):
                result = self.resolveOperation(getOperationArguments(line))
            elif isCallable(arg):
                result = self.getProcess(arg).result
                resolved_args.append(result)
            elif containsAssignment(arg):
                args = cleanList(arg.split("="))
                arg = {args[0].strip(): args[1].strip()}
                resolved_args.append(arg)
            elif arg.isidentifier():
                arg = self.get_arg_values(arg)
                resolved_args.append(arg)
            else:
                arg = self.get_arg_values(arg)
                resolved_args.append(arg)

        return resolved_args



    def getParamArgs(self, line):

        logging.debug("Getting Arguments for Params = {}".format(line))
        logging.debug("Testing resolveParamArgument = {}".format(self.resolveParameterArguments(line)))
        print(type(self.resolveParameterArguments(line)))
        print(type(self.resolveParameterArguments(line)[0]))

        arg_list = []
        arg_line = ""
        length = len(line)

        for i in range(length):
            c = line[i]
            if is_operator(c) or is_holder(c) or c == ",":
                arg_list.append(arg_line)
                arg_list.append(c)
                arg_line = ""
            else:
                arg_line += c

        if arg_line != "":
            arg_list.append(arg_line.strip())

        args = ""
        call = None
        stop = ''
        cparam = ""
        kwargs = False
        kparam = ""
        kcall = None
        ckwargs = {}
        kname = None
        string = False
        brackets = 0
        kcount = 0
        for i in range(len(arg_list)):
            arg = arg_list[i]
            if string or call or kwargs:
                if string == True:
                    if len(arg) > 1 and stop in args:
                        string = False
                        # print("got here")
                        arg = arg.rstrip()
                    elif arg == stop:
                        string = False
                        arg = arg
                    args += arg
                    # print("args at string continue = |{}|".format(arg))
                elif kwargs == True:
                    if kcount == 0:
                        kcount += 1
                    elif kcount == 1:
                        if kcall == True:
                            # print("args at kwargs = |{}|".format(arg))
                            if arg == "(":
                                brackets += 1
                            elif arg == ')':
                                brackets -= 1
                            kparam += arg
                            if brackets == 0:
                                kcall = False
                                kwargs = False
                                kcount = 0
                                p = self.getcallArgs(kparam)
                                print(p)
                                arg = self.getParamArgs(p.args)
                                p = assignP(p, args=arg)
                                p = self.run_function(p)
                                arg = p.result
                        if arg.isidentifier():
                            # print("args at kwargs identifier = |{}|".format(arg))
                            arg = arg.strip()
                            if i + 1 < len(arg_list) - 1 and arg_list[i + 1] == '(':
                                kcall = True
                                kparam = arg
                            else:
                                arg = self.get_arg_values(arg)
                                kwargs = False
                                ckwargs[kname] = arg
                        else:
                            if arg != ')':
                                kparam += arg
                            else:
                                args += arg
                                ckwargs[kname] = kparam
                elif call == True:
                    if arg == "(":
                        brackets += 1
                    elif arg == ')':
                        brackets -= 1
                    cparam += arg
                    # print("args at call param begin = |{}|".format(cparam))
                    if brackets == 0:
                        call = False
                        p = self.getcallArgs(cparam)
                        arg = self.getParamArgs(p.args)
                        p = assignP(p, args=arg)
                        p = self.run_function(p)
                        args += str(p.result)

            else:
                if len(arg) > 1 and ("'" == arg[0] or '"' == arg[0]) and arg[0] != arg[-1]:
                    string = True
                    stop = arg[0]
                    args += arg
                    # print("args at string begin = |{}|".format(arg))
                elif arg.strip().isidentifier():
                    arg = arg.strip()
                    if i + 1 < len(arg_list) - 1 and arg_list[i + 1] == '(':
                        call = True
                        cparam = arg
                    elif i + 1 < len(arg_list) - 1 and arg_list[i + 1] == '=':
                        kwargs = True
                        kname = arg
                    else:
                        arg_ = self.get_arg_values(arg)
                        if arg_ is not None and arg is not 'None':
                            args += str(arg_)
                        else:
                            return None
                    # print("args at identifier = |{}|".format(arg_))
                else:
                    # print("args at else = |{}|".format(arg))
                    args += arg.strip()

        if ckwargs != {}:
            args = {'args': args, 'kwargs': ckwargs}

        logging.debug("Result Arguments for Params = {}".format(line))

        return args

    def getDataObject(self, line):
        line = line.strip()
        if isCollection(line):
            if isIndexing(line):
                return Process("datatype.collection", line, None, None, None)
            if isSet(line):
                return Process("datatype.set", line, None, None, None)
            elif isDict(line):
                return Process("datatype.dict", line, None, None, None)
            elif isList(line):
                return Process("datatype.list", line, None, None, None)
            elif isTuple(line):
                return Process("datatype.tuple", line, None, None, None)
        elif isString(line):
            return Process("datatype.string", line, None, None, None)
        elif isRawdata(line):
            line = self.getParamArgs(line)
            return Process("datatype.tuple", line, None, None, None)
        elif isNumber(line):
            return Process("datatype.number", line, None, None, None)

        else:
            pass

    def getExpression(self, line):
        return Process("expression", line, None, None, None)

    def has_operator(self, line):
        for operator in self._builtins['operators'].keys():
            if operator in line:
                return True
        return False

    def is_operator(self, line):
        for operator in self._builtins['operators'].keys():
            if operator == line:
                return operator
        return False

    def has_keyword(self, line):
        for keyword in self._builtins['keywords'].keys():
            if keyword in line:
                return True

    def is_keyword(self, line):
        for keyword in self._builtins['keywords'].keys():
            if keyword == line:
                return keyword
        return False

    def has_function(self, line):
        for f in self._builtins['functions'].keys():
            if f in line:
                return True
        for f in self._environ['functions'].keys():
            if f in line:
                return True
        for f in self._builtins['types'].keys():
            if f in line:
                return True
        return False

    def is_function(self, line):
        for f in self._builtins['functions'].keys():
            if line == f:
                return f
        for f in self._environ['functions'].keys():
            if line == f:
                return f
        for f in self._builtins['types'].keys():
            if line == f:
                return f
        return False

    def is_type(self, line):
        if line is not None:
            for t in self._builtins['types'].keys():
                if t == str(line):
                    return True
            return False

    def is_builtin(self, line):
        for tool in self._builtins.keys():
            for key in self._builtins[tool]:
                if key == line:
                    return True
        return False

    def has_builtin(self, line):
        for tool in self._builtins.keys():
            for key in self._builtins[tool]:
                if key in line:
                    return key
        return False

    def exist_var(self, name):
        try:
            (self._environ['variables'])['{}'.format(name)]
            return True
        except KeyError:
            return False

    def get_var(self, name):
        try:
            if self.is_builtin(name) == True or name == "True" or name == "False" or name == "None":
                return name.lower()
            else:
                return (self._environ['variables'])['{}'.format(name)]
        except KeyError:
            self._output = "NameException :: Undefined Name"

    def set_var(self, name, value):
        if self.is_builtin(name) == False:
            (self._environ['variables'])['{}'.format(name)] = value
            # if self.exist_var(name):
            #     logging.debug("exist var")
            #     logging.debug("is type {} ".format(self.is_type(self.get_var(name))))
            #     if self.is_type(self.get_var(name)):
            #         _type = self.get_var(name)
            #         if self._type_(value) == _type:
            #             (self._environ['variables'])['{}'.format(name)] = value
            #         else:
            #             self._output = 'AssignmentError :: Type mismatch : object should be type {}'.format(_type)
            # else:
            #     (self._environ['variables'])['{}'.format(name)] = value
        else:
            print('AssignError :: Cannot assign to name {} : failed Syntax'.format(name))
            self._output = 'AssignError :: Cannot assign to name {} : failed Syntax'.format(name)

    def get_args(self, fname, line):
        args = ''
        mark = False
        for c in line:
            if c == '(':
                mark = True
            if mark:
                args += c
            if c == ')':
                return args

    def get_index(self, line):
        args = ''
        mark = False
        for c in line:
            if c == '[':
                mark = True
            if mark:
                args += c
            if c == ']':
                return args

    def get_arg_values(self, args):
        old_args = args
        logging.debug("finding arg value for {} in get_arg_values".format(args))
        while has_paranthesis(args):
            args = raw_string(args).strip()
        if args is not None:
            if self.is_type(args):
                return args
            if isinstance(args, str):
                if args == '' or args.isspace():
                    return args
            if not isinstance(args, (tuple, dict, set)) and args.isidentifier():
                args = self.get_var(args)
            else:
                if isinstance(args, dict):
                    rargs = {}
                    for k in args.keys():
                        rargs[k] = self.get_arg_values(args[k])
                    args = rargs
                elif isinstance(args, (tuple, list, set)):
                    arg_list = []
                    for arg in args:
                        arg_list.append(self.get_arg_values(arg))
                    args = tuple(arg_list)
                else:
                    try:
                        args = eval("{}".format(args))
                    except Exception:
                        args = self.get_var(args)
                if args is None:
                    if '[' in old_args and ']' in old_args:
                        args = self._index_(old_args)
            logging.debug("returning from get_arg_values {}".format(args))
            return args
        logging.debug('Something went wrong in get arg Values')

    def evaluate(self, args):
        print(args)
        session = self.new_session()
        session.process(args)
        return session._temp

    def new_session(self, _return=None):
        session = MyvarpRun()
        session.assign(self, _return)
        return session

    def validateCall(self, p):
        if self.is_type(p.method):
            return p
        elif p.object == None:
            func = self.get_function(p)
            params = func['params']
            args = params['arguments']
            defargs = params['defaults']
            if isinstance(p.args, dict):
                newkwargs = {}
                arg, kwarg = p.args['args'], p.args['kwargs']
                provided = []
                for k in kwarg.keys():
                    if k in defargs.keys():
                        newkwargs[k] = kwarg[k]
                        provided.append(k)
                    else:
                        if k in args:
                            arg + '{}'.format(k)
                        else:
                            self._output = 'InvalidKeywordArgument ::  Keyword does not exits for this  function {}'
                            return None
                for k in defargs:
                    if k not in provided:
                        newkwargs[k] = defargs[k]
                newargs = {'args': arg, 'kwargs': newkwargs}
                return assignP(p, args=newargs)
            else:
                # if len(args) > 1:
                #     #split the string p.args in to the the various params
                #     #and assign relace then with p.args then send new p  
                # else:
                #     #check if p.args != () then continue else throw args param error
                if len(defargs) > 0:
                    newargs = {'args': p.args, 'kwargs': defargs}
                    return assignP(p, args=newargs)
                else:
                    return p

    def get_function(self, p):
        func = None
        try:
            func = (self._builtins['types'][p.method])
        except KeyError:
            try:
                func = (self._builtins['functions'][p.method])
            except KeyError:
                try:
                    func = (self._environ['functions'][p.method])
                except KeyError:
                    self._output = "CallError :: function {} does not exist".format(p.method)
        return func

    def run_function(self, p):
        func = self.get_function(p)['function']
        if func:
            p = self.validateCall(p)
            if p:
                if isinstance(p.args, dict):
                    args = self.get_arg_values(p.args['args'])
                    kwargs = self.get_arg_values(p.args['kwargs'])
                    p = assignP(p, result=func(p.args['args'], kwargs=kwargs))
                else:
                    args = self.get_arg_values(p.args)
                    p = assignP(p, result=func(p.args))
                self._output = p.result
                self._temp = p
                return p
            else:
                self._output = "Invalid :: Call Parameters"

    def run_method(self, p):
        func = (self._builtins['functions'][p.method])['function']
        p = assignP(p, result=func(p.args))
        self._output = p.result
        self._temp = p
        return p

    def func_creator(self):
        pass

    def func_runner(self):
        pass

    def _eq_(self, p):
        name = p.object
        try:
            if is_string(p.args):
                value = p.args
            else:
                value = self.get_arg_values(p.args)

            if value is not None:
                if name.isidentifier():
                    self.set_var(name, value)
                else:
                    self._output = 'SyntaxError :: Invalid Variable Name'
            self._output = "NameError :: Can't find value for {}".format(p.args)
        except Exception:
            self._output = 'AssignError :: Failed to assign {} to {}: failed Syntax'.format(p.args, name)

    def _add_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp + val
        return temp

    def _sub_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp - val
        return temp

    def _mul_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp * val
        return temp

    def _div_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp / val
        return temp

    def _self_add_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp += val
        return temp

    def _self_sub_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp -= val
        return temp

    def _self_mul_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp *= val
        return temp

    def _self_div_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp /= val
        return temp

    def _abs_div_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp // val
        return temp

    def _mod_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp % val
        return temp

    def _pow_(self, p):
        temp = 0
        if isinstance(p.args, tuple) == True:
            args = p.args
        else:
            args = (p.args)
        for arg in args:
            if arg.isidentifier():
                val = self.get_var(arg)
            elif is_string(arg):
                val = raw_string(arg)
            else:
                val = self.get_arg_values(arg)
            if self._status['operating'] is None:
                self._status['operating'] = True
                temp = val
            else:
                temp = temp ** val
        return temp

    def _inc_(self, p):
        pass

    def _dec_(self, p):
        pass

    def _ne_(self, p):
        pass

    def _gt_(self, p):
        pass

    def _ge_(self, p):
        pass

    def _lt_(self, p):
        pass

    def _le_(self, p):
        pass

    def _index_(self, args):
        arg = self.get_index(args)
        name = args.replace(arg, '')
        try:
            self._output = eval("self.get_var('{}'){}".format(name, arg))
            return self._output
        except TypeError:
            self._output = 'TypeError :: The object {} is  no subscriptable'.format(self.get_var(name))
        except IndexError:
            self._output = "IndexError :: The index you're trying to reach is out of Bounds"

    def _int_(self, val):
        try:
            return int(self.get_arg_values(val))
        except Exception as e:
            self._output = "ValueError :: " + str(e)
            return 'none'

    def _string_(self, val):
        val = self.get_arg_values(val)
        if is_string(val):
            return val
        else:
            return '"{}"'.format(val)

    def _bool_(self, val):
        if isinstance(val, tuple):
            val = val[0]
        if is_string(val):
            val = raw_string(val)
            if val == 'true':
                return 'true'
            elif val == 'false':
                return 'false'
        else:
            if val == 'true':
                return 'true'
            elif val == 'false':
                return 'false'
            else:
                return 'none'
        try:
            val = self.get_arg_values(val)
            if val == 'true':
                return 'true'
            elif val == 'false':
                return 'false'
            elif eval(val) == 1:
                return 'true'
            elif eval(val) == 0:
                return 'false'
            else:
                return 'none'
        except Exception:
            self._output = "ValueEror :: Cannot convert object {} to bool".format(val)

    def _float_(self, val):
        val = self.get_arg_values(val)
        return float(val)

    def _list_(self, val):
        val = self.get_arg_values(val)
        return list(val)

    def _tuple_(self, val):
        val = self.get_arg_values(val)
        return tuple(val)

    def _set_(self, val):
        val = self.get_arg_values(val)
        return set(val)

    def _dict_(self, val):
        val = self.get_arg_values(val)
        return dict(val)

    def _object_(self):
        return object

    def _byte_(self, val):
        val = self.get_arg_values(val)
        return bytearray(val)

    def _getvar_(self, val):
        val = self.get_arg_values(val)
        self._output = val
        return val

    def _if_(self, a, b):
        return a + b

    def _else_(self, a, b):
        return a - b

    def _elif_(self, a, b):
        return a * b

    def _pass_(self):
        pass

    def _display_(self, args, kwargs={}):
        args = self.get_arg_values(args)
        if isinstance(args, (tuple, list, dict)):
            for arg in args:
                print(kwargs['start']) if kwargs['start'] != '' else self._pass_()
                print(str(arg) + str(kwargs['sep']), end='')
            print(kwargs['endl'], end='')
        else:
            print(kwargs['start'], end="") if kwargs['start'] != '' else self._pass_()
            print(args, sep=kwargs['sep'], end=kwargs['endl'])

    def _input_(self, arg):
        # arg = eval(arg)
        arg = self.get_arg_values(arg)
        self._temp = input(arg)
        self._output = self._temp
        return '"' + self._temp + '"'

    def _type_(self, obj):
        obj = raw_string(obj)
        obj = str(obj)
        print(obj)
        if is_string(obj):
            return 'string'
        elif self.is_type(obj):
            return 'object'
        elif obj.lower() == "true" or obj.lower() == "false":
            return "bool"
        elif obj.isidentifier():
            obj = self.get_arg_values(obj)
            return self._type_(obj)
        else:
            _type = str(type(eval(obj)))
            if _type.__contains__("int"):
                return "int"
            elif _type.__contains__("bool"):
                return "bool"
            elif _type.__contains__("list"):
                return "list"
            elif _type.__contains__("dict"):
                return "dict"
            elif _type.__contains__("set"):
                return "set"
            elif _type.__contains__("byte"):
                return "byte"
            else:
                # check user class __future
                logging.debug("all failed")
                return "object"

    def check_type(self, args):
        obj = args[0]
        _type = args[1]
        if obj.isidentifier():
            obj = self.is_type(self.get_arg_values(args))
        if self._type_(obj) == _type:
            return True
        return False

    def _sleep_(self, arg):
        arg = self.get_arg_values(arg)
        time.sleep(arg)

    def _exit_(self, arg):
        arg = self.get_arg_values(arg)
        exit(arg)

    def __str__(self):
        return self._output
