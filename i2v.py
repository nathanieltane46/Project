#!/usr/bin/env python3
"""Turn an image into a video with a Replicate model.

Usage: REPLICATE_API_TOKEN=... python3 i2v.py IMAGE "PROMPT" [-o out.mp4] [--model owner/name]
IMAGE is a local file or an http(s) URL.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.replicate.com/v1"
# shortcut: input keys are fixed to "image"/"prompt", which Wan uses; other models (e.g. Kling's start_image) need --image-key.
DEFAULT_MODEL = "wan-video/wan-2.2-i2v-fast"


def call(method, url, body=None):
    req = urllib.request.Request(
        url,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Replicate {e.code}: {e.read().decode(errors='replace')}")


def image_ref(path):
    """URLs pass through; local files become a data URI."""
    if path.startswith(("http://", "https://")):
        return path
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    if not mime.startswith("image/"):
        sys.exit(f"{path} does not look like an image ({mime})")
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def video_url(output):
    """Models return either a URL or a list of URLs."""
    url = output[0] if isinstance(output, list) else output
    if not isinstance(url, str) or not url.startswith("http"):
        sys.exit(f"Unexpected model output: {output!r}")
    return url


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("prompt")
    p.add_argument("-o", "--out", default="out.mp4")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--image-key", default="image", help="input field name the model uses for the image")
    a = p.parse_args()
    if "REPLICATE_API_TOKEN" not in os.environ:
        sys.exit("Set REPLICATE_API_TOKEN (https://replicate.com/account/api-tokens)")

    pred = call("POST", f"{API}/models/{a.model}/predictions",
                {"input": {a.image_key: image_ref(a.image), "prompt": a.prompt}})
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        print(f"{pred['status']}...", file=sys.stderr)
        time.sleep(5)
        pred = call("GET", pred["urls"]["get"])
    if pred["status"] != "succeeded":
        sys.exit(f"Prediction {pred['status']}: {pred.get('error')}")

    urllib.request.urlretrieve(video_url(pred["output"]), a.out)
    print(a.out)


if __name__ == "__main__":
    main()
