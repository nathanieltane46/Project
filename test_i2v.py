import os
import tempfile
import unittest

from i2v import image_ref, video_url


class I2VTest(unittest.TestCase):
    def test_url_passes_through(self):
        self.assertEqual(image_ref("https://x/a.png"), "https://x/a.png")

    def test_local_file_becomes_data_uri(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG")
        try:
            self.assertEqual(image_ref(f.name), "data:image/png;base64,iVBORw==")
        finally:
            os.unlink(f.name)

    def test_non_image_rejected(self):
        with self.assertRaises(SystemExit):
            image_ref("notes.txt")

    def test_video_url_accepts_str_or_list(self):
        self.assertEqual(video_url("https://r/v.mp4"), "https://r/v.mp4")
        self.assertEqual(video_url(["https://r/v.mp4"]), "https://r/v.mp4")
        with self.assertRaises(SystemExit):
            video_url(None)


if __name__ == "__main__":
    unittest.main()
