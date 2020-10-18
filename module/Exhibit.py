from pprint import pprint

def checker(dic, essential_list, debug_FLAG=0):
    essential_list_FLAG = {}

    print("> checker >>>>>>>>>>>>")
    if debug_FLAG : pprint(dic.form)
    for k in essential_list:
        if dic.form[k] is not '':
            print(dic.form[k])
            essential_list_FLAG[k] = 1
        else:
            essential_list_FLAG[k] = 0

    if debug_FLAG : pprint(essential_list)
    if debug_FLAG : pprint(essential_list_FLAG)

    if dic.files["file"].filename:
        essential_list_FLAG["file"] = 1
    else:
        essential_list_FLAG["file"] = 0

    return essential_list_FLAG


def checker_init(essential_list, debug_FLAG=0):
    essential_list_FLAG = {}
    for k in essential_list:
        essential_list_FLAG[k] = 1
    
    essential_list_FLAG["file"] = 1
    return essential_list_FLAG


if __name__ == "__main__":
    print()
    pass