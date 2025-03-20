from abc import ABC, abstractmethod
from math import sqrt
from random import randint, choice
import inspect


class Figure(ABC):
    @abstractmethod
    def square(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def __setattr__(self, key, value):
        if not isinstance(value, int | float) or value < 0:
            raise ValueError(f"Enter correct type/value of parameter: {key[key.find('__') + 2:]}={value}")
        super().__setattr__(key, value)

    def __str__(self):
        params = []
        for key, value in self.__dict__.items():
            formatted_key = key[key.find('__') + 2:]
            params.append(f"{formatted_key}={value}")
        return f"Об'єкт '{self.__class__.__name__}' з параметрами: {', '.join(params)}"


class Circle(Figure):
    def __init__(self, *, radius: [int, float]):
        self.__radius = radius

    def square(self):
        return round(3.14 * pow(self.__radius, 2) / 2, 2)

    def perimeter(self):
        return round(2 * 3.14 * self.__radius, 2)


class Rhombus(Figure):
    def __init__(self, *, diameter_a, diameter_b):
        self.__diameter_a = diameter_a
        self.__diameter_b = diameter_b

    def square(self):
        return round((self.__diameter_a * self.__diameter_b) / 2)

    def perimeter(self):
        side_a = self.__diameter_a / 2
        side_b = self.__diameter_b / 2
        side_c = sqrt(pow(side_a, 2) + pow(side_b, 2))
        return round(side_c * 4, 2)


class Rectangle(Figure):
    def __init__(self, *, side_a, side_b):
        self.__side_a = side_a
        self.__side_b = side_b

    def square(self):
        return self.__side_a * self.__side_b

    def perimeter(self):
        return (self.__side_a + self.__side_b) * 2


if __name__ == '__main__':
    # Dinamycally instantiate classes with random params.
    figures_cls = [Circle, Rectangle, Rhombus]
    for obj_num in range(10):
        obj_kwargs = {}
        obj_class = choice(figures_cls)
        # Get params of current class and fill them random values.
        obj_class_params = inspect.signature(obj_class).parameters
        for parameter_name, parameter_value in obj_class_params.items():
            obj_kwargs[parameter_name] = randint(1, 100)
        instance = obj_class(**obj_kwargs)
        print(instance)
        print(f"Проведені наступні обчислення: Площа - {instance.square()}, Периметр - {instance.perimeter()}")
