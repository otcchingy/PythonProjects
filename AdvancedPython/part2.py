from collections import deque
import random

def raise_to(exp):
    def power(x):
        return pow(x, exp)
    return  power



def fullname(function):
    def take_args(*args, **kwargs):
        function_result = function(*args, **kwargs)
        # do somethings with the function results
        # and return another result
        print(args, function_result)



    return take_args


@fullname
def name(*args):
    full = ''
    for name in args:
        full+= name+' '
    return full


def printArray(array):
    for i in range(len(array)):
        if i % 20 == 0:
            print()
        print(array[i]," ", end='')


def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp
    return array

def pushArray(array, old_index, new_index):
    if old_index < new_index:
        new_array = []
        for i in range(len(array)):
            if old_index <= i < new_index:
                new_array.append(array[i+1])
            elif i == new_index:
                new_array.append(array[old_index])
            else:
                new_array.append(array[i])
        return new_array


def pushSort(array):
    if len(array) > 1:
        for i in range(len(array)):
            for j in range(1, len(array)):
                if array[i] > array[-j] and i < len(array) - j:
                    array = pushArray(array, i, len(array) - j)
        return array

def swapSort(array):
    if len(array) > 1:
        for i in range(len(array)):
            for j in range(1,len(array)-i):
                if array[j-1] > array[j]:
                    array = swap(array, j-1, j)
        return array


def oldSort(array):
    if len(array) > 1:
        new, old = [],[1]
        for i in range(len(array)):
            if new == old:
                break;
            for j in range(1,len(array)-i):
                if array[j-1] > array[j]:
                    array = swap(array, j-1, j)
                    new = array
                printArray(array)
                print("\n\n")
            print("new : ")
            printArray(new)
            print("old : ")
            printArray(old)
            old = new
        return array


# def divideSort(array):
#     if len(array) > 1:
#         imin, imax, = 0, -1
#         for i in range(1,len(array)):
#             for j in range(i,len(array)-i):
#                 if array[j] < array[imin]:
#                     imin = j-1
#                 if  array[-(j+1)] > array[imax]:
#                     imax = -(j+1)
#                 print("min = ", array[imin], "\t\tmax = ", array[imax])
#             array = swap(array, imin, i)
#             array = swap(array, imax, -i)
#             printArray(array)
#             print("\n\n")
#         printArray(array)
#         return array

# a = [ 13,151, 5 ,18 , 405 , 594 , 111 , 983 , 878,  855,  746]
#
# a = list(a)

# divideSort(a)

# import time




# for i in range(10):
# a = [i for i in (random.sample(range(1000), 20))]
# start = time.time()
# ss = swapSort(a)
# end = time.time()
# print("\n\nswapSort")
# print(end - start, "\n\n")
# printArray(ss)

# start = time.time()
# ans = pushSort(a)
# end = time.time()
# print("\n\npushSort")
# print(end-start,"\n\n")
# printArray(ans)
# start = time.time()
# s = oldSort(a)
# end = time.time()
# print("\n\noldSort")
# print(end-start,"\n\n")
# printArray(s)
# start = time.time()
# s = sorted(a)
# end = time.time()
# print("\n\nSorted")
# print(end-start,"\n\n")
# printArray(s)

# chingy.debillz@gmail.com# [a-z\.]+@[a-z]+\.[a-z]+
#
# 0553567950 # [0-9]+
#
# len(chi646ngy) #len\([0-z]+\)