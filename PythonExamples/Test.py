'''
import os.path

def savefile():
    save_path = str(input("\npaste the Path you wish to save the file :  "))
    name = str("Crpytoread")
    completeName = os.path.join(save_path, name + ".txt")
    with open(completeName, 'w') as file:
        file.write(text)
        file.close()
    print("\nCheck the directory {}/crytocode.txt for your Decrpyted Message".format(save_path))
    time.sleep(1)

text = "I am the text"
savefile()

record = open('file.txt', 'w')
record.write("sdfsdfdfsdfsds dfsd yuyds hj jkf udhfiusdhfhdfh jkfhskjdhf jkhfjksd\n")
record.write("rejktvnrj jkfmfdm jkhfjksd\n")
record.close()

reader = open('file.txt', 'r')
for line in reader:
    print(line)
lines = reader.read()
reader.close()


print(lines)
print(lines.count('f'))
'''

'''
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
        print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])
    print(keywords)


cheeseshop('sdfcsdf','dfadfdf','sdsadasdd',
            me='you',
            num=1,
            name='sexy')

'''