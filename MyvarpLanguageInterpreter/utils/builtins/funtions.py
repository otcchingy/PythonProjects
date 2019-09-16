from utils.base.myvarp_function import MyvarpFunction
from utils.base.myvarp_script_interpreter import MyvarpScriptInterpreter


class Display(MyvarpFunction):

    def __init__(self, scope: MyvarpScriptInterpreter, script="", expression_data=None):
        super().__init__(scope, script, expression_data)
        self.set_name('display')
        self.add_positional_param('line', '')
        self.add_positional_param('sep', ', ')
        self.add_positional_param('end', '\n')

        def call(args):

            keys = list(args.keys())
            line = args['line'] if 'line' in keys else 'line'
            sep = args['sep'] if 'sep' in keys else 'sep'
            end = args['end'] if 'end' in keys else 'end'

            print(
                self.get_interpreter().evaluate_line(line),
                sep=self.get_interpreter().evaluate_line(sep),
                end=self.get_interpreter().evaluate_line(end),
            )

        self.set_attribute('call', call)


class Decision(MyvarpFunction):

    def __init__(self):
        super().__init__()


# parent = MyvarpScriptInterpreter()
# parent.evaluate_line("name = 'bernard'")
# # parent.evaluate_line("age = 21")
# display = Display(scope=parent)
# display.call({'line': 'name'})