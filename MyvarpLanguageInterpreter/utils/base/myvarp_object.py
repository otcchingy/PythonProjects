from utils.base.processors.process import Process


class MyvarpObject:
    __script__: str
    __interpreter__: None
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

    def __init__(self, parent=None, script: str = "", **kwargs):
        """

        :param parent: parent interpretor
        :param script: lines to process
        :param kwargs:
            access_spec = [
                'private',
                'public',
                'protected'
            ],
            modifier_access = [
                'static',
                'normal'
            ],
            access_state = [
                'final',
                'constant',
                'normal'
            ]
        """
        self.__script__ = script
        self.__result__ = None
        self.__interpreter__ = None
        self.__attr_dict__ = {}

    def call(self, args=None):
        # set interpreter variable (params) to args
        # runs the script in the interpreter (interpreter.interpret) and returns the result # default result = None
        if args is None:
            args = {'posargs': [], 'kwargs': {}}

        param_details = self.get_interpreter().get_all_params()
        posargs: list = args['posargs']
        kwargs: dict = args['kwargs']
        using_kwargs = False
        pos_arg_index = 0
        for i in range(param_details):
            param = param_details[i]
            if param['param-type'] == 'positional':
                if using_kwargs:
                    # TODO: trow error positional arg after kwarg args
                    pass
                elif kwargs.keys().__contains__(param['param']):
                    using_kwargs = True
                    self.get_interpreter().set_param_value(param['param'], kwargs.pop(param['param']))
                else:
                    self.get_interpreter().set_param_value(param['param'],  posargs[pos_arg_index])
                    pos_arg_index += 1
            else:
                using_kwargs = True
                if i == len(param_details)-1:
                    self.get_interpreter().set_param_value(param['param'], kwargs)
                else:
                    # throw error invalid argument structure
                    pass

        self.__result__ = self.get_interpreter().run_script()
        if isinstance(self.__result__, Process) and self.__result__.get_type() == "exception":
            print(self.__result__.get_object())

    def add_parent(self, parent):
        pass

    def get_interpreter(self):
        return self.__interpreter__

    def get_script(self):
        return self.__script__

    def get_value(self):
        return self.__result__ or self.__script__
        pass

    def to_string(self):
        # return new object with script to_string and parent self.__interpreter
        return self.__attr_dict__['to_string']

    def equal_to(self, item):
        return self.get_interpreter().get_property('eq').call(item)

    def greater_than(self, item):
        return self.get_interpreter().get_property('gt').call(item)

    def less_than(self, item):
        return self.get_interpreter().get_property('lt').call(item)

    def greater_than_or_equal_to(self, item):
        return self.get_interpreter().get_property('ge').call(item)

    def less_than_or_equal_to(self, item):
        return self.get_interpreter().get_property('le').call(item)

    def not_equal_to(self, item):
        return self.get_interpreter().get_property('ne').call(item)

    def set_property(self, name, value, **kwargs):
        self.get_interpreter().set_property(name, value, **kwargs)

    def get_property(self, name):
        return self.get_interpreter().get_property(name)

    def set_attribute(self, name, value):
        self.__attr_dict__[f'{name}'] = value

    def get_attribute(self, name):
        return self.__attr_dict__[f'{name}']

    def has_attribute(self, name):
        pass

    def remove_attribute(self, name):
        pass

    def class_type(self):
        return self.__attr_dict__['object']

    def plus(self, other):
        pass

    def minus(self, other):
        pass

    def mul(self, other):
        pass

    def div(self, other):
        pass

    def abs_div(self, other):
        pass

    def is_empty(self):
        return False

    def is_obj(self, other):
        pass

    def and_op(self, other):
        # return not self.is_empty() and not other.is_empty()
        pass

    def or_op(self, other):
        # return not self.is_empty() or not other.is_empty()
        pass

    def clone(self):
        return self.__new__
