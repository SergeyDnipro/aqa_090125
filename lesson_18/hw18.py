import logging
import logging.config


def logging_factorial(func):
    def wrapper(value, **kwargs):
        if not isinstance(value, int):
            logger.error("TypeError: 'value' must be 'int' type.")
            return
        for result, i in func(value):
            log_message = f"Calling {func.__name__}({i}); Result: {result}"
            logger.info(log_message)
    return wrapper

@logging_factorial
def factorial_generator(end_value):
    """ Generator that produce factorial of numbers from 0 to 'end_value'. """
    result = 1
    for i in range(end_value + 1):
        result *= i if i != 0 else result
        yield result, i


logging.config.fileConfig('logger_config.ini')
logger = logging.getLogger('hw17_logger')

if __name__ == '__main__':
    factorial_seq = factorial_generator(10)