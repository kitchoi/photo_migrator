import logging
import sys

import attr
import click

from photo_migrator.downsize_photos import downsize_photos, TARGET_IMAGE_BYTES
from photo_migrator.rename_photos import rename_photos
from photo_migrator.utils import log_utils

LOGGER = logging.getLogger("photo_migrator")

_IS_MAIN = (__name__ == "__main__")

@attr.s
class CliContext(object):

    log_level = attr.ib(default=logging.WARNING)

    dry_run = attr.ib(default=False)


@click.group()
@click.pass_context
@click.option(
    "--debug", is_flag=True, help="Set logging level to 'DEBUG'")
@click.option(
    "--verbose", "-v", is_flag=True, help="Set logging level to 'INFO'")
@click.option(
    "--dry-run", is_flag=True,
    help="Print proposed actions but do not comit them.")
def main(context, debug, verbose, dry_run):
    context.obj = CliContext()

    # Store dry_run
    context.obj.dry_run = dry_run

    # Set log_level
    if debug:
        context.obj.log_level = logging.DEBUG
    elif verbose:
        context.obj.log_level = logging.INFO

    if dry_run:
        context.obj.log_level = min(context.obj.log_level, logging.INFO)


@main.command()
@click.pass_context
@click.argument("dir_path")
def rename(context, dir_path):
    """ Rename all photos in a given directory using the date when it is
    created """
    set_logger_cm = log_utils.set_logger(
        logger=LOGGER,
        level=context.obj.log_level,
        stream=(sys.stdout if _IS_MAIN else sys.stderr))

    with set_logger_cm:
        rename_photos(dir_path=dir_path, dry_run=context.obj.dry_run)


@main.command()
@click.pass_context
@click.argument("source")
@click.argument("out_dir")
@click.option(
    "--overwrite", "-O",
    is_flag=True,
    help="Overwrite existing output files.",
)
@click.option(
    "--target-bytes",
    default=TARGET_IMAGE_BYTES,
    help="Target size in bytes.",
)
def downsize(context, source, out_dir, overwrite, target_bytes):
    """ Downsize photo(s) from SOURCE and export to OUT_DIR using the same
    relative path(s).
    """
    set_logger_cm = log_utils.set_logger(
        logger=LOGGER,
        level=context.obj.log_level,
        stream=(sys.stdout if _IS_MAIN else sys.stderr))
    with set_logger_cm:
        downsize_photos(
            dir_or_file=source, out_dir=out_dir,
            dry_run=context.obj.dry_run,
            overwrite=overwrite,
            size_in_bytes=target_bytes)
