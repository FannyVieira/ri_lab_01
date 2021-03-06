from ri_lab_01.settings import DEADLINE
from datetime import date

def is_valid_date(value):
    """Checks if value passed is greater than DEADLINE date.
    :param value: the data extracted by scrapy
    :return bool: if data is valid, else false.
    """
    DAY_DEADLINE, MONTH_DEADLINE, YEAR_DEADLINE = DEADLINE.split('.')
    DEADLINE_DATE = date(int(YEAR_DEADLINE), int(MONTH_DEADLINE), int(DAY_DEADLINE))

    # Extracted data is in following format: YYYY-MM-DD
    year, month, day = value.split('-')
    pub_date = date(int(year), int(month), int(day))

    return pub_date > DEADLINE_DATE