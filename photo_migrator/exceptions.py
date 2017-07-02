""" This module defines Exception for the library.
"""


class DatetimeNotFound(BaseException):
    """ Raise when the DateTimeOriginal/DateTimeDigitized/DateTime of
    an image cannot be obtained.
    """
    pass


class ImageFormatError(BaseException):
    """ Raise when the image file cannot be processed due to its format."""
    pass
