import os
import shutil
import unittest

from click.testing import CliRunner

from photo_migrator import cli
from photo_migrator.utils import testing


class TestPhotom(testing.TempDirMixin, unittest.TestCase):
    """ Test photom commands """

    def setUp(self):
        testing.TempDirMixin.setUp(self)
        self.source_dir = os.path.join(self.temp_dir, "source_dir")
        shutil.copytree(testing.TEST_IMAGES_DIR, self.source_dir)
        self.out_dir = os.path.join(self.temp_dir, "out_dir")
        os.mkdir(self.out_dir)

    def check_cli_result(self, result):
        if result.exit_code != 0:
            raise result.exc_info[1]

    def test_photom_rename(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ["rename", self.source_dir])
        self.check_cli_result(result)
        expected = [
            '2017-05-28T06:00:49.jpg',
            '2017-07-02T16:54:00.jpg',
            'no_datetime.jpg',
            'no_datetime_larger.jpg',
        ]
        self.assertEqual(
            sorted(os.listdir(self.source_dir)),
            sorted(expected),
        )

    def test_photom_downsize(self):
        args = [
            "downsize",
            "--target-bytes", "1",
            self.source_dir, self.out_dir
        ]
        runner = CliRunner()
        result = runner.invoke(cli.main, args)
        self.check_cli_result(result)

        # Check the larger image is downsized
        large_filename = os.path.basename(testing.IMG_NO_DATETIME_LARGE)
        in_file = os.path.join(self.source_dir, large_filename)
        in_size = os.path.getsize(in_file)
        out_file = os.path.join(self.out_dir, large_filename)
        out_size = os.path.getsize(out_file)
        self.assertLess(out_size, in_size)
