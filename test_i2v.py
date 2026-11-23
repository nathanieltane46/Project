import os
import tempfile
import unittest

from i2v import check_image, video_path


class I2VTest(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            self.png = f.name

    def tearDown(self):
        os.unlink(self.png)

    def test_url_passes_through(self):
        self.assertEqual(check_image("https://x/a.png"), "https://x/a.png")

    def test_local_image_accepted(self):
        self.assertEqual(check_image(self.png), self.png)

    def test_missing_or_non_image_rejected(self):
        with self.assertRaises(SystemExit):
            check_image("nope.png")
        with self.assertRaises(SystemExit):
            check_image(__file__)

    def test_video_path_shapes(self):
        self.assertEqual(video_path((self.png, 42)), self.png)
        self.assertEqual(video_path(({"video": self.png}, 42)), self.png)
        with self.assertRaises(SystemExit):
            video_path((None, 42))


if __name__ == "__main__":
    unittest.main()
