import argparse
import datetime
from functools import partial
import math
import logging
import os
import shutil
from pathlib import Path

from PIL import Image

from photo_migrator.exceptions import DatetimeNotFound
from photo_migrator.utils import image_utils

logger = logging.getLogger(__name__)

TARGET_IMAGE_BYTES = 1048576


def downsize(image, target_size=TARGET_IMAGE_BYTES, resample=Image.ANTIALIAS):
    """ Downsize the given image to the target size.

    Parameters
    ----------
    image : PIL.Image
        Loaded image to be downsized.
    target_size : int
        Target file size in bytes.
    resample : int
        Resample method
    """
    original_size = os.path.getsize(image.filename)
    ratio = math.sqrt(target_size/float(original_size))
    new_size = tuple(
        max(1, int(value*ratio)) for value in image.size
    )
    logger.debug("Target size %r", new_size)
    image.thumbnail(new_size, resample=resample)


def copy_photo(
        photo_path, out_path,
        create_dir=True, transform=None, overwrite=False):
    """ Apply a tranform function to an image and export the output.

    Parameters
    ----------
    photo_path : str
        Path to the source image.
    out_path : str
        Path to the output file.
    create_dir : boolean
        Whether to create intermediate folders if not already exist.
    transform : callable(PIL.Image)
        Tranform function for the loaded image.
    overwrite : boolean
        Whether overwriting existing file is allowed.

    Raises
    ------
    IOError
        - If the output path already exists and overwrite is false.
        - If the output path is in a directory that does not exist and
          create_dir is false.
    """
    if os.path.exists(out_path) and not overwrite:
        raise IOError("{} already exists.".format(out_path))
    elif os.path.exists(out_path) and overwrite:
        logger.warning("Overwriting {!r}".format(out_path))

    out_dir, filename = os.path.split(out_path)
    if not os.path.exists(out_dir):
        if create_dir:
            Path(out_dir).mkdir(mode=0o775, parents=True)
        else:
            raise IOError("{!r} does not exist.".format(out_dir))

    if transform is None:
        shutil.copy(photo_path, out_path)
    else:
        with Image.open(photo_path) as im:
            transform(im)
            im.save(out_path)


def downsize_photos(
        dir_path, out_dir, overwrite=False, dry_run=False,
        size_in_bytes=TARGET_IMAGE_BYTES):
    """ Downsize all the photos in a given directory and export the
    output to the output directory with the same relative paths.

    Parameters
    ----------
    dir_path : str
        Path to the source directory.
    out_path : str
        Path to the output directory.
    overwrite : boolean
        Whether overwriting existing file is allowed.
    dry_run : boolean
        If true, log the proposed action and then do nothing.
    size_in_bytes : int
        Target image size in bytes.
    """
    photo_paths = image_utils.grep_all_image_paths(dir_path)
    transform_fun = partial(downsize, target_size=size_in_bytes)
    for photo_path in photo_paths:
        out_path = os.path.join(
            out_dir, os.path.relpath(photo_path, start=dir_path))
        logger.info("Downsize {!r} -> {!r}".format(photo_path, out_path))

        if dry_run:
            continue

        try:
            copy_photo(
                photo_path=photo_path, out_path=out_path,
                transform=transform_fun, overwrite=overwrite)
        except (IOError, DatetimeNotFound) as exception:
            # Expected output files may exist or datetime cannot
            # be obtained.
            logger.error(exception)
            logger.debug(
                "Cannot downsize photo {!r}.".format(photo_path),
                exc_info=True)
