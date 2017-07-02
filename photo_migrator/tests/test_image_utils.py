import datetime
import unittest

from photo_migrator.exceptions import DatetimeNotFound
from photo_migrator.utils import image_utils
from photo_migrator.utils.testing import (
        IMG_NO_DATETIME, IMG_WITH_DATETIME, IMG_WITH_DATETIME_ORIGINAL
)


class TestImageUitils(unittest.TestCase):

    def test_get_datetime_creation_fail(self):
        with self.assertRaises(DatetimeNotFound):
            image_utils.get_datetime_creation(IMG_NO_DATETIME)

    def test_get_datetime_creation_with_original(self):
        actual = image_utils.get_datetime_creation(IMG_WITH_DATETIME_ORIGINAL)
        expected = datetime.datetime(2017, 5, 28, 6, 0, 49)
        self.assertEqual(actual, expected)

    def test_get_datetime_creation_with_datetime(self):
        actual = image_utils.get_datetime_creation(IMG_WITH_DATETIME)
        expected = datetime.datetime(2017, 7, 2, 16, 54, 0)
        self.assertEqual(actual, expected)
