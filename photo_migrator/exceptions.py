""" This module defines Exception for the library.
"""

class DatetimeNotFound(BaseException):
    """ Raise when the DateTimeOriginal/DateTimeDigitized/DateTime of
    an image cannot be obtained.
    """
    pass
