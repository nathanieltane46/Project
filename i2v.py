#!/usr/bin/env python3
"""Turn an image into a video with a free Hugging Face Space (Wan 2.2).

Usage: python3 i2v.py IMAGE ["PROMPT"] [-o out.mp4] [--seconds 3.5]
IMAGE is a local file or an http(s) URL. Set HF_TOKEN for a bigger free GPU quota.
"""
import argparse
import mimetypes
import os
import shutil
import sys

from gradio_client import Client, handle_file

# shortcut: tied to this one Space's API; if it goes away or changes, pick another and update predict() below.
SPACE = "zerogpu-aoti/wan2-2-fp8da-aoti-faster"


def check_image(path):
    """URLs pass through; local files must exist and look like an image."""
    if path.startswith(("http://", "https://")):
        return path
    if not os.path.isfile(path):
        sys.exit(f"No such file: {path}")
    mime = mimetypes.guess_type(path)[0] or ""
    if not mime.startswith("image/"):
        sys.exit(f"{path} does not look like an image ({mime or 'unknown type'})")
    return path


def video_path(result):
    """The Space returns (video, seed); video is a path or a {'video': path} dict."""
    video = result[0] if isinstance(result, (list, tuple)) else result
    if isinstance(video, dict):
        video = video.get("video")
    if not isinstance(video, str) or not os.path.isfile(video):
        sys.exit(f"Unexpected Space output: {result!r}")
    return video


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("prompt", nargs="?", default="make this image come alive, cinematic motion, smooth animation")
    p.add_argument("-o", "--out", default="out.mp4")
    p.add_argument("--seconds", type=float, default=3.5)
    a = p.parse_args()

    client = Client(SPACE, token=os.environ.get("HF_TOKEN"), verbose=False)
    try:
        result = client.predict(
            input_image=handle_file(check_image(a.image)),
            prompt=a.prompt,
            duration_seconds=a.seconds,
            api_name="/generate_video",
        )
    except Exception as e:  # quota and queue errors come back as generic AppErrors
        sys.exit(f"Space error: {e}")
    shutil.copy(video_path(result), a.out)
    print(a.out)


if __name__ == "__main__":
    main()
