import argparse
from collections import Counter
import datetime
from functools import partial
import math
import logging
import os
import shutil
from pathlib import Path

from PIL import Image

from photo_migrator.utils import image_utils

logger = logging.getLogger(__name__)


def downsize(image, target_size=1048576, resample=Image.ANTIALIAS):
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
    width, height = image.size
    new_size = (int(width*ratio), int(height*ratio))
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
    """
    if os.path.exists(out_path) and not overwrite:
        raise IOError("{} already exists.".format(out_path))

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


def downsize_photos(dir_path, out_dir, overwrite=False, dry_run=False):
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
    """
    photo_paths = image_utils.grep_all_image_paths(dir_path)
    for photo_path in photo_paths:
        out_path = os.path.join(
            out_dir, os.path.relpath(photo_path, start=dir_path))
        logger.info("Downsize {!r} -> {!r}".format(photo_path, out_path))
        if not dry_run:
            copy_photo(
                photo_path=photo_path, out_path=out_path,
                transform=downsize, overwrite=overwrite)