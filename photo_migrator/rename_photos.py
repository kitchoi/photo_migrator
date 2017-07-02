""" This module provides a console script for renaming photos
using the date when the photo is take.
"""
import argparse
import logging
import os

import click
from photo_migrator.utils import image_utils

logger = logging.getLogger(__name__)


def rename_one_file(
        photo_path, fmt="%Y-%m-%dT%H:%M:%S%z", overwrite=False, dry_run=False):
    """ Rename a given photo using its creation date.

    Parameters
    ----------
    photo_path : str
        Path to the photo.
    fmt : str
        Format for the date.
    overwrite : boolean
        Whether overwriting existing file is allowed.
    dry_run : boolean
        If true, log proposed actions but not actually rename the file.

    Raises
    ------
    IOError
        If the output file exists and overwrite is false.
    """
    dirpath, basename = os.path.split(photo_path)
    _, file_ext = os.path.splitext(basename)
    timestamp = image_utils.get_datetime_creation(photo_path=photo_path)
    new_filename = timestamp.strftime(fmt)+file_ext
    if new_filename == basename:
        # Nothing to do, it is renamed to itself.
        logger.info("No renaming required.")
        return

    new_filepath = os.path.join(dirpath, new_filename)
    logger.info("Rename {!r} to {!r}".format(photo_path, new_filepath))

    if os.path.exists(new_filepath) and not overwrite:
        raise IOError(
            "{!r} already exists and overwrite is false. "
            "Doing nothing.".format(new_filepath))
    elif os.path.exists(new_filepath) and overwrite:
        logger.warning("Overwriting {!r}".format(new_filepath))

    if dry_run:
        return

    if os.path.exists(new_filepath):
        os.remove(new_filepath)
    os.rename(photo_path, new_filepath)


def rename_photos(dir_path, dry_run=False):
    """ Rename all the photos in a source directory using the datetime
    when they are created.  If the datetime cannot be obtained or that the
    target filename already exists, the renaming is skipped for that file.

    Parameters
    ----------
    dir_path : str
        Path to the source directory.
    dry_run : boolean
        If true, log the proposed action and then do nothing.
    """
    photo_paths = image_utils.grep_all_image_paths(dir_path)
    for photo_path in photo_paths:
        logger.info("Found {!r}".format(photo_path))
        try:
            rename_one_file(photo_path=photo_path, dry_run=dry_run)
        except (IOError, DatetimeNotFound) as exception:
            # Expected output files may exist or datetime cannot
            # be obtained.
            logger.error(str(exception))
            logger.debug(
                "Cannot rename photo {!r}.".format(photo_path),
                exc_info=True)
