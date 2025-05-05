import pytest
from np_tracking_page import NovaPostEN

EN_URL = 'https://tracking.novaposhta.ua/#/uk'


@pytest.mark.parametrize('en_number', [
    '20400453699415',
    '20400453699415',
    '20415453699415',
])
def test_novapost_en_status(browser, en_number):
    """ Test EN status """
    np_opened_page = NovaPostEN(browser, EN_URL)
    assert np_opened_page.driver is not None
    en_response = np_opened_page.check_en(en_number)
    assert en_response == 'Отримана'
