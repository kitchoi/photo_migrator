import os
import shutil
import tempfile

import pkg_resources


THIS_PACKAGE = __name__.split(".", 1)[0]
TEST_IMAGES_DIR = pkg_resources.resource_filename(
    THIS_PACKAGE, "tests/images/"
)
# Image without datetime in the metadata
IMG_NO_DATETIME = os.path.join(TEST_IMAGES_DIR, "no_datetime.jpg")

# Image with DateTimeOriginal
IMG_WITH_DATETIME_ORIGINAL = os.path.join(
    TEST_IMAGES_DIR, "with_datetime_original.jpg"
)
# Image with DateTime (but not DateTimeOriginal)
IMG_WITH_DATETIME = os.path.join(
    TEST_IMAGES_DIR, "with_datetime_no_datetime_original.jpg"
)
# A larger image without datetime
IMG_NO_DATETIME_LARGE = os.path.join(TEST_IMAGES_DIR, "no_datetime_larger.jpg")


class TempDirMixin(object):
    """ Mixin for TestCase. Create a `temp_dir` temporary directory
    and clean up afterwards.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)
