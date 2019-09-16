import sys
from MyvarpRunner import MyvarpRun
from utils.base.myvarp_script_interpreter import MyvarpScriptInterpreter


class MyvarpCompile:
    session = MyvarpRun()

    def __init__(self, file_path):
        with open(str(file_path), 'r') as file:
            for i, line in enumerate(file):
                self.session.run(line)
                if 'Error' in str(self.session.output) or 'Exception' in str(self.session.output):
                    sys.exit(self.session.output + "  at [line {}]".format(i + 1))


class NewMyvarpCompile:
    session: MyvarpScriptInterpreter

    def __init__(self, file_path):
        with open(str(file_path), 'r') as file:
            self.session = MyvarpScriptInterpreter(name=file.name, path=file_path)
            for i, line in enumerate(file):
                self.session.add_line(line+"\n")
                self.session.run_script()
            self.session.add_line('\n')
            self.session.run_script()


# c = NewMyvarpCompile('C:/Users/Otc_Chingy/PycharmProjects/MyvarpLanguageInterpreter/test.txt')
