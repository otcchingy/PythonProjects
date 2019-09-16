from utils.base.myvarp_object import MyvarpObject


class MyvarpClass(MyvarpObject):

    def __init__(self, scope=None, script: str = "", expression_data: list = None):
        super().__init__(parent=scope, script=script, expression_data=expression_data, )
        self.set_name('MyvarpClass')
        self.set_attribute('arguments', {'p_args': [], 'kw_args': {}})

    def set_name(self, name: str):
        self.set_attribute('name', name)

    def get_name(self) -> str:
        return self.get_attribute('name')

    def construct(self, args):
        # split args and create variables in memory with values
        pass

    def add_positional_param(self, arg, default_value=None, _arg_type_hint='all'):
        self.__add_positional_args(arg, default_value, _arg_type_hint)

    def add_keyword_param(self, kw_arg, kw_value):
        self.__add_keyword_args(kw_arg, kw_value)

    def get_positional_args(self):
        return self.get_attribute('arguments')['p_args']

    def get_keyword_args(self):
        return self.get_attribute('arguments')['kw_args']

    def __add_positional_args(self, arg, default_value=None, _arg_type_hint='all'):
        if self.has_attribute('arguments'):
            args: dict = self.get_attribute('arguments')
            p_args: list = args['p_args']
            if p_args is None:
                p_args = []
            if arg not in p_args:
                p_args.append(
                    {
                        'index': len(p_args),
                        'name': arg,
                        'type': 'all'
                    })
                self.get_interpreter().get_memory().set_item(arg, default_value)
                args['p_args'] = p_args
                self.set_attribute('arguments', args)

    def __add_keyword_args(self, kw_arg, kw_value):
        if self.has_attribute('arguments'):
            args: dict = self.get_attribute('argument')
            if args['kw_args'] is None:
                args['kw_args'] = {}
            args['kw_args'][f'{kw_arg}'] = kw_value
            self.get_interpreter().get_memory().set_item(kw_arg, kw_value)
            self.set_attribute('arguments', args)

    def get_positional_args(self):
        return self.get_attribute('arguments')['p_args']

    def get_keyword_args(self):
        return self.get_attribute('arguments')['kw_args']

    def inherit_from_class(self):
        pass

    def add_access_specifier(self, name: str):
        if name in ['static', 'public', 'private', 'protected', 'final', 'constant']:
            acc_sp: list = self.get_access_specifiers().keys()
            if name not in acc_sp:
                if name in ['public', 'private', 'protected']:
                    for spec in ['public', 'private', 'protected']:
                        if acc_sp.__contains__(spec):
                            acc_sp.remove(spec)
                            acc_sp.append(name)
                            break
                else:
                    acc_sp.append(name)
            self.set_attribute('access_spec', acc_sp)

    def get_access_specifiers(self) -> dict:
        return self.get_attribute('access_spec')
