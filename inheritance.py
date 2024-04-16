class WithInit:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I am {self.name}. Nice to meet you!"

class WithoutInit:
    def greet(self):
        return "Hello, I am a class without __init__ function. Nice to meet you!"

def call_with_init():
    with_init_obj = WithInit("Alice")
    print(with_init_obj.greet())  

def call_without_init():
    without_init_obj = WithoutInit()
    print(without_init_obj.greet())  

# Call the functions to demonstrate
call_with_init()
call_without_init()