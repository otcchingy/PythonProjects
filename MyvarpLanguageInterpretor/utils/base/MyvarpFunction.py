from MyvarpLanguageInterpretor.utils.base.MyvarpClass import MyvarpClass


class MyvarpFunction(MyvarpClass):

    def __init__(self):
        super().__init__()
        self.set_attribute('arguments', {'p_args': [], 'kw_args': {}})

    def __add_positional_args(self, arg, default_value=None):
        if self.has_attribute('arguments'):
            args: dict = self.get_attribute('argument')
            p_args: list = args['p_args']
            if arg not in p_args:
                p_args.append({arg: default_value})
                args['p_args'] = p_args
                self.set_attribute('arguments', args)

    def __add_keyword_args(self, kw_args: dict):
        if self.has_attribute('arguments'):
            args: dict = self.get_attribute('argument')
            args['kw_args'] = kw_args
            self.set_attribute('arguments', args)

    def __set_method(self, method):
        pass

    def __get_method(self):
        pass

    def __process_call(self, actual_args=None):
        pass

    def __prepare_method_args(self, args):
        pass

    def __prepare_call_args(self, args=None):
        return self.__process_call(args)

    def prepare_method(self):
        pass

    def run(self, args=None):
        return self.__process_call(args)
