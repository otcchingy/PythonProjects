from utils.base.myvarp_class import MyvarpClass


class MyvarpFunction(MyvarpClass):

    def __init__(self, scope=None, script: str = "", **kwargs):
        super().__init__(scope, script, **kwargs)
        self.set_name("MyvarpFunction")

    def to_string(self):
        return f'[object Function<{self.get_name()}>]'
