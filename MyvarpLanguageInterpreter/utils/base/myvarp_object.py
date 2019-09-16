from utils.base.myvarp_script_interpreter import MyvarpScriptInterpreter, Process


class MyvarpObject:
    __script__: str  # code
    __interpreter__: MyvarpScriptInterpreter
    __attr_dict__: dict

    """
        important attributes:
            name
            call
            eq
            nt
            lt
            gt
            ge
            le
            to_string
            clone
            access specifications = access_spec = public | private | protected
            modifier access = modifier_access = final | constant 
            access_state = static  
            
    """

    def __init__(self, parent=None, script: str = "", expression_data: list = None):
        self.__script__ = script
        self.__result__ = None
        self.__interpreter__ = MyvarpScriptInterpreter(script, parent=parent, expression_data=expression_data)
        self.__attr_dict__ = {'access_spec': 'protected', 'modifier_access': 'normal', 'access_state': 'normal'}

    def call(self, args: dict = None):
        # set interpreter variable (params) to args
        # runs the script in the interpreter (interpreter.interpret) and returns the result # default result = None
        self.__interpreter__.start_interpreting_process()
        self.__result__ = self.get_attribute('call')(args)
        if isinstance(self.__result__, Process) and self.__result__.type == "exception":
            print(self.__result__.object)

    def get_interpreter(self):
        return self.__interpreter__

    def get_value(self):
        return self.__result__
        pass

    def to_string(self):
        # return new object with script to_string and parent self.__interpreter
        return self.__attr_dict__['to_string']

    def equal_to(self, item):
        return self.__attr_dict__['eq'].call(item)

    def greater_than(self, item):
        return self.__attr_dict__['gt'].call(item)

    def less_than(self, item):
        return self.__attr_dict__['lt'].call(item)

    def greater_than_or_equal_to(self, item):
        return self.__attr_dict__['ge'].call(item)

    def less_than_or_equal_to(self, item):
        return self.__attr_dict__['le'].call(item)

    def not_equal_to(self, item):
        return self.__attr_dict__['ne'].call(item)

    def set_attribute(self, name, value):
        self.__attr_dict__[f'{name}'] = value

    def get_attribute(self, name):
        return self.__attr_dict__[f'{name}']

    def has_attribute(self, name):
        return self.__attr_dict__.keys().__contains__(name)

    def remove_attribute(self, name):
        return self.__attr_dict__.pop(name)

    def class_type(self):
        return self.__attr_dict__['object']

    def clone(self):
        return self.__new__
