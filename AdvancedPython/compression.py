import random


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(dict_size))

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    #from cStringIO import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(dict_size))

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop

    ##result = StringIO()
    w = compressed.pop(0)
    ##result.write(w)
    result = ""
    result+=w
    for k in compressed:
        print("w = ", w)
        print("k = ", k)
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        print("entry = ",entry, "\n\n")
        ##result.write(entry)
        result+=entry

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result ##result.getvalue()


# How to use:

txt = 'my name is Bernard atinga , now the story of bernard begins in a small town gore where everyone loves'
txt2 = 'TOBEORNOTTOBEORTOBEORNOT'
compressed = compress(txt2)
print (compressed)
decompressed = decompress(compressed)
print (decompressed ,(decompressed == txt2))

print(len(compressed))
print(len(decompressed))
print(len(decompressed) - len(compressed))