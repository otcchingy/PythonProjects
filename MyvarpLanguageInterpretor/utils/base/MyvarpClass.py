from MyvarpLanguageInterpretor.utils.base.MyvarpObject import MyvarpObject


class MyvarpClass(MyvarpObject):

    def __init__(self):
        super().__init__()

    def set_name(self, name: str):
        self.set_attribute('name', name)

    def get_name(self) -> str:
        return self.get_attribute('name')

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
