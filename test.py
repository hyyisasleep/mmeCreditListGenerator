#
#
# list1 = [{"c":1},{"c":2},{"c":3}]
# list2 = list()
# def f1():
#     t1 = {"c":4}
#     list1.append(t1)
#     list2.append(t1)
#
# def f2():
#     t1 = {"c":8}
#     list1.append(t1)
#     list2.append(t1)
#
# f1()
#
# print("after append t1")
# print(list1)
# print(list2)
# # print("t1[c]=3")
# # t1["c"] = 3
# # print(list1)
# # print(list2)
# print("list1[3][c] = 0")
# list1[3]["c"] = 0
# print(list1)
# print(list2)
# print("list1[3][c] = 2")
# list1[3]["c"] = 2
# f2()
# print(list1)
# print(list2)
# # for l1 in list1:
# #     list2.append(l1)
# #
# # list2[0]["c"] = 3
# #
# # print(list1)
# # print(list2)

# datas = [{"c":1},{"c":2}]
#
# class MyData():
#     def __init__(self,datas):
#         self.datas = datas
#         self.datas = [{"c":2},{"c":8}]
#         self.datas[0]["c"] = 3
#
# ndata = MyData(datas)
# print(ndata.datas)
# print(datas)

l = [1,2,3,4]

for i in range(len(l)):
    print("char " +str(l[-(i+1)]))
