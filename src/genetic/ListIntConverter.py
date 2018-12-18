
def Int2List(num, listSize):
    """
    Converts int to list
    Example input:
    9, 6
    output:
    [0, 0, 1, 0, 0, 1]
    """
    return [b == '1' for b in bin(num)[2:].rjust(listSize)]

def List2Int(lst):
    """
    Converts list to int
    Example input:
    [True, True, False]
    output:
    6
    """
    #return sum(v<<i for i, v in enumerate(lst[::-1]))
    return int(''.join('1' if i else '0' for i in lst), 2)


if __name__ == '__main__': # test
    print('list -> int')
    l = [1, 0, 1, 1, 1] #23
    print(l)
    print(List2Int(l))
    print('int -> list')
    print(23)
    print(Int2List(23, 6))