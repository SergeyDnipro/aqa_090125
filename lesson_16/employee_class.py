from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, *, name, salary, team=None):
        self.name = name
        self.salary = salary
        self.team = team if isinstance(team, Teamlead) else None

    def add_to_team(self, new_team):
        if isinstance(new_team, Teamlead) and self not in new_team.team_person_list:
            if self.team:
                self.team.team_size -= 1
                self.team.team_person_list.remove(self)
            self.team = new_team
            new_team.team_size += 1
            new_team.team_person_list.append(self)

    def __repr__(self):
        return f"name:{self.name}/position:{self.employee_classname()}"

    @abstractmethod
    def employee_classname(self):
        pass


class Manager(Employee):
    def __init__(self, *, name, salary, department, team=None, **kwargs):
        super().__init__(name=name, salary=salary, **kwargs)
        self.department = department

    def employee_classname(self):
        return self.__class__.__name__


class Developer(Employee):
    def __init__(self, *, name, salary, programming_language, team=None, **kwargs):
        super().__init__(name=name, salary=salary, **kwargs)
        self.programming_language = programming_language

    def employee_classname(self):
        return self.__class__.__name__


class Teamlead(Manager, Developer):
    def __init__(self, *, name, salary, department, programming_language, team_name):
        super().__init__(name=name, salary=salary, department=department, programming_language=programming_language)
        self.team_size = 0
        self.team_name = team_name
        self.team_person_list = []

    def __repr__(self):
        return f"Teamlead '{self.name}', team_name: '{self.team_name}', stuff: {self.team_person_list}"


if __name__ == '__main__':
    obj1 = Manager(name='Jack', salary=1000, department='marketing')
    obj2 = Developer(name='Vader', salary=1500, programming_language='python')
    obj3 = Developer(name='Darth', salary=2500, programming_language='C#')
    obj4 = Teamlead(name='Jonh', salary=3000, department='development', programming_language='Java', team_name='StarGoose')
    obj5 = Teamlead(name='Luke', salary=1999, department='development', programming_language='C++', team_name='Goliath')

    obj2.add_to_team(obj4)
    print(obj4.team_person_list)
    print(obj4.team_size)
    obj3.add_to_team(obj4)
    print(obj4.team_person_list)
    print(obj4.team_size)
    # obj2.add_to_team(obj5)
    print(obj4.team_person_list)
    print(obj5.team_person_list)
    print(obj4)
    obj1.add_to_team(obj4)
    print(obj4)
    print(obj4.team_size)

    # print(obj4.team_size)
    # obj3.add_to_team(obj4)
    # obj2.add_to_team(obj4)
    # print(obj4.team_size)
    # print(obj4.salary)
    # obj3.add_to_team(obj5)
    # obj3.add_to_team(obj5)
    # obj1.add_to_team(obj3)
    # print(obj4.team_size)
    # print(obj5.team_size)
    # print(obj5.employee_classname())
    # print(obj1.employee_classname())
    # obj1.add_to_team(obj4)
    # print(obj4.team_size)
    # print(obj4.team_person_list)
    # print(obj5.team_person_list)