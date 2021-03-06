import datetime
import logging
import os

from PIL import Image
from PIL.ExifTags import TAGS

from photo_migrator.exceptions import DatetimeNotFound

logger = logging.getLogger(__name__)

# Get the tag index for 'DateTimeOriginal'
_TAG_NAMES_TO_INDEX = {
    name: index
    for index, name in TAGS.items()
}

DATE_TIME_DIGITIZED = _TAG_NAMES_TO_INDEX["DateTimeDigitized"]
DATE_TIME = _TAG_NAMES_TO_INDEX["DateTime"]
DATE_TIME_ORIGINAL = _TAG_NAMES_TO_INDEX["DateTimeOriginal"]


def get_datetime_creation(photo_path):
    """ Return the datetime when a photo is created.

    Parameters
    ----------
    photo_path : str
        Path to a photo

    Returns
    -------
    datetime.datetime

    Raises
    ------
    DatetimeNotFound
        If the date cannot be obtained.
    """
    with Image.open(photo_path) as image:
        info = get_exif(image)

        for index in [DATE_TIME_ORIGINAL, DATE_TIME_DIGITIZED, DATE_TIME]:
            if index in info:
                date_time_str = info[index]
                logger.debug("Found {name}: {value!r}".format(
                    name=TAGS[index], value=date_time_str))
                break
        else:
            raise DatetimeNotFound(
                "Could not obtain DateTimeOriginal/DateTimeDigitized/DateTime "
                "for {!r}".format(photo_path))

    return datetime.datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")


def get_exif(image):
    """ Return the EXIF (dict) for a given PIL.Image.

    Parameters
    ----------
    image : PIL.Image.Image
        Image object

    Returns
    -------
    exif : dict
    """
    # There isn't a better and more reliable option from Image
    # for getting the EXIF.
    try:
        exif = image._getexif()
    except AttributeError:
        return {}
    else:
        if exif is None:
            return {}
        return exif


def is_photo(filepath):
    """ Return true if we can open the file as an image.
    """
    try:
        Image.open(filepath).close()
    except IOError:
        return False
    else:
        return True


def grep_all_image_paths(dir_path):
    """ Return all the file paths for files that can be opened as
    an image, search subdirectories recursively.

    Parameters
    ----------
    dir_path : str
        Path to a directory.

    Returns
    -------
    photo_paths : list of str
        List of absolute paths to the image files.
    """
    photo_paths = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            full_path = os.path.abspath(os.path.join(dirpath, filename))
            if is_photo(full_path):
                photo_paths.append(full_path)
    return photo_paths
