import pytest
from geometry_eval_class import Circle, Rectangle, Rhombus, Figure


@pytest.fixture
def setup_figures():
    return {
        'rectangle': Rectangle(side_a=10, side_b=25),
        'circle': Circle(radius=10),
        'rhombus': Rhombus(diameter_a=6, diameter_b=8),
    }


class TestGeometricalFigures:

    def test_rectangle_methods_positive(self, setup_figures):
        """ Test the square and perimeter methods of the Rectangle class with positive inputs. """
        expected_square = 250
        expected_perimeter = 70
        current_figure = setup_figures['rectangle']
        assert current_figure.square() == expected_square
        assert current_figure.perimeter() == expected_perimeter

    def test_circle_methods_positive(self, setup_figures):
        """ Test the square and perimeter methods of the Circle class with positive inputs. """
        expected_square = 157
        expected_perimeter = 62.8
        current_figure = setup_figures['circle']
        assert current_figure.square() == expected_square
        assert current_figure.perimeter() == expected_perimeter

    def test_rhombus_methods_positive(self, setup_figures):
        """ Test the square and perimeter methods of the Rhombus class with positive inputs. """
        expected_square = 24
        expected_perimeter = 20
        current_figure = setup_figures['rhombus']
        assert current_figure.square() == expected_square
        assert current_figure.perimeter() == expected_perimeter

    @pytest.mark.parametrize('figure, params, exception', [
        (Rectangle, {'side_a': '12', 'side_b': 20}, ValueError),
        (Circle, {'radius': -10}, ValueError),
        (Rhombus, {'diameter_a': 12}, TypeError)
    ])
    def test_invalid_data_for_instantiate(self, figure, params, exception):
        """ Test the instantiation of geometrical figures with invalid input data. """
        with pytest.raises(exception):
            figure(**params)

    def test_regret_to_instantiate_base_class(self):
        """ Test that instantiating the base Figure class raises a TypeError. """
        with pytest.raises(TypeError):
            Figure()
