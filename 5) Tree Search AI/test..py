import copy

class Test:
    def __init__(self, name):
        self.name = name



class Test2:

    def __init__(self, name):
        self.test_obj = Test(name)

        self.test_copy = copy.deepcopy(self.test_obj)



x = Test2("test")
