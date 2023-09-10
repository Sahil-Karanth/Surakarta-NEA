class Test:

    def __init__(self, name):
        self.__name = name

    
    def do_something(self, word):
        raise NotImplementedError("Subclass must implement abstract method")
    

class Test2(Test):

    def __init__(self, name):
        super().__init__(name)

    def do_something(self):
        print("do something")



x = Test2("test")

x.do_something()