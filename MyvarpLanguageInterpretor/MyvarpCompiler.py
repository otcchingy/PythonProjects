import sys
from MyvarpLanguageInterpretor.MyvarpRunner import MyvarpRun
from MyvarpLanguageInterpretor.MyvarpScriptManager import MyvarpScriptReader


class MyvarpCompile:

    session = MyvarpRun()

    def __init__(self, file_path):
        with open(str(file_path), 'r') as file:
            for i, line in enumerate(file):
                self.session.run(line)
                if 'Error' in str(self.session.output) or 'Exception' in str(self.session.output):
                    sys.exit(self.session.output + "  at [line {}]".format(i + 1))


class NewMyvarpCompile:

    session: MyvarpScriptReader

    def __init__(self, file_path):
        with open(str(file_path), 'r') as file:
            self.session = MyvarpScriptReader(name=file.name, path=file_path)
            for i, line in enumerate(file):
                self.session.run(line)


c = NewMyvarpCompile('C:/Users/Otc_Chingy/PycharmProjects/MyvarpLanguageInterpretor/test.txt')