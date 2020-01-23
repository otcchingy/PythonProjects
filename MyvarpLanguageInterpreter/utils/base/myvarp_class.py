from utils.base.myvarp_object import MyvarpObject


class MyvarpClass(MyvarpObject):

    def __init__(self, scope=None, script: str = "", **kwargs):
        super().__init__(parent=scope, script=script, **kwargs)
        self.set_name('MyvarpClass')

    def set_name(self, name: str):
        self.set_attribute('name', name)

    def get_name(self) -> str:
        return self.get_attribute('name')

    def construct(self, args):
        self.call(args)
        self.get_interpreter().run_script()

    def add_property(self, key, value):
        self.set_attribute(key, value)

    def get_property(self, key):
        self.get_attribute(key)

    def inherit_from_class(self, myvarpclass):
        self.add_parent(myvarpclass)
