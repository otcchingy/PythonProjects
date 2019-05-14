import json
from difflib import get_close_matches


data = json.load(open('dictionary.json'))


def wrap(sentence, length):
    sentence = str(sentence)
    new_sentence = ""
    retStr = ""
    if len(sentence) > length:
        for word in sentence.split(" "):
            if len(new_sentence + word) > length:
                new_sentence += "\n"
                retStr += new_sentence
                new_sentence = word + " "
            else:
                new_sentence += word + " "
        retStr += new_sentence
        return retStr
    else:
        return sentence


def get_meaning_of(phrase):
    phrase = phrase.lower()
    if phrase in data:
        meaning = data[phrase]
        for i in range(len(meaning)):
            print("\nDefinition ", i + 1, " : ")
            print(wrap(meaning[i], 60))
    else:
        print("\nThe word you entered does not exist in this Dictinary")
        matches = get_close_matches(phrase, data.keys())
        if len(matches) > 0:
            ans = str(input("Did you mean {} ? (y/n) : ".format(matches[0])))
            while ans.lower() != "y" and ans.lower() != "n":
                ans = str(input("please enter y or n : "))
            if ans == "y":
                get_meaning_of(matches[0])


if __name__ == "__main__":
    print("############################################################")
    print("##        welcome to chingy's dictionary ...v 1.0         ##")
    print("##                  to quit enter ':q'                    ##")
    print("############################################################")

    while True:
        word = str(input("\nEnter a word : "))
        if word != ":q":
            get_meaning_of(word)
        else:
            print("\n############################################################")
            print("##                      Goodbye...                        ##")
            print("############################################################")
            break
