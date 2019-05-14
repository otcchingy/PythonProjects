"""

Author : chingy
This script defines words that are passes in.
could be a word or a bunch of words
use define.py -h or --help for help

"""

import sys

from dictionary import get_meaning_of

args = sys.argv


def main(argv):

    if len(argv) > 0:
        if argv[0] == "-h" or argv[0] == "-help":
            print("\ndefine [word] || define [word1 word2 ....words]")
        else:
            for word in argv:
                print("\n( {} )".format(word))
                get_meaning_of(word)
    else:
        print("\ndefine [word] || define [word1 word2 ....words]")


if __name__ == "__main__":
    main(args[1:])


# # !/usr/bin/python3
# import sys, getopt
#
# def main(argv):
#     inputfile = ''
#     outputfile = ''
#     try:
#         opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
#     except getopt.GetoptError:
#         print('test.py -i <inputfile> -o <outputfile>')
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print('test.py -i <inputfile> -o <outputfile>')
#             sys.exit()
#         elif opt in ("-i", "--ifile"):
#             inputfile = arg
#         elif opt in ("-o", "--ofile"):
#             outputfile = arg
#             print('Input file is "', inputfile)
#             print('Output file is "', outputfile)
#
#
# if __name__ == "__main__":
#     main(sys.argv[1:])
