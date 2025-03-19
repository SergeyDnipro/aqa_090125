import pytest
from employee_class import Teamlead, Manager, Developer, Employee


@pytest.fixture
def employee_instances():
    return {
        'manager1': Manager(name='Alice Cooper', salary=1000, department='HR'),
        'developer1': Developer(name='Robert Plant', salary=1500, programming_language='Python'),
        'developer2': Developer(name='Clint Eastwood', salary=2500, programming_language='JS'),
        'developer3': Developer(name='Evil Pokemon', salary=2500, programming_language='Python'),
        'teamlead1': Teamlead(name='Luke Skywalker', salary=3000, department='frontend',
                              programming_language='TypeScript', team_name='StarGoose'),
        'teamlead2': Teamlead(name='Marty McFly', salary=1999, department='backend', programming_language='Python',
                              team_name='Goliath'),
    }


class TestTeamleadClass:

    def test_instantiating_base_class(self):
        """ Test that instantiating the abstract Employee superclass raises a TypeError. """
        with pytest.raises(TypeError):
            Employee(name='Alex', salary=2999)

    def test_attributes_in_teamlead_instance_exists(self, employee_instances):
        """ Test that a Teamlead instance has all the required attributes. """
        assert hasattr(employee_instances['teamlead2'], 'name')
        assert hasattr(employee_instances['teamlead2'], 'salary')
        assert hasattr(employee_instances['teamlead2'], 'department')
        assert hasattr(employee_instances['teamlead2'], 'programming_language')
        assert hasattr(employee_instances['teamlead2'], 'team_size')

    def test_attributes_in_teamlead_instance(self, employee_instances):
        """ Test that a Teamlead instance has the correct attribute values. """
        expected_name = 'Marty McFly'
        expected_salary = 1999
        expected_department = 'backend'
        expected_programming_language = 'Python'
        expected_team_size = 0
        assert employee_instances['teamlead2'].name == expected_name
        assert employee_instances['teamlead2'].salary == expected_salary
        assert employee_instances['teamlead2'].department == expected_department
        assert employee_instances['teamlead2'].programming_language == expected_programming_language
        assert employee_instances['teamlead2'].team_size == expected_team_size

    def test_teamlead_team_size_changed(self, employee_instances):
        """ Test the process of developers joining and leaving a Teamlead's team. Changed 'team_size'. """
        employee_instances['developer1'].add_to_team(employee_instances['teamlead2'])
        employee_instances['developer2'].add_to_team(employee_instances['teamlead2'])
        employee_instances['developer3'].add_to_team(employee_instances['teamlead2'])
        assert employee_instances['teamlead2'].team_size == 3
        employee_instances['developer2'].add_to_team(employee_instances['teamlead1'])
        assert employee_instances['teamlead2'].team_size == 2

    def test_developer_instance_in_team(self, employee_instances):
        """ Test the presence of developer instances in a Teamlead's team. """
        employee_instances['developer1'].add_to_team(employee_instances['teamlead2'])
        employee_instances['developer2'].add_to_team(employee_instances['teamlead2'])
        employee_instances['developer3'].add_to_team(employee_instances['teamlead2'])
        assert employee_instances['developer1'] in employee_instances['teamlead2'].team_person_list
        assert employee_instances['developer2'] in employee_instances['teamlead2'].team_person_list
        assert employee_instances['developer3'] in employee_instances['teamlead2'].team_person_list
        employee_instances['developer2'].add_to_team(employee_instances['teamlead1'])
        assert employee_instances['developer2'] not in employee_instances['teamlead2'].team_person_list

    def test_invalid_data_while_join_team(self, employee_instances):
        """ Test the behavior when a developer attempts to join an invalid team. """
        employee_instances['developer1'].add_to_team(employee_instances['manager1'])
        assert employee_instances['developer1'].team is None
