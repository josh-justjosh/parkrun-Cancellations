def rem_dups(data_with_dups):
    '''removes duplicates from a list'''
    return list(dict.fromkeys(data_with_dups))


def sort_by_index_0(e):
    '''sorts by the first item in the list'''
    return e[0]


def sort_by_index_1(e):
    '''sorts by the second item in the list'''
    return e[1]
