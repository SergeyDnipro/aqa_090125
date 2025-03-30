import requests
import logging.config
from json import JSONDecodeError
from lesson_19.logger_config import LOGGING_CONFIG


REMOTE_URL = 'http://127.0.0.1:8080/'
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('flask_logger')


def upload_image_request(*, filename: str):
    """ Upload file 'filename' to server. Handling and logging errors. """

    error_messages = []
    if not isinstance(filename, str):
        logger.error(f"{filename} must be 'str' type, current type: '{type(filename).__name__}'")
        return f"{filename} must be 'str' type, current type: '{type(filename).__name__}'"

    try:
        with open(filename, 'rb') as file:
            file_to_upload = {'image': file}
            response = requests.post(f"{REMOTE_URL}upload", files=file_to_upload)
            response.raise_for_status()
            json_data = response.json()
            logger.info(f"Upload complete {file.name}, URL: {json_data} status code: {response.status_code}")
            return json_data

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        error_messages.append(f"File not found: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        error_messages.append(f"Request failed, additional info in logfile")
    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        error_messages.append(f"JSON decoding error, additional info in logfile")

    return error_messages


def get_image_request(*, filename: str, content_type: str = 'text'):
    """ Retrieve JSON of image file URL or file instance depending on 'Content-Type'. Handling and logging errors."""

    error_messages = []
    headers = {'Content-Type': content_type}

    try:
        response = requests.get(f"{REMOTE_URL}image/{filename}", headers=headers)
        response.raise_for_status()

        if content_type == 'text':
            json_data = response.json()
            logger.info(f"Get image: {json_data}, status code: {response.status_code}")
            return json_data

        elif content_type == 'image':
            filename_prefix = filename[:filename.find('.')]
            with open(f"{filename_prefix}_copy.jpg", 'wb') as file:
                file.write(response.content)
            logger.info(f"{filename} Downloaded successfully. File saved to {file.name}")
            return file

    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        error_messages.append(f"JSON decoding error, additional info in logfile")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        error_messages.append(f"Request failed, additional info in logfile")

    return error_messages


def get_list_of_images_request():
    """ Retrieve JSON list of images URL in static folder 'uploads'. Handling and logging errors."""
    error_messages = []

    try:
        response = requests.get(f"{REMOTE_URL}")
        response.raise_for_status()
        json_data = response.json()
        return json_data

    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        error_messages.append(f"JSON decoding error, additional info in logfile")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        error_messages.append(f"Request failed, additional info in logfile")

    return error_messages


def delete_image_request(*, filename):
    """ Delete file 'filename' from server static folder 'uploads'. Handling and logging errors. """
    error_messages = []

    try:
        response = requests.delete(f"{REMOTE_URL}delete/{filename}")
        response.raise_for_status()
        json_data = response.json()
        logger.info(f"File '{filename}' deleted. Status code: {response.status_code}")
        return json_data

    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        error_messages.append(f"JSON decoding error, additional info in logfile")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        error_messages.append(f"Request failed, additional info in logfile")

    return error_messages


if __name__ == '__main__':

    print(upload_image_request(filename='mars_photo_2.jpg'))
    print(upload_image_request(filename='mars_photo_1.jpg'))
    print(upload_image_request(filename='mars_photo_123.jpg'))
    print(get_image_request(filename='mars_photo_1.jpg', content_type='image'))
    print(get_image_request(filename='mars_photo_1.jpg', content_type='text'))
    print(get_list_of_images_request())
    print(delete_image_request(filename='mars_photo_1.jpg'))
