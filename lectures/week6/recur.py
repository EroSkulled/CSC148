#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled


def first_at_depth(obj, d) -> int:

    if isinstance(obj, int):
        if d == 0:
            return obj
        else:
            return None

    else:
        for sublist in obj:
            tmp = first_at_depth(sublist, d - 1)
            if not tmp:
                tmp = first_at_depth(sublist, d - 1)
            else:
                return tmp
        return None


def add_one(obj):
    if isinstance(obj, int):
        pass
    else:
        for i in range(len(obj)):
            if isinstance(obj[i], int):
                obj[i] += 1
            else:
                add_one(obj[i])


    # a = d
    # if isinstance(obj, int):
    #     if d == 0:
    #         return obj
    #     else:
    #         return None
    # else:
    #     for sublist in obj:
    #         a += 1
    #         tmp = first_at_depth(sublist, a)
    #         if d == a:
    #             return tmp
    #         else:
    #             tmp = first_at_depth(sublist, a)
    # return None

a = 0
b = [0, 1]
c = [0,1,2, [3, 4]]
add_one(a)
add_one(b)
add_one(c)
print(c)
print(a)
print(b)

