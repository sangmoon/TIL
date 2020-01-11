def quick_sort(lst):
    if len(lst) == 0 or len(lst) == 1:
        return lst
    pivot = lst.pop(len(lst)//2)
    return quick_sort(list(filter(lambda x: x < pivot, lst))) + [pivot] + quick_sort(list(filter(lambda x: x >= pivot, lst)))


if __name__ == "__main__":
    lst = [4,6,8,1,4,5,9,67,8,1,2]
    print(quick_sort(lst))
