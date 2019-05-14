import sys
from MyvarpRunner import MyvarpRun

class MyvarpCompile:

    session = MyvarpRun()

    def __init__(self, file_path):
        with open(str(file_path), 'r') as file:
            for i, line in enumerate(file):
                self.session.run(line)
                if 'Error' in str(self.session._output) or 'Exception' in str(self.session._output):
                    sys.exit(self.session._output+"  at [line {}]".format(i+1))
