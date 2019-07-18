class MyvarpObject:
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
            access specifications = access_spec = | static | public | private | protected | final | constant
            
    """

    def __init__(self):
        self.__attr_dict__ = {'access_spec': ['protected']}

    def call(self, item=None):
        return self.__attr_dict__['call'].call(item)

    def to_string(self):
        return self.__attr_dict__['to_string']

    def equal_to(self, item):
        return self.__attr_dict__['eq'].call(item)

    def __greater_than(self, item):
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
        try:
            if self.__attr_dict__[f'{name}']:
                return True
            else:
                return False
        except KeyError:
            return False

    def remove_attribute(self, name):
        return self.__attr_dict__.pop(name)

    def class_type(self):
        return self.__attr_dict__['class']

    def clone(self):
        return self.__new__
