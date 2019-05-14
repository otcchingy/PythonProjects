import pandas as pd


# import json
#
# data = json.load(open("supermarkets.json"))
#
# file = open("supermarkets_c.txt", "w")
#
# file.write("{},{},{},{},{},{},{}\n".format("ID","Address", "City", "State", "Country", "Name", "Employees"))
# for i in data:
#     file.write("{}, {}, {}, {}, {}, {}, {}\n"
#                .format(i["ID"], i["Address"], i["City"], i["State"], i["Country"], i["Name"], i["Employees"]))



def add_row(dataframe : pd.core.frame.DataFrame, parameters):
    dft = dataframe.T
    try:
        dft[parameters[0]] = parameters[1:]
        return dft.T
    except Exception:
        print("An Error Occurred...Check if all columns have been properly assigned")


def drop_row(dataframe : pd.core.frame.DataFrame, index):
    # noinspection PyBroadException
    try:
        dataframe = dataframe.drop(index, 0)
        return dataframe
    except Exception:
        print("An Error Occurred...Check if the indexes exist")


def drop_column(dataframe : pd.core.frame.DataFrame, index):
    # noinspection PyBroadException
    try:
        dataframe = dataframe.drop(index, 1)
        return dataframe
    except Exception:
        print("An Error Occurred...Check if the columns exist")
