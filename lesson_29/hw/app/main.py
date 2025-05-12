from db_driver import DatabaseHandler, Dataset
import inspect


def add_x_y(db_instance, value_1: float, value_2: float):
    result = value_1 + value_2
    function_description = f"{inspect.currentframe().f_code.co_name}, operation: {value_1} + {value_2}"
    db_instance.add_record(function_description=function_description, result=result)
    return result


def pow_x_y(db_instance, value_1: float, value_2: int):
    result = value_1 ** value_2
    function_description = f"{inspect.currentframe().f_code.co_name}, operation: {value_1} ** {value_2}"
    db_instance.add_record(function_description=function_description, result=result)
    return result


def update_description(db_instance, record_id: int, new_function_description: str):
    db_instance.update_record(record_id=record_id, new_function_description=new_function_description)


def get_record(db_instance, record_id: int):
    return db_instance.get_record(record_id=record_id)


def delete_record(db_instance, record_id: int):
    return db_instance.delete_record(record_id=record_id)


if __name__ == "__main__":
    db = DatabaseHandler(Dataset)
    add_x_y(db_instance=db, value_1=1, value_2=2)
    pow_x_y(db_instance=db, value_1=10, value_2=5)
    get_record(db_instance=db, record_id=1)
