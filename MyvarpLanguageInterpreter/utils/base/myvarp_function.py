from utils.base.myvarp_class import MyvarpClass


class MyvarpFunction(MyvarpClass):

    def __init__(self, scope=None, script: str = "", expression_data: list = None):
        super().__init__(scope, script, expression_data)

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

    def to_string(self):
        return f'[object Function<{self.get_name()}>]'

    def run(self, args=None):
        return self.__process_call(args)