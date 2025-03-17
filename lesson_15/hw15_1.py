class Rhombus:
    def __init__(self, *, side:float, angle_a:float):
        # Creating 'attributes names' list.
        super().__setattr__('angles', ['angle_a', 'angle_b'])
        # Initiating start values. Triggering __setattr__ method.
        self.side = side
        self.angle_a = angle_a

    def __str__(self):
        return f"Rhombus parameters: side={self.side}, angleA={self.angle_a}, angleB={self.angle_b}"

    def __setattr__(self, name, value):
        # Check the presence of attribute name is attributes class dict.
        if name == 'side' or name in self.__dict__['angles']:
            if isinstance(value, int | float):
                if name == 'side' and value > 0:
                    super().__setattr__(name, value)
                elif 0 < value < 180:
                    # Looping and processing all angle values, while passing to __setattr__ one angle value.
                    for item in self.__dict__['angles']:
                        if name == item:
                            super().__setattr__(name, value)
                        elif name in self.__dict__['angles']:
                            super().__setattr__(item, 180 - value)
                else:
                    raise ValueError(f"Value error: '{name}'={value}, not in range")
            else:
                raise TypeError(f"Type error: '{value}' must be integer/float type. Current type: {type(value).__name__}")
        else:
            raise AttributeError(f"Undefined attribute: {name}")


if __name__=='__main__':
    res = Rhombus(side=19, angle_a=15)
    print(res)
    res.angle_b = 10
    res.side = 12.5
    print(res)
    res.angle_a = 179
    print(res)
