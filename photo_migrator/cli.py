import logging

import attr
import click

from photo_migrator.downsize_photos import downsize_photos
from photo_migrator.rename_photos import rename_photos
from photo_migrator.utils import log_utils

LOGGER = logging.getLogger("photo_migrator")

@attr.s
class CliContext(object):

    log_level = attr.ib(default=logging.WARNING)


@click.group()
@click.pass_context
@click.option(
    "--debug", is_flag=True, help="Set logging level to 'DEBUG'")
@click.option(
    "--verbose", "-v", is_flag=True, help="Set logging level to 'INFO'")
def main(context, debug, verbose):
    context.obj = CliContext()
    if debug:
        context.obj.log_level = logging.DEBUG
    elif verbose:
        context.obj.log_level = logging.INFO


@main.command()
@click.pass_context
@click.argument("dir_path")
@click.option(
    "--dry-run", is_flag=True,
    help="Print proposed actions but do not comit them.")
def rename(context, dir_path, dry_run):
    log_level = context.obj.log_level
    if dry_run:
        log_level = min(log_level, logging.INFO)

    with log_utils.set_logger(logger=LOGGER, level=log_level):
        rename_photos(dir_path=dir_path, dry_run=dry_run)


@main.command()
@click.pass_context
@click.argument("source_dir")
@click.argument("out_dir")
@click.option(
    "--dry-run", is_flag=True,
    help="Print proposed actions but do not comit them.")
def downsize(context, source_dir, out_dir, dry_run):
    log_level = context.obj.log_level
    if dry_run:
        log_level = min(log_level, logging.INFO)

    with log_utils.set_logger(logger=LOGGER, level=log_level):
        downsize_photos(
            dir_path=source_dir, out_dir=out_dir, dry_run=dry_run)
