# (a/b)&c
class Memory:
    a = []
    b = []
    c = []

    def enter_lists(self):
        print("Enter list elements splitting them by space\n")
        print("A = ")
        self.a = [x for x in input().split()]
        print("B = ")
        self.b = [x for x in input().split()]
        print("C = ")
        self.c = [x for x in input().split()]


def list_diff_list(l1, l2):
    return [l1[i] for i in range(len(l1)) if l1[i] not in l2]


def list_con_list(l1, l2):
    return [l1[i] for i in range(len(l1)) if l1[i] in l2]


obj = Memory()
obj.enter_lists()
print(list_con_list(list_diff_list(obj.a, obj.b), obj.c))
