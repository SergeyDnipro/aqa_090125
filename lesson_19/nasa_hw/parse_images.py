import requests
import logging.config
from requests.exceptions import HTTPError, MissingSchema
from pathlib import Path
from json import JSONDecodeError
from lesson_19.logger_config import LOGGING_CONFIG


BASE_DIR = Path(__file__).parent
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('nasa_images_logger')


def get_response(*, url: str, params: dict = None):
    """ Get response from URL and catching errors. """

    error_messages = []

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data = response.json()
        logger.info(f"JSON data received on URL:{url}")
        return json_data

    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        error_messages.append(f"JSON decoding error, additional info in logfile")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        error_messages.append(f"Request failed, additional info in logfile")

    return error_messages


def parse_images(*, json_data, image_url_list=None) -> list:
    """ Recursion parsing unknown JSON document, finding following 'key'. Appending it to list. """

    if image_url_list is None:
        image_url_list = []

    if isinstance(json_data, list):
        for list_element in json_data:
            parse_images(json_data=list_element, image_url_list=image_url_list)

    if isinstance(json_data, dict):
        for key in json_data:
            if key == 'img_src':
                image_url_list.append(json_data[key])
            elif isinstance(json_data[key], (dict, list)):
                parse_images(json_data=json_data[key], image_url_list=image_url_list)

    return image_url_list


def process_images_on_url(*, url: str, params: dict = None):
    """ Getting response from URL, finding and validating data, saving to the following place. """
    data = get_response(url=url, params=params)
    images = parse_images(json_data=data)

    if not images:
        logger.warning(f"No images found on URL: {url}")
        return

    image_folder = create_image_folder(folder_name_part=params.get('sol'))
    for image_number, image_src in enumerate(images, 1):
        image = requests.get(image_src)
        with open(image_folder / f"mars_photo_{image_number}.jpg", "wb") as file:
            logger.info(f"Downloading image: {file.name}")
            file.write(image.content)


def create_image_folder(*, folder_name_part: int):
    img_folder = BASE_DIR / 'images/' / f"sol_{folder_name_part}"
    if not img_folder.exists():
        logger.info(f"Make folder: '{img_folder}'")
        img_folder.mkdir(parents=True)
    return img_folder


if __name__ == '__main__':
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    params = {'sol': 1000, 'camera': 'fhaz', 'api_key': 'DEMO_KEY'}
    process_images_on_url(url=url, params=params)
