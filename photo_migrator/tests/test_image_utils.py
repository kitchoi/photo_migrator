import datetime
import unittest

import pkg_resources

from photo_migrator.exceptions import DatetimeNotFound
from photo_migrator.utils import image_utils

THIS_PACKAGE = __name__.split(".", 1)[0]
# Image without datetime in the metadata
IMG_NO_DATETIME = pkg_resources.resource_filename(
    THIS_PACKAGE, "tests/images/no_datetime.jpg"
)
# Image with DateTimeOriginal
IMG_WITH_DATETIME_ORIGINAL = pkg_resources.resource_filename(
    THIS_PACKAGE, "tests/images/with_datetime_original.jpg"
)
# Image with DateTime (but not DateTimeOriginal)
IMG_WITH_DATETIME = pkg_resources.resource_filename(
    THIS_PACKAGE, "tests/images/with_datetime_no_datetime_original.jpg"
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
