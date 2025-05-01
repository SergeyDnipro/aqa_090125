import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record, self.datefmt)
        record.message = record.getMessage()
        if record.exc_info:
            message = f"[{record.asctime}][{record.levelname}] {record.message} - [{record.filename} :{record.exc_info[2].tb_lineno}]"
        else:
            message = f"[{record.asctime}][{record.levelname}] {record.message}"
        return message