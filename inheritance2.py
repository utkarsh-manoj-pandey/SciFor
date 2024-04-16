class Animal:
    def __init__(self, name):
        self.name = name

class Bird(Animal):
    def fly(self):
        print(f"{self.name} is flying.")

    def sing(self):
        print(f"{self.name} is singing.")

    def swim(self):
        print(f"{self.name} is swimming.")

class Department:
    def __init__(self, name):
        self.name = name

class Post:
    def __init__(self, title):
        self.title = title

class Employee(Department, Post):
    def __init__(self, name, department, post):
        super().__init__(department)
        super().__init__(post)
        self.name = name
        self.department = department
        self.post = post

    def display_info(self):
        print(f"Name: {self.name}, Department: {self.department.name}, Post: {self.post.title}")

# Example usage
bird1 = Bird("Sparrow")
bird1.fly()   # Output: Sparrow is flying.

bird2 = Bird("Penguin")
bird2.swim()  # Output: Penguin is swimming.

department = Department("HR")
post = Post("Manager")
employee = Employee("John Doe", department, post)
employee.display_info()  # Output: Name: John Doe, Department: HR, Post: Manager