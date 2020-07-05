import os
import sys
import datetime

from MyvarpCompiler import MyvarpCompile, NewMyvarpCompile
from utils.base.myvarp_script_interpreter import MyvarpScriptInterpreter

args = sys.argv

"""
        session = MyvarpScriptInterpreter()
        # session.read("", _return=True)
        while True:
            if session.process_output == "...":
                line = input('   ... ')
                session.add_line(line)
                session.run_line()
            else:
                line = input('mv >>> ')

                if str(line) == 'exit()' or str(line) == 'quit()' or str(line) == ':q':
                    break
                elif str(line) == 'clear()' or str(line) == 'clean()':
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    session.add_line(line)
                    session.run_line()

"""


def main(argv):
    if len(argv) > 0:
        if argv[0] == "-h" or argv[0] == "-help":
            print("\nhelp on Myvarp ..how to run how to convert to python file")
        else:
            NewMyvarpCompile(argv[0], argv=argv)
    else:
        print("#"*110)
        print("##"+(" "*34)+"Myvarp By TechupStudio @Copyright "+str(datetime.datetime.now().year)+(" "*34)+"##")
        print("##"+(" "*42)+"Version 1.0 Build 0001"+(" "*42)+"##")
        print("#"*110+"\n")

        session = MyvarpScriptInterpreter()

        while True:

            if session.is_comments_active():
                line = input('   ... ')
                session.add_line(line+"\n")
                session.run_script()
                if session.has_error():
                    session.show_error()
                    session.clear_error()
                else:
                    result = session.get_result()
                    if result is not None:
                        if isinstance(result, list):
                            for output in result:
                                print(output)
                        else:
                            print(result)
                    session.clear_result()

            else:
                line = input('mv >>> ')

                if str(line) == 'exit()' or str(line) == 'quit()' or str(line) == ':q':
                    break
                elif str(line) == 'clear()' or str(line) == 'clean()':
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    session.add_line(line+"\n")
                    session.run_script()
                    if session.has_error():
                        session.show_error()
                        session.clear_error()
                    else:
                        result = session.get_result()
                        if result is not None:
                            if isinstance(result, list):
                                for output in result:
                                    print(output)
                            else:
                                print(result)
                        session.clear_result()


if __name__ == "__main__":
    main(args[1:])
