# Using advanced concepts in Python

# Decorator function to measure the time taken by a function to execute
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper

# Class with getter and setter methods
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

# Lambda function to perform a simple operation
add = lambda x, y: x + y

# Generator function to generate Fibonacci sequence
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Map function to apply a function to each element of a list
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))

# Decorated function to calculate factorial
@timer
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Using all the advanced concepts
if __name__ == "__main__":
    # Getter and setter
    person = Person("Stud1", 30)
    print(f"Name: {person.name}, Age: {person.age}")
    person.name = "Stud2"
    person.age = 25
    print(f"Updated Name: {person.name}, Updated Age: {person.age}")

    # Lambda function
    print("Sum using lambda function:", add(5, 3))

    # Generator
    print("Fibonacci sequence:", list(fibonacci(10)))

    # Map function
    print("Squared numbers:", squared_numbers)

    # Decorated function
    print("Factorial of 5 is:", factorial(5))
