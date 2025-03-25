import logging.config


# Generators
def even_numbers_generator(end_value: int):
    """ Even numbers generator. """
    current_value = 0
    while current_value <= end_value:
        yield current_value
        current_value += 2

def fibonacci_generator(number: int):
    """ Generate Fibonacci sequence with end 'number'. """
    prev_prev_number = 0
    prev_number = 1
    while prev_number <= number:
        prev_prev_number, prev_number = prev_number, prev_number + prev_prev_number
        yield prev_prev_number


# Iterators
class ReverseList:
    """ Iterator return element of sequence in reversed order """
    def __init__(self, obj: list):
        if not isinstance(obj, list):
            raise TypeError("Object must be a 'list' type")
        self.sequence = obj

    # Вирішив не реалізовувати метод __next__. Якщо завдання потребує, зроблю.
    def __iter__(self):
        for ind in range(len(self.sequence) - 1, -1, -1):
            yield self.sequence[ind]


class EvenNumbers:
    """ Iterator return even number from 0 to 'number' """
    def __init__(self, number: int):
        if not isinstance(number, int):
            raise TypeError("Object must be a 'int' type")
        self.number = number

    # Вирішив не реалізовувати метод __next__. Якщо завдання потребує, зроблю.
    def __iter__(self):
        current_number = 0
        while current_number <= self.number:
            yield current_number
            current_number += 2


# Decorators
def function_handle_decorator(func):
    """ Decorator that handle function workflow for results and exceptions. """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            log_message = f"Function {func.__name__} with arguments: {args} succeeded with result: {result}"
            logger.info(log_message)
        except Exception as e:
            log_message = f"Function {func.__name__} with arguments: {args} called an exception {e.__class__.__name__}({e})"
            logger.warning(log_message)
    return wrapper

@function_handle_decorator
def divide(a, b):
    return a / b


logging.config.fileConfig('logger_config.ini')
logger = logging.getLogger('hw17_logger')

if __name__ == '__main__':
    # chapter 1. Generators.
    even_numbers = even_numbers_generator(25)
    fibonacci_numbers = fibonacci_generator(100)
    print(list(even_numbers))
    print(list(fibonacci_numbers))
    # chapter 2. Iterators.
    reverse_list = ReverseList(['a', 'b', 'c', 'd'])
    even_numbers_iter = EvenNumbers(29)
    print(list(reverse_list))
    print(list(even_numbers_iter))
    # chapter 3. Decorators.
    # Decorator 'function_handle_decorator' works for both tasks in chapter.
    result_1 = divide(1, 1)
    result_2 = divide(10,'2')
