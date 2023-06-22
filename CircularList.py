class CircularList:

    def __init__(self, lst):
        self.__lst = lst

    def __str__(self):
        return self.__lst
    
    def __getitem__(self, i):
        return self.__lst[i % len(self.__lst)]        


c = CircularList([1,2,3])

count = 0
for i in c:
    print(i)
