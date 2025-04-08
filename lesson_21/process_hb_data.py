from datetime import timedelta, datetime
from logger_conf import logger


def process_heart_beating_file(*, filename, thread_id: str, hb_delta_normal: int, hb_delta_high: int):
    """
     Function to process file with timestamps and filtering due to the params:
    - 'thread_id': 'string' value of thread,
    - 'hb_delta_normal': 'int' value of normal time rate between signals (seconds),
    - 'hb_delta_high': 'int' value of highest time rate between signals (seconds),
    """
    timedelta_normal = timedelta(seconds=hb_delta_normal)
    timedelta_high = timedelta(seconds=hb_delta_high)
    time_format = '%H:%M:%S'
    start_time_str = None
    start_time_datetime_obj = None
    temp_list = []

    try:
        # Try to open file, handle and logging errors. Creating list of valid records (in accordance to our thread_id).
        with open(filename, 'r', encoding='utf-8') as file:
            for row_number, row in enumerate(file, 1):
                if thread_id in row:
                   temp_list.append((row, row_number)) # Appending tuple with record and appropriate row number in original file.
            if not temp_list:
                logger.critical(f"No records with thread ID:'{thread_id}' found")
    except FileNotFoundError:
        logger.critical(f"File not found - {filename}")

    for record_instance, row_number in temp_list:
        # Try to get Datetime Objects from string values of timestamps. Handle and logging errors.
        try:
            if record_instance.find('Timestamp ') == -1:
                raise ValueError(f"No 'timestamp' label found in the record")
            timestamp_start_index = record_instance.find("Timestamp ") + 10
            end_time_str = record_instance[timestamp_start_index:timestamp_start_index + 8]
            end_time_datetime_obj = datetime.strptime(end_time_str, time_format)

            if not start_time_str:
                start_time_str, start_time_datetime_obj = end_time_str, end_time_datetime_obj
                continue

            timedelta_current = start_time_datetime_obj - end_time_datetime_obj

            # Logging following data due to the current record timedelta checking result.
            if timedelta_high > timedelta_current > timedelta_normal:
                logger.warning(f"Between current TS[{start_time_str}] and previous TS[{end_time_str}] - "
                               f"{timedelta_current.seconds} seconds, row # {row_number}")
            elif timedelta_current >= timedelta_high:
                logger.error(f"  Between current TS[{start_time_str}] and previous TS[{end_time_str}] - "
                             f"{timedelta_current.seconds} seconds, row # {row_number}")

            start_time_str, start_time_datetime_obj = end_time_str, end_time_datetime_obj

        except ValueError as e:
            logger.error(f"  ValueError: {e}, row # {row_number}")


if __name__ == '__main__':
    process_heart_beating_file(
        filename='hblog.txt',
        thread_id='TSTFEED0300|7E3E|0400',
        hb_delta_normal=31,
        hb_delta_high=33
    )
