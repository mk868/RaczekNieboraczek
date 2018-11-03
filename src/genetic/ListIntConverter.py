
def Int2List(num, listSize):
    """
    Converts int to list
    Example input:
    9, 6
    output:
    [0, 0, 1, 0, 0, 1]
    """
    result = [0] * listSize

    for i in range(0, listSize):
        if num &  2 ** (listSize - i - 1):
            result[i] = 1 

    return result

def List2Int(lst):
    """
    Converts list to int
    Example input:
    [1, 1, 0]
    output:
    6
    """
    num = 0
    listSize = len(lst)
    for i in range(0, listSize):
        num += lst[i] * 2 ** (listSize - i - 1)

    return num


if __name__ == '__main__': # test
    print('list -> int')
    l = [1, 0, 1, 1, 1]
    print(l)
    print(List2Int(l))
    print('int -> list')
    print(23)
    print(Int2List(23, 6))