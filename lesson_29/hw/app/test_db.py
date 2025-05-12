import pytest
from main import add_x_y, pow_x_y, update_description, get_record, delete_record
from logger_conf import logger
from conftest import logger_decorator


@logger_decorator(logger)
@pytest.mark.parametrize(
    "value_1, value_2, expected_result",
    [
        (1, 2, 3),
        (100, -100, 0),
    ])
def test_add_function_positive(request, db_for_testing, value_1, value_2, expected_result):
    result = add_x_y(db_instance=db_for_testing, value_1=value_1, value_2=value_2)

    assert result == expected_result
    return f"Function: 'add_x_y', value1={value_1}, value2={value_2}, actual result={result}, expected result={expected_result}"


@logger_decorator(logger)
@pytest.mark.parametrize(
    "value_1, value_2, expected_result",
    [
        (8, 2, 64),
        (100, 2, 10000),
    ])
def test_pow_function_positive(request, db_for_testing, value_1, value_2, expected_result):
    result = pow_x_y(db_instance=db_for_testing, value_1=value_1, value_2=value_2)

    assert result == expected_result
    return f"Function: 'pow_x_y', value1={value_1}, value2={value_2}, actual result={result}, expected result={expected_result}"


@logger_decorator(logger)
def test_update_record_description(request, db_for_testing):
    record_id = 1
    new_function_description = "Test updating field value"
    current_record = get_record(db_instance=db_for_testing, record_id=record_id)
    update_description(db_instance=db_for_testing, record_id=record_id, new_function_description=new_function_description)
    new_record = get_record(db_instance=db_for_testing, record_id=record_id)
    assert new_record.function_description == new_function_description
    return (f"Function: 'update_description', old function description: {current_record.function_description}, "
            f"new function description: {new_record.function_description}")


@logger_decorator(logger)
def test_delete_record(request, db_for_testing):
    record_id = 2
    delete_record(db_instance=db_for_testing, record_id=record_id)
    if not get_record(db_instance=db_for_testing, record_id=record_id):
        return f"Record with ID: {record_id} deleted successfully"
    assert False


@logger_decorator(logger)
def test_retrieve_record(request, db_for_testing):
    record_id = 1
    record_result = 3
    function_description = "Test updating field value"
    record = get_record(db_instance=db_for_testing, record_id=record_id)

    assert record.id == record_id
    assert record.function_description == function_description
    assert record.result == record_result

    return f"Record with ID:{record_id}, function_description: {function_description}, result: {record_result} successfully loaded from database. "
